from fastapi import FastAPI
from app.users.api.login import router as login_router
from app.users.api.register import router as register_router
from app.users.api.refresh import router as refresh_router
from app.users.api.logout import router as logout_router
from app.users.api.user import router as user_router

app = FastAPI()
app.include_router(login_router)
app.include_router(register_router)
app.include_router(refresh_router)
app.include_router(logout_router)
app.include_router(user_router)

