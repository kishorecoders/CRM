from fastapi import APIRouter, Depends, HTTPException, Header
from sqlmodel import Session
from .models import ProjectCreate , ProjectGet ,ProjectUpdate , ProjectDelete
from .service import create_task_customer , get_task_customer , update_task_customer , delete_task_customer
from src.database import get_db
from src.parameter import get_token


router = APIRouter()


@router.post("/createproject")
def create(
    project_create: ProjectCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")


    return create_task_customer(db=db, project_create=project_create)

@router.post("/getproject")
def get(
    project_get: ProjectGet,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    return get_task_customer(db=db, project_get=project_get)


@router.post("/updateproject")
def update(
    project_update: ProjectUpdate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    
    return update_task_customer(db=db, project_update=project_update)

@router.post("/deleteproject")
def delete(
    project_delete: ProjectDelete,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")


    return delete_task_customer(db=db, project_delete=project_delete)

