from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status,HTTPException
from .models import Bank,BankCreate
from sqlmodel import Session, select
from sqlalchemy import select, update





# def create(db: Session, bank: BankCreate):
#     existing_bank = db.exec(
#         select(Bank).where(
#             Bank.admin_id == bank.admin_id,
#             Bank.account_number == bank.account_number
#         )
#     ).first()

#     if existing_bank:
#         return {'status': 'false', 'message': "Account number already exists for this Admin"}

    
#     db_bank = Bank(**bank.dict())
#     db.add(db_bank)
#     db.commit()
#     db.refresh(db_bank)
    
#     response = {'status': 'true', 'message': "Bank Detail Added Successfully", 'data': db_bank}
#     return response



def create(db: Session, bank: BankCreate):
    if bank.is_default is None:
        return {'status': 'false', 'message': "Please specify whether this account should be set as default (true/false)."}

    existing_bank = db.execute(
        select(Bank).where(
            Bank.admin_id == bank.admin_id,
            Bank.account_number == bank.account_number
        )
    ).scalar_one_or_none()

    if existing_bank:
        return {'status': 'false', 'message': "Account number already exists for this Admin"}

    if bank.is_default:
        db.execute(
            update(Bank)
            .where(Bank.admin_id == bank.admin_id)
            .values(is_default=False)
        )

    db_bank = Bank(**bank.dict())
    db.add(db_bank)
    db.commit()
    db.refresh(db_bank)

    return {'status': 'true', 'message': "Bank Detail Added Successfully", 'data': db_bank}




# def get_bank_list(db: Session, admin_id: str, employee_id: Optional[str] = None):
    
    
#     query = select(Bank).where(Bank.admin_id == admin_id)
    
#     if employee_id:
#         query = query.where(Bank.employee_id == employee_id)
    
#     query = query.order_by(Bank.id.desc())

#     bank_list = db.exec(query).all()
#     return bank_list


def get_bank_list(db: Session, admin_id: str, employee_id: Optional[str] = None):
    query = select(Bank).where(Bank.admin_id == admin_id)
    
    if employee_id:
        query = query.where(Bank.employee_id == employee_id)
    
    query = query.order_by(Bank.id.desc())

    bank_list = db.execute(query).scalars().all()
    return bank_list



