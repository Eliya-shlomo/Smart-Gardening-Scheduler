from fastapi import FastAPI
from clients.api.clients import router as client_router     





app = FastAPI()

app.include_router(client_router, prefix="/clients", tags=["Clients"])



@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
