from typing import List
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from src.SuperAdminEnquiry.models import SuperAdminEnquiry,SuperAdminEnquiryCreate
from src.SuperAdminEnquiry.service import create,get_all_enquiry,update
from src.parameter import get_token

router = APIRouter()

@router.get("/")
def get_all_enquiry_details(auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_all_enquiry(db=db)
    
    return inner_get_plan(auth_token)

@router.post("/")
def create_enquiry_details(super_admin_enquiry: SuperAdminEnquiryCreate,
                auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return create(db=db, super_admin_enquiry=super_admin_enquiry)
    
    return inner_get_plan(auth_token)

@router.put("/{enquiry_id}")
def update_enquiry_details(enquiry_id:int,super_admin_enquiry:SuperAdminEnquiryCreate,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db:Session=Depends(get_db)):
       def inner_get_plan(auth_token: str):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return update(enquiry_id=enquiry_id,super_admin_enquiry=super_admin_enquiry,db=db)
    
       return inner_get_plan(auth_token)