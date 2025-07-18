from fastapi import FastAPI
from notification.api.recommendation import router as recommendation     
from notification.database import Base, engine
from notification.models.recommendation import Recommendation 

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(recommendation, prefix="/notification")



@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
