from sqlalchemy.orm import Session
from backend import models
from backend.schemas.tree import TreeCreate

def create_tree(db: Session, tree_in: TreeCreate):
    tree = models.Tree(**tree_in.model_dump())
    db.add(tree)
    db.commit()
    db.refresh(tree)
    return tree

def get_trees_for_client(db: Session, client_id: int):
    return db.query(models.Tree).filter(models.Tree.client_id == client_id).all()

def get_tree_by_id(db: Session, tree_id: int):
    return db.query(models.Tree).filter(models.Tree.id == tree_id).first()
