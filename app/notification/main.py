from fastapi import FastAPI
from notification.api.recommendation import router as recommendation     
from notification.database import Base, engine
from notification.models.recommendation import Recommendation 
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import time
from starlette.middleware.base import BaseHTTPMiddleware


# ----- Prometheus Metrics -----
REQUEST_COUNTER = Counter('http_requests_total', 'Total HTTP requests')
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'Latency of HTTP requests in seconds')

Base.metadata.create_all(bind=engine)

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


app.include_router(recommendation, prefix="/notification")



@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)