#!/bin/bash

job=$1

echo "📡 Waiting for job '$job' to complete..."
for i in {1..90}; do
  status=$(kubectl get job "$job" -o jsonpath='{.status.conditions[?(@.type=="Complete")].status}')
  if [[ "$status" == "True" ]]; then
    echo "✅ Job '$job' completed successfully"
    exit 0
  fi

  failed=$(kubectl get job "$job" -o jsonpath='{.status.conditions[?(@.type=="Failed")].status}')
  if [[ "$failed" == "True" ]]; then
    echo "❌ Job '$job' failed"
    echo "🔍 Job describe:"
    kubectl describe job "$job"

    echo "📦 Related pod logs:"
    pod=$(kubectl get pods --selector=job-name="$job" -o jsonpath='{.items[0].metadata.name}')
    kubectl logs "$pod"

    exit 1
  fi

  sleep 5
done

echo "⏰ Timeout: Job '$job' did not complete within expected time"
echo "🔍 Job describe:"
kubectl describe job "$job"

echo "📦 Related pod logs:"
pod=$(kubectl get pods --selector=job-name="$job" -o jsonpath='{.items[0].metadata.name}')
kubectl logs "$pod"

exit 1
