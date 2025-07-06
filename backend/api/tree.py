from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.tree import TreeCreate, TreeResponse
from backend.api.deps import get_current_user
from backend.models.user import User
from backend.models.client import Client
from backend.crud.tree import get_tree_by_id as crud_get_tree_by_id
from backend.crud.tree import create_tree, get_trees_for_client


router = APIRouter(prefix="/trees", tags=["Trees"])

@router.post("/", response_model=TreeResponse)
def create_tree_view(tree_in: TreeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    client = db.query(Client).filter(Client.id == tree_in.client_id, Client.user_id == current_user.id).first()
    if not client:
        raise HTTPException(status_code=403, detail="You do not have access to this client")
    return create_tree(db, tree_in)

@router.get("/client/{client_id}", response_model=list[TreeResponse])
def get_trees_for_client_view(client_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    client = db.query(Client).filter(Client.id == client_id, Client.user_id == current_user.id).first()
    if not client:
        raise HTTPException(status_code=403, detail="Client not found or unauthorized")
    return get_trees_for_client(db, client_id)

@router.get("/{tree_id}", response_model=TreeResponse)
def get_tree_by_id(tree_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tree = crud_get_tree_by_id(db, tree_id)
    if not tree:
        raise HTTPException(status_code=404, detail="Tree not found")
    if tree.client.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return tree
