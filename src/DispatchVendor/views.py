from typing import List,Optional
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from .models import DispatchVendorCreate,VendorListRequest,VendorListResponse,VendorUpdateRequest,VendorDeleteRequest
from .service import create,get_vendor_list_service,update_vendor_service,delete_vendor_service
from src.parameter import get_token


router = APIRouter()


@router.post("/create_dispatch_vendor")
def create_Vendor_details(
    vendor: DispatchVendorCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db),
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    else:
        return create(db=db, vendor=vendor)
        


@router.post("/dispatch_vendor_list")
def get_vendor_list(
    request: VendorListRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db),
):
    if auth_token != get_token():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized Request")
    
    vendors = get_vendor_list_service(db=db, admin_id=request.admin_id, employee_id=request.employee_id)
    
    if not vendors:
        return {
            "status":"false",
            "message":"No vendors found with the provided id",
        }
    
    return {
        "status":"true",
        "message":"Vendor list retrieved successfully",
        "data":vendors
    
    }



@router.post("/update_dispatch_vendor")
def update_vendor_details(
    request: VendorUpdateRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db),
):
    if auth_token != get_token():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized Request")
    
    return update_vendor_service(db=db, request=request)




@router.post("/delete_dispatch_vendor")
def delete_vendor_details(
    request: VendorDeleteRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db),
):
    if auth_token != get_token():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized Request")
    
    return delete_vendor_service(db=db, request=request)