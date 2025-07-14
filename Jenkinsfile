pipeline {
  agent any

  environment {
    AWS_REGION = "us-east-1"
    ECR_REPO = "261303806788.dkr.ecr.us-east-1.amazonaws.com/smart-gardening-scheduler"
    IMAGE_TAG = "dev-${env.BUILD_NUMBER}"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout([
        $class: 'GitSCM',
        branches: [[name: '*/dev']],
        userRemoteConfigs: [[
          url: 'git@github.com:Eliya-shlomo/Smart-Gardening-Scheduler.git',
          credentialsId: 'git-ssh-key',
          refspec: '+refs/heads/*:refs/remotes/origin/*'
          ]]
        ])
      } 
    }
  }

  stage('Save current latest digest') {
    steps {
      withCredentials([usernamePassword(credentialsId: 'aws-credentials', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
        sh '''
            aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
            aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
            aws configure set region $AWS_REGION
            aws ecr batch-get-image \
              --repository-name smart-gardening-scheduler \
              --image-ids imageTag=latest \
              --query 'images[0].imageDigest' \
              --output text > latest_digest.txt || echo "none" > latest_digest.txt
        '''
      }
    }
  }

    stage('Build Docker Image') {
      steps {
        sh 'docker build -t $ECR_REPO:$IMAGE_TAG .'
      }
    }

    stage('Push Image to ECR') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'aws-credentials', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
          sh '''
            aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
            aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
            aws configure set region $AWS_REGION
            aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO
            docker push $ECR_REPO:$IMAGE_TAG
          '''
        }
      }
    }

    stage('Run K8s Test Job') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'aws-credentials', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
        sh '''
          kubectl delete job scheduler-test --ignore-not-found --wait=true
          sed "s|__IMAGE__|$ECR_REPO:$IMAGE_TAG|g" k8s/test-job.yaml | kubectl replace --force -f -
          ./scripts/wait_for_job.sh scheduler-tests
        '''
        }
      }
    }


    stage('Merge dev → main') {
      when {
        branch 'dev'
        expression { sh(script: './scripts/wait_for_job.sh scheduler-tests', returnStatus: true) == 0 }
      }
      steps {
        sshagent (credentials: ['git-ssh-key']) {
          sh '''
            git config --global user.name "jenkins"
            git config --global user.email "jenkins@ci"
            git fetch origin main
            git checkout -B main origin/main
            git pull origin main
            git merge dev --no-edit
            git push origin main
          '''
        }
      }
    }

    stage('Tag & Push :latest') {
      when {
        branch 'dev'
        expression { sh(script: './scripts/wait_for_job.sh scheduler-tests', returnStatus: true) == 0 }
      }
      steps {
        sh '''
          docker tag $ECR_REPO:$IMAGE_TAG $ECR_REPO:latest
          docker push $ECR_REPO:latest
        '''
      }
    }

    stage('Deploy to K8s') {
      when {
        branch 'dev'
        expression { sh(script: './scripts/wait_for_job.sh scheduler-tests', returnStatus: true) == 0 }
      }
      steps {
        sh 'kubectl apply -f k8s/deployment.yaml'
      }
    }
  }

  post {
    failure {
      echo "❌ Build or tests failed. main was not updated, and :latest remains unchanged."
    }
    success {
      echo "✅ Pipeline completed successfully. main and :latest updated only after passing tests."
    }
  }
}
