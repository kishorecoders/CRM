from typing import List
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from .models import Bank,BankCreate,BankListRequest,BankUpdateRequest,BankDeleteRequest
from .service import create,get_bank_list
from src.parameter import get_token
from sqlmodel import Session, select
from sqlalchemy import select, update


router = APIRouter()



@router.post("/create_bank")
def create_Vendor_details(bank: BankCreate,
                auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return create(db=db, bank=bank)
        




@router.post("/get_bank_list")
def get_series_details(
    request: BankListRequest,  
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
   
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    
   
    bank_list = get_bank_list(db=db, admin_id=request.admin_id, employee_id=request.employee_id)

    return {
        "status": "true",
        "message": "Bank List Retrieved Successfully",
        "data": bank_list
    }
    
    
    
    

# @router.post("/update_bank")
# def update_bank(
#     request: BankUpdateRequest,
#     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#     db: Session = Depends(get_db)
# ):
#     if auth_token != get_token():
#         return {"status": "false", "message": "Unauthorized Request"}
    
#     bank = db.exec(select(Bank).where(Bank.id == request.id, Bank.admin_id == request.admin_id)).first()
#     if not bank:
#         return {"status": "false", "message": "Bank record not found"}
    
#     bank.employee_id = request.employee_id if request.employee_id is not None else bank.employee_id
#     bank.bank_name = request.bank_name if request.bank_name is not None else bank.bank_name
#     bank.branch = request.branch if request.branch is not None else bank.branch
#     bank.account_number = request.account_number if request.account_number is not None else bank.account_number
#     bank.ifsc_code = request.ifsc_code if request.ifsc_code is not None else bank.ifsc_code
#     #bank.is_default = request.is_default if request.is_default is not None else bank.is_default
    
#     db.add(bank)
#     db.commit()
#     db.refresh(bank)
    
#     return {"status": "true", "message": "Bank details updated successfully", "data": bank}



@router.post("/update_bank")
def update_bank(
    request: BankUpdateRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    
    bank = db.query(Bank).filter(Bank.id == request.id, Bank.admin_id == request.admin_id).first()

    if not bank:
        return {"status": "false", "message": "Bank record not found"}
    
    bank.employee_id = request.employee_id if request.employee_id is not None else bank.employee_id
    bank.bank_name = request.bank_name if request.bank_name is not None else bank.bank_name
    bank.account_holder_name =  request.account_holder_name if request.account_holder_name is not None else bank.account_holder_name
    bank.branch = request.branch if request.branch is not None else bank.branch
    bank.account_number = request.account_number if request.account_number is not None else bank.account_number
    bank.ifsc_code = request.ifsc_code if request.ifsc_code is not None else bank.ifsc_code

    if request.is_default == "true":
        db.execute(
            update(Bank)
            .where(Bank.admin_id == bank.admin_id)
            .values(is_default=False)
        )
        db.commit()  
        bank.is_default = True
    elif request.is_default == "false":
        bank.is_default = False  
    
    db.add(bank)
    db.commit()
    db.refresh(bank)
    
    return {"status": "true", "message": "Bank details updated successfully", "data": bank}


# @router.post("/delete_bank")
# def delete_bank(
#     request: BankDeleteRequest,
#     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#     db: Session = Depends(get_db)
# ):
#     if auth_token != get_token():
#         return {"status": "false", "message": "Unauthorized Request"}
    
#     bank = db.exec(select(Bank).where(Bank.id == request.id, Bank.admin_id == request.admin_id)).first()
#     if not bank:
#         return {"status": "false", "message": "Bank record not found"}
    
#     db.delete(bank)
#     db.commit()
    
#     return {"status": "true", "message": "Bank details deleted successfully"}





@router.post("/delete_bank")
def delete_bank(
    request: BankDeleteRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    
    bank = db.query(Bank).filter(Bank.id == request.id, Bank.admin_id == request.admin_id).first()
    if not bank:
        return {"status": "false", "message": "Bank record not found"}
    
    if bank.is_default:
        last_bank = db.query(Bank).filter(Bank.id != request.id).order_by(Bank.created_at.desc()).first()
        
        if last_bank:
            if not last_bank.is_default:
                last_bank.is_default = True
                db.commit()
            else:
                return {"status": "false", "message": "No new default bank to assign"}
        else:
            return {"status": "false", "message": "No banks available to assign as default"}
    
    db.delete(bank)
    db.commit()
    
    return {"status": "true", "message": "Bank details deleted successfully"}








