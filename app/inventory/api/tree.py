from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from inventory.database import get_db
from inventory.schemas.tree import TreeCreate, TreeResponse, TreeUpdate
from inventory.utils.get_current_user import get_current_user
from inventory.utils.audit_logger import send_log
from inventory.crud.tree import create_tree, get_trees_for_client, get_tree_by_id
from inventory.models.tree import Tree
import httpx


CLIENT_SERVICE_URL = "http://localhost:8002"

async def verify_client_access(client_id: int, request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{CLIENT_SERVICE_URL}/clients/{client_id}/access",
                headers={"Authorization": auth_header},
                timeout=5
            )
            if resp.status_code != 200:
                raise HTTPException(status_code=403, detail="No access to this client")
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail=f"Client service unavailable: {exc}")

router = APIRouter(prefix="/trees", tags=["Trees"])

@router.post("/", response_model=TreeResponse)
async def create_tree_view(
    tree_in: TreeCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    await verify_client_access(tree_in.client_id, request)
    tree = create_tree(db, tree_in)
    send_log(
        user_id=current_user["id"],
        action="create",
        entity_type="Tree",
        entity_id=tree.id,
        details=f"Created tree: {tree.type} for client_id={tree.client_id}"
    )
    return tree

@router.get("/client/{client_id}", response_model=list[TreeResponse])
async def get_trees_for_client_view(
    client_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    await verify_client_access(client_id, request)
    return get_trees_for_client(db, client_id)

@router.get("/{tree_id}", response_model=TreeResponse)
async def get_tree_by_id_view(
    tree_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    tree = get_tree_by_id(db, tree_id)
    if not tree:
        raise HTTPException(status_code=404, detail="Tree not found")
    # בדוק הרשאה מול המיקרוסרביס (ע"פ tree.client_id)
    await verify_client_access(tree.client_id, request)
    return tree

@router.put("/{tree_id}", response_model=TreeResponse)
async def update_tree(
    tree_id: int,
    request: Request,
    tree_in: TreeUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    tree = get_tree_by_id(db, tree_id)
    if not tree:
        raise HTTPException(status_code=404, detail="Tree not found")
    await verify_client_access(tree.client_id, request)
    tree.type = tree_in.type
    tree.planting_date = tree_in.planting_date
    tree.notes = tree_in.notes
    db.commit()
    db.refresh(tree)
    send_log(
        user_id=current_user["id"],
        action="update",
        entity_type="Tree",
        entity_id=tree.id,
        details=f"Updated tree to type={tree.type} for client_id={tree.client_id}"
    )
    return tree

@router.delete("/{tree_id}")
async def delete_tree(
    tree_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    tree = get_tree_by_id(db, tree_id)
    if not tree:
        raise HTTPException(status_code=404, detail="Tree not found")
    await verify_client_access(tree.client_id, request)
    db.delete(tree)
    db.commit()
    send_log(
        user_id=current_user["id"],
        action="delete",
        entity_type="Tree",
        entity_id=tree_id,
        details=f"Deleted tree of type={tree.type} for client_id={tree.client_id}"
    )
    return {"detail": "Tree deleted"}
