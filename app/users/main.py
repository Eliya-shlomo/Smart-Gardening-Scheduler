from fastapi import FastAPI
from users.api.login import router as user_login     
from users.api.register import router as user_register   
from users.api.logout import router as user_logout
from users.api.user import router as user_me
from users.api.refresh import router as token_refresh
from users.database import Base, engine 
import redis.asyncio as redis


redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_login, prefix="/users", tags=["Users"])
app.include_router(user_register, prefix="/users", tags=["Users"])
app.include_router(user_logout, prefix="/users", tags=["Users"])
app.include_router(user_me, prefix="/users", tags=["Users"])
app.include_router(token_refresh, prefix="/users", tags=["Users"])


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
