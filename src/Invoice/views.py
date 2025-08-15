from typing import List
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from src.Invoice.models import Invoice,InvoiceCreate
from src.Invoice.service import create,get_all_invoice,get_invoice_by_admin_id,update,delete_invoice
from src.parameter import get_token

router = APIRouter()

@router.get("/showAllInvoice")
def get_all_invoice_details(auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
           return {"status": "false", "message": "Unauthorized Request"}
        else:
           return get_all_invoice(db=db)
    
    return inner_get_plan(auth_token)

@router.post("/createInvoice")
def create_invoice_details(invoice_create: InvoiceCreate,
                auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return create(db=db, invoice_create=invoice_create)
    
    return inner_get_plan(auth_token)

@router.get("/showInvoiceByAdmin/{admin_id}/{lead_id}")
def read_invoice_by_admin_id(admin_id:str, lead_id:str, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_invoice_by_admin_id(admin_id=admin_id, lead_id=lead_id, db=db)
    
    return inner_get_plan(auth_token)
     
@router.put("/updateInvoice/{invoice_id}")
def update_invoice_details(invoice_id:int,invoice:InvoiceCreate,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db:Session=Depends(get_db)):
       def inner_get_plan(auth_token: str):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return update(invoice_id=invoice_id,invoice=invoice,db=db)
    
       return inner_get_plan(auth_token)

@router.delete("/deleteInvoice/{invoice_id}")
def delete_invoice_details(invoice_id: int, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
  def inner_get_plan(auth_token: str):
    if auth_token != get_token():
     return {"status": "false", "message": "Unauthorized Request"}
    else:
     return delete_invoice(invoice_id=invoice_id, db=db)
    
  return inner_get_plan(auth_token)