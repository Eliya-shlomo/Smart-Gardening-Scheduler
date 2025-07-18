from fastapi import FastAPI
from inventory.api.tree import router as tree     
from inventory.database import Base, engine
from inventory.models.tree import Tree 

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(tree, prefix="/inventory", tags=["inventory"])



@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
