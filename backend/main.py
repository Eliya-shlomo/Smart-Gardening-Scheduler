from fastapi import FastAPI
from backend.database import engine
from backend.models import Base
from backend.api import user, client, tree, appointment,recommendation, reports, email_log
from backend.services.scheduler import start_scheduler
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(client.router)  
app.include_router(tree.router)  
app.include_router(appointment.router)
app.include_router(recommendation.router)
app.include_router(reports.router)
app.include_router(email_log.router)






@app.get("/")
def read_root():
    # start_scheduler()
    return {"message": "Smart Gardening API is up!"}

