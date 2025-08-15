from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from src.Quotation.models import Quotation,QuotationCreate,Quotationupdate,CreateInvoiceRequest ,QuotationApprove, Convertorder
from src.Quotation.service import create,get_all_quotation,get_quotation_by_admin_id,update_quotation,delete_quotation,convert_order
from src.parameter import get_token
from src.QuotationProductEmployee.models import QuotationProductEmployee,QuotationProductEmployeeCreateList
from sqlmodel import select
from src.Account.models import Account
import os
import base64
import re
from datetime import datetime
import imghdr

router = APIRouter()

@router.get("/showAllQuotation")
def get_all_quotation_details(auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
           return {"status": "false", "message": "Unauthorized Request"}
        else:
           return get_all_quotation(db=db)
    
    return inner_get_plan(auth_token)


# @router.post("/createQuotation")
# def create_quotation_details(
#     quotation_create: QuotationCreate,
#     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#     db: Session = Depends(get_db)
# ):
    
#     if auth_token != get_token():
#         return {"status": "false", "message": "Unauthorized Request"}

    
#     return create(db=db, quotation_create=quotation_create)





def save_base64_file(base64_str: str, filename: str) -> str:
    """Save a Base64 file to the 'uploads' directory."""
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    file_path = os.path.join("uploads", filename)
    with open(file_path, "wb") as file:
        file.write(base64.b64decode(base64_str))

    return file_path


@router.post("/createQuotation")
def create_quotation_details(
    quotation_create: QuotationCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    return create(db=db, quotation_create=quotation_create)



    
    
@router.get("/showQuotationByAdmin/{admin_id}")
def read_quotation_by_admin_id(
    admin_id: str, 
    emp_id: Optional[str] = None, 
    from_admin_id: Optional[str] = None,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    quote_id: Optional[int] = None,
    month_year: Optional[str] = None ,
    quotation_status: Optional[int] = None ,
    page: Optional[int] = 1, 
    page_size: Optional[int] = 10,
    status_filter: Optional[str] = None,
    date_filter:Optional[str] = None,
    db: Session = Depends(get_db)
):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_quotation_by_admin_id(admin_id=admin_id, emp_id=emp_id, 
                                             db=db, quote_id=quote_id,status_filter=status_filter,
                                             date_filter=date_filter, page=page, page_size=page_size,
                                             quotation_status= quotation_status , month_year = month_year,
                                             from_admin_id = from_admin_id)

    return inner_get_plan(auth_token)

    
@router.put("/updateQuotation/{quotation_id}")
def update_quotation_details(
    quotation_id: int,
    quotation: Quotationupdate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db),
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    return update_quotation(quotation_id=quotation_id, quotation=quotation, db=db)


@router.delete("/deleteQuotation/{quotation_id}")
def delete_quotation_details(
    quotation_id: int,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db),
):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return delete_quotation(quotation_id=quotation_id, db=db)
    
    return inner_get_plan(auth_token)
    

@router.post("/create_invoice_number")
def update_invoice_number(
    request: CreateInvoiceRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    
    quotation = db.exec(
        select(Quotation).where(
            Quotation.admin_id == request.admin_id,
            Quotation.id == request.quote_id
        )
    ).first()

    
    if not quotation:
        return {"status": "false", "message": "Quotation not found"}

    
    quotation.invoice_number = request.invoice_number
    db.add(quotation)
    db.commit()
    db.refresh(quotation)

    return {
        "status": "true",
        "message": "Invoice number updated successfully",
        "data": quotation
    }
    

@router.post("/quotation_status_approve")
def approve_quotation(
    request: QuotationApprove,

    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {
            "status": "false",
            "message": "Unauthorized Request",
            }

    account = db.query(Account).filter(Account.id == request.account_id).first()
    if not account:
        return {
            "status": "false",
            "message": "Account not found",
            }

    quotation = db.query(Quotation).filter(Quotation.id == account.quote_id).first()
    if not quotation:
        return {
            "status": "false",
            "message": "Quotation not found for this account",
            }

    if request.quotation_status not in [2, 3]:
        return {
            "status": "false",
            "message": "Invalid status. Use 2 for Rejected, or 3 for Converted.",
            }

    # ? Update quotation status
    quotation.quotation_status = request.quotation_status

    db.commit()
    db.refresh(quotation)

    return {
        "status": "true",
        "message": f"Quotation  successfully",
        "data": {
            "id": quotation.id,
            "status": quotation.quotation_status,
            "data": quotation.dict()
        }
    }


from src.Account.models import Account

@router.post("/quotation_status_approve")
def approve_quotation(
    request: QuotationApprove,

    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    # ? Authentication check
    if auth_token != get_token():
        return {
            "status": "false",
            "message": "Unauthorized Request",
            }

    account = db.query(Account).filter(Account.id == request.account_id).first()
    if not account:
        return {
            "status": "false",
            "message": "Account not found",
            }

    quotation = db.query(Quotation).filter(Quotation.id == account.quote_id).first()
    if not quotation:
        return {
            "status": "false",
            "message": "Quotation not found for this account",
            }

    if request.quotation_status not in [2, 3]:
        return {
            "status": "false",
            "message": "Invalid status. Use 2 for Rejected, or 3 for Converted.",
            }

    # ? Update quotation status
    quotation.quotation_status = request.quotation_status

    db.commit()
    db.refresh(quotation)

    return {
        "status": "true",
        "message": f"Quotation status upadated successfully",
    }

@router.post("/convertorder")
def update_admin_sales_details(
    admin_sales: Convertorder,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    
    return convert_order(admin_sales_data=admin_sales, db=db)




