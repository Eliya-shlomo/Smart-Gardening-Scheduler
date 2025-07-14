from fastapi import FastAPI
from api.user import router as user_router

app = FastAPI(
    title="Users Microservice",
    version="1.0.0"
)

app.include_router(user_router)
