from fastapi import APIRouter, Depends, HTTPException, Header
from sqlmodel import Session
from .models import CustomerCreate , CustomerGet ,Customerupdate , CustomerDelete
from .service import create_task_customer , get_task_customer , update_task_customer , delete_task_customer
from src.database import get_db
from src.parameter import get_token



router = APIRouter()


@router.post("/createcustomer")
def create(
    task_create: CustomerCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    
    return create_task_customer(db=db, task_create=task_create)

@router.post("/getcustomer")
def get(
    customer_get: CustomerGet,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    
    return get_task_customer(db=db, customer_get=customer_get)


@router.post("/updatecustomer")
def update(
    customer_update: Customerupdate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    
    return update_task_customer(db=db, customer_update=customer_update)

@router.post("/deletecustomer")
def delete(
    customer_delete: CustomerDelete,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    
    return delete_task_customer(db=db, customer_delete=customer_delete)

