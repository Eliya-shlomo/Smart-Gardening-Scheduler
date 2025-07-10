#!/bin/bash
job=$1

echo "Waiting for job $job to complete..."
for i in {1..30}; do
  status=$(kubectl get job $job -o jsonpath='{.status.conditions[?(@.type=="Complete")].status}')
  if [[ "$status" == "True" ]]; then
    echo "✅ Job completed"
    exit 0
  fi

  failed=$(kubectl get job $job -o jsonpath='{.status.conditions[?(@.type=="Failed")].status}')
  if [[ "$failed" == "True" ]]; then
    echo "❌ Job failed"
    exit 1
  fi

  sleep 5
done

echo "⏰ Timeout waiting for job"
exit 1
