from typing import List
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from .models import QuotationCustomerCreate,GetCustomerRequest,UpdateCustomerRequest,DeleteCustomerRequest
from .service import create,get_customers,update_customer,delete_customer
from src.parameter import get_token

router = APIRouter()


@router.post("/create_customer")
def create_customer_details(customer: QuotationCustomerCreate,
                auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return create(db=db, customer=customer)
        



@router.post("/get_customers")
def get_customer_list(request: GetCustomerRequest,
                      auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                      db: Session = Depends(get_db)):

    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    return get_customers(db=db, admin_id=request.admin_id, employe_id=request.employe_id)



@router.post("/update_customer")
def update_customer_details(request: UpdateCustomerRequest,
                            auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                            db: Session = Depends(get_db)):

    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    return update_customer(db=db, request=request)




@router.post("/delete_customer")
def delete_customer_details(request: DeleteCustomerRequest,
                            auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                            db: Session = Depends(get_db)):

    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    return delete_customer(db=db, request=request)
