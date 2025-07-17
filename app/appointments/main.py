from fastapi import FastAPI
from appointments.api.appointments import router as appointments     
from appointments.database import Base, engine
from appointments.models.appointments import Appointment 

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(appointments, prefix="/appointments", tags=["Audit_Log"])



@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
