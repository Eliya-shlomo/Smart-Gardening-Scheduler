from fastapi import FastAPI
from users.api.login import router as user_login     
from users.api.register import router as user_register   
from users.api.logout import router as user_logout
from users.api.user import router as user_me
from users.api.refresh import router as token_refresh
from users.database import Base, engine 
import redis.asyncio as redis

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import time
from starlette.middleware.base import BaseHTTPMiddleware

# ----- Prometheus Metrics -----
REQUEST_COUNTER = Counter('http_requests_total', 'Total HTTP requests')
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'Latency of HTTP requests in seconds')

# ----- Redis & DB -----
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)
Base.metadata.create_all(bind=engine)

# ----- FastAPI -----
app = FastAPI()

# ----- Prometheus Middleware -----
class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        REQUEST_COUNTER.inc()
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        REQUEST_LATENCY.observe(duration)
        return response

app.add_middleware(MetricsMiddleware)

# ----- Routers -----
app.include_router(user_login, prefix="/users", tags=["Users"])
app.include_router(user_register, prefix="/users", tags=["Users"])
app.include_router(user_logout, prefix="/users", tags=["Users"])
app.include_router(user_me, prefix="/users", tags=["Users"])
app.include_router(token_refresh, prefix="/users", tags=["Users"])

# ----- Health -----
@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}

# ----- Metrics -----
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
