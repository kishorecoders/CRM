from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session
from src.database import get_db
from src.parameter import get_token
from .models import DesignHandoverCreate,DesignHandoverRead,DeleteDesignHandoverRequest,DesignHandover
from .service import create_design_handover,get_design_handover
from typing import List, Optional



router = APIRouter()


@router.post("/create_design_handover")
def create_handover_details(
    handover_create: DesignHandoverCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    
    response = create_design_handover(db=db, handover_create=handover_create)
    return response




@router.post("/get_design_handover")
def get_design_handover_view(
    request_data: DesignHandoverRead,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    expected_token = get_token()
    
    if auth_token != expected_token:
        return {"status": "false", "message": "Unauthorized Request", "received_token": auth_token, "expected_token": expected_token}
    
    response = get_design_handover(db, request_data)
    return response




@router.post("/delete_design_handover")
def delete_design_handover(
    request_data: DeleteDesignHandoverRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    expected_token = get_token()
    
    if auth_token != expected_token:
        return {"status": "false", "message": "Unauthorized Request"}
    
    query = db.query(DesignHandover).filter(
        DesignHandover.admin_id == request_data.admin_id,
        DesignHandover.id == request_data.design_handover_id
    )
    
    if request_data.employee_id:
        query = query.filter(DesignHandover.employee_id == request_data.employee_id)
    
    handover = query.first()
    if not handover:
        return {"status": "false", "message": "Design Handover not found"}
    
    db.delete(handover)
    db.commit()
    
    return {"status": "true", "message": "Design Handover deleted successfully"}
