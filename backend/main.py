from fastapi import FastAPI
from backend.database import engine
from backend.models import Base
from backend.api import user, client

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(client.router)  



@app.get("/")
def read_root():
    return {"message": "Smart Gardening API is up!"}

