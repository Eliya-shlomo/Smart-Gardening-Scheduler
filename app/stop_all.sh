#!/bin/bash

echo "🛑 Stopping all FastAPI microservices..."

pkill -f uvicorn

echo "✅ All services stopped."
