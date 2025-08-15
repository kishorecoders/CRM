from typing import List
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from src.SuperAdminBilling.models import SuperAdminBilling,SuperAdminBillingCreate
from src.SuperAdminBilling.service import create,get_all_billing,update
from src.parameter import get_token

router = APIRouter()

@router.get("/ShowBilling")
def get_all_billing_details(auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_all_billing(db=db)
    
    return inner_get_plan(auth_token)

@router.post("/CreateBilling")
def create_billing_details(super_admin_billing: SuperAdminBillingCreate,
                auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return create(db=db, super_admin_billing=super_admin_billing)
    
    return inner_get_plan(auth_token)

@router.put("/UpdateBilling/{billing_id}")
def update_billing_details(billing_id:int,super_admin_billing:SuperAdminBillingCreate,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db:Session=Depends(get_db)):
       def inner_get_plan(auth_token: str):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return update(billing_id=billing_id,super_admin_billing=super_admin_billing,db=db)
    
       return inner_get_plan(auth_token)