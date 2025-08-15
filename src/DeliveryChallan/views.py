from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session
from src.database import get_db
from .models import DeliveryChallanCreate,DeliveryChallanRequest,UpdateChallanRequest,updatestatus,GetDispatch
from .service import create,fetch_delivery_challans,update_challan_service,product_status,get_dispatch_complited
from src.parameter import get_token
from typing import List, Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, Header, Request

router = APIRouter()

   
@router.post("/create_delivery_challan")
def create_delivery_details(
    delivery_create: DeliveryChallanCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    
    
    response = create(db=db, delivery_create=delivery_create)
    return response


@router.post("/delivery_challans", response_model=Dict)
def get_delivery_challan_list(
    request: DeliveryChallanRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    
    challans = fetch_delivery_challans(db, request.admin_id, request.employee_id, request.date)
    
    if not challans:
        return {
            "status": "false",
            "message": "No delivery challans found",
            "data": []
        }
    
    return {
        "status": "true",
        "message": "Delivery challans retrieved successfully",
        "data": challans
    }



# @router.post("/update-delivery-challan", response_model=Dict)
# def update_delivery_challan(
#     request: UpdateChallanRequest,
#     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#     db: Session = Depends(get_db)
# ):
#     if auth_token != get_token():
#         return {"status": "false", "message": "Unauthorized Request"}

#     return update_challan_service(db, request)
@router.post("/update_delivery_challan", response_model=Dict)
def update_delivery_challan(
    request: UpdateChallanRequest,
    req: Request,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    return update_challan_service(db, request, req)


@router.post("/update_delivery_product_status")
def update_delivery_product_status(
    request: updatestatus,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    return product_status(db, request)

@router.post("/get_completed_dispatch")
def getcompleteddispatch(
    request: GetDispatch,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    return get_dispatch_complited(db, request)





