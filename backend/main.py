from fastapi import FastAPI
from backend.database import engine
from backend.models import Base

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Smart Gardening API is up!"}

