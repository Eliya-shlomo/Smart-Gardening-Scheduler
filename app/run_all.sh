#!/bin/bash

echo "🚀 Starting all FastAPI microservices in background..."

mkdir -p logs

nohup uvicorn users.main:app --host 0.0.0.0 --port 8001 > logs/users.log 2>&1 &
nohup uvicorn clients.main:app --host 0.0.0.0 --port 8002 > logs/clients.log 2>&1 &
nohup uvicorn audit.main:app --host 0.0.0.0 --port 8003 > logs/audit.log 2>&1 &
nohup uvicorn appointments.main:app --host 0.0.0.0 --port 8004 > logs/appointments1.log 2>&1 &
nohup uvicorn inventory.main:app --host 0.0.0.0 --port 8005 > logs/inventory.log 2>&1 &
nohup uvicorn appointments.main:app --host 0.0.0.0 --port 8006 > logs/appointments2.log 2>&1 &
nohup uvicorn notification.main:app --host 0.0.0.0 --port 8007 > logs/notification.log 2>&1 &

echo "✅ All microservices started in background. Check logs in ./logs/"
