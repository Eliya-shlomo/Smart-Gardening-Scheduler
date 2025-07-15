from fastapi import FastAPI
from audit.api.audit import router as log_forword     



app = FastAPI()

app.include_router(log_forword, prefix="/audit_log", tags=["Audit_Log"])



@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
