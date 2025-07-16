from fastapi import FastAPI
from audit.api.audit import router as log_forword     
from audit.database import Base, engine
from audit.models.audit import AuditLog 

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(log_forword, prefix="/audit_log", tags=["Audit_Log"])



@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
