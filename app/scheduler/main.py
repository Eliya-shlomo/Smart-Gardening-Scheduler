from fastapi import FastAPI
from scheduler.api.appointment import router as appointment     
from notification.database import Base, engine
from scheduler.models.appointment import Appointment 

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(appointment, prefix="/scheduler")



@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
