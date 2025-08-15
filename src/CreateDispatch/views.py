from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session
from src.database import get_db
from .models import CreateDispatchCreate,DispatchListRequest
from .service import create,get_dispatch_list
from src.parameter import get_token

router = APIRouter()

   
@router.post("/create_dispatch")
def create_dispatch_details(
    dispatch_create: CreateDispatchCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    
    
    response = create(db=db, dispatch_create=dispatch_create)
    return response



@router.post("/dispatch_list")
def get_dispatch_list_details(
    request: DispatchListRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    response = get_dispatch_list(db=db, request=request)
    return response
