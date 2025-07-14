import httpx
from fastapi import Request, Response

SERVICE_URLS = {
    "users": "http://localhost:8001",
    "clients": "http://localhost:8002",
    "scheduler": "http://localhost:8003",
    "inventory": "http://localhost:8004",
    "audit": "http://localhost:8005",
}


async def proxy_request(request: Request, service_name: str, path: str):
    service_url = SERVICE_URLS[service_name] + path
    async with httpx.AsyncClient() as client:
        body = await request.body()
        headers = dict(request.headers)
        method = request.method.lower()
        resp = await client.request(method, service_url, content=body, headers=headers)
        return Response(content=resp.content, status_code=resp.status_code, headers=resp.headers)
