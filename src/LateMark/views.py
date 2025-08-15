from typing import List
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from .models import LateMarkRead ,LateMarkCreate,LateMarkDelete ,LetmarkUpdate
from .service import get_all_latemark ,create, delete ,update
from src.parameter import get_token

router = APIRouter()

@router.post("/show_all_latemark")
def read_all_Latemark_details(
    data :LateMarkRead,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    else:
        return get_all_latemark(db=db , data = data)
        
@router.post("/addLateMark")
def create_latemark(
    latemark_create: LateMarkCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    return create(db=db, latemark_create=latemark_create)


@router.post("/deleteLateMark")
def delete_latemark(
    latemark_delete: LateMarkDelete,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    return delete(db=db, latemark_delete=latemark_delete)

@router.post("/updateLateMark")
def update_latemark(
    latemark_update: LetmarkUpdate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    return update(db=db, latemark_update=latemark_update)

