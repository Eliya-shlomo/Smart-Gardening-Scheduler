#!/bin/bash

echo "🚀 Starting all FastAPI microservices in background..."

uvicorn users.main:app --host 0.0.0.0 --port 8001 &
uvicorn clients.main:app --host 0.0.0.0 --port 8002 &
uvicorn audit.main:app --host 0.0.0.0 --port 8003 &
uvicorn appointments.main:app --host 0.0.0.0 --port 8004 &
uvicorn inventory.main:app --host 0.0.0.0 --port 8005 &
uvicorn notification.main:app --host 0.0.0.0 --port 8006 &
uvicorn scheduler.main:app --host 0.0.0.0 --port 8007 &

echo "✅ All microservices started in background."
