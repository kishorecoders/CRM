from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session
from src.database import get_db
from .models import IntegrationCreate
from .service import create,get_integration_by_admin_id,update,delete_integration_by_id
from src.parameter import get_token

router = APIRouter()


@router.get("/show-integration-by-admin-id/{admin_id}")
def read_integration_by_admin(admin_id:str, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    else:
        return get_integration_by_admin_id(db=db, admin_id=admin_id)


@router.post("/Create-integration")
def create_integration_details(integration_create: IntegrationCreate, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    else:
        return create(db=db, integration_create=integration_create)


@router.put("/Update-integration/{integration_id}")
def update_integration_details(integration_id: int, integration__update: IntegrationCreate, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    else:
        return update(integration_id=integration_id, integration__update=integration__update, db=db)


@router.delete("/delete-integration/{id}")
def delete_integration_details_by_id(id: int, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    else:
        return delete_integration_by_id(id=id, db=db)
