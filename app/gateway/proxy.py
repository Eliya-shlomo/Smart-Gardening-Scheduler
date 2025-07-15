import httpx
from fastapi import Request, Response

SERVICE_URLS = {
    "users":     "http://users-service",     
    "clients":   "http://clients-service",
    "scheduler": "http://scheduler-service",
    "inventory": "http://inventory-service",
    "audit":     "http://audit-service",
}


async def proxy_request(request: Request, service_name: str, path: str):
    service_url = SERVICE_URLS[service_name] + path
    async with httpx.AsyncClient() as client:
        body = await request.body()
        headers = dict(request.headers)
        method = request.method.lower()
        resp = await client.request(method, service_url, content=body, headers=headers)
        return Response(content=resp.content, status_code=resp.status_code, headers=resp.headers)
