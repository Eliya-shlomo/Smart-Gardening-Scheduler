pipeline {
  agent any

  environment {
    AWS_REGION = "us-east-1"
    ECR_REPO = "261303806788.dkr.ecr.us-east-1.amazonaws.com/smart-gardening-scheduler"
    GIT_BRANCH = "main" 
  }

  stages {
    stage('Checkout Code') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker :test') {
      steps {
        sh 'docker build -t $ECR_REPO:test .'
      }
    }

    stage('Push :test to ECR') {
      steps {
        withCredentials([usernamePassword(
          credentialsId: 'aws-credentials',
          usernameVariable: 'AWS_ACCESS_KEY_ID',
          passwordVariable: 'AWS_SECRET_ACCESS_KEY'
        )]) {
          sh '''
            aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
            aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
            aws configure set region $AWS_REGION
            aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO
            docker push $ECR_REPO:test
          '''
        }
      }
    }

    stage('Run K8s Test Job') {
      steps {
        sh '''
          kubectl delete job scheduler-test-job --ignore-not-found
          kubectl apply -f k8s/test-job.yaml
          ./scripts/wait_for_job.sh scheduler-test-job
        '''
      }
    }

    stage('Tag & Push :latest') {
      steps {
        sh '''
          docker tag $ECR_REPO:test $ECR_REPO:latest
          docker push $ECR_REPO:latest
        '''
      }
    }

    stage('Deploy to K8s') {
      steps {
        sh 'kubectl apply -f k8s/deployment.yaml'
      }
    }

    stage('Push to Git (optional)') {
      steps {
        sh '''
          git config user.email "jenkins@ci"
          git config user.name "Jenkins CI"
          git add .
          git commit -m "CI: Successful build & deploy [skip ci]" || echo "No changes to commit"
          git push origin $GIT_BRANCH
        '''
      }
    }
  }

  post {
    failure {
      echo "❌ Pipeline failed. Deployment was not performed."
    }
    success {
      echo "✅ Pipeline completed successfully."
    }
  }
}
