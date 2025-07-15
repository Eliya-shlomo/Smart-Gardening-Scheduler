from fastapi import FastAPI
from app.users.api import user as user_router     
from app.users.api import token as token_router    

app = FastAPI()

app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(token_router.router, prefix="/users", tags=["Tokens"])

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
