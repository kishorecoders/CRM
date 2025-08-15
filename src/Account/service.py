from sqlalchemy.orm import Session
from src.Account.models import Account, AccountCreate
from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.parameter import get_current_datetime
from src.Quotation.models import Quotation

import os
import base64
import re
from datetime import datetime
import imghdr


from datetime import datetime
import pytz

from src.Quotation.models import Quotation
from decimal import Decimal
from decimal import Decimal, InvalidOperation
from src.AddPayment.models import PaymentRequest



def save_base64_file(base64_str: str, filename: str) -> str:
    """Save a Base64 file to the 'uploads' directory."""
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    file_path = os.path.join("uploads", filename)
    with open(file_path, "wb") as file:
        file.write(base64.b64decode(base64_str))

    return file_path


from src.Notifications.models import Notification
from src.AdminAddEmployee.models import AdminAddEmployee
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew


def create_account(db: Session, account: AccountCreate) -> dict:
    file_path = None

    #if not account.percent_cash or not account.percent_ac or not account.payment_type:
    if not account.payment_type:
        return {
            "status": "false",
            "message": "payment_type are required.",
        }

    quotation = db.query(Quotation).filter(Quotation.id == account.quote_id).first()
    if not quotation:
        return {
            "status": "false",
            "message": "Invalid quotation ID. No quotation found with this ID.",
        }

    try:
        total_amount = Decimal(quotation.total_amount)
        gst = Decimal(quotation.gst)
    except (ValueError, TypeError):
        return {
            "status": "false",
            "message": "Invalid data format for total_amount or gst.",
        }

    max_advance_amt = total_amount - gst



    try:
        advance_amt = Decimal(account.adavnce_amt)
    except (InvalidOperation, ValueError) as e:
        # Handle invalid conversion (log it, raise a custom error, etc.)
        advance_amt = Decimal(0)  # Default value, or handle it according to your needs


    if advance_amt > max_advance_amt:
        return {
            "status": "false",
            "message": f"Advance amount cannot exceed {max_advance_amt}.",
        }

    advance_cash = Decimal(0)
    advance_account = Decimal(0)
    
    if account.payment_type.lower() == "cash":
        advance_cash = advance_amt
    elif account.payment_type.lower() == "on account":
        advance_account = advance_amt
    else:
        return {
            "status": "false",
            "message": "Invalid payment_type. Must be 'Cash' or 'Account'.",
        }




    if quotation.status == 0:

        quotation.status = 1
        quotation.quotation_status = 4
        db.add(quotation)
        db.commit()
        db.refresh(quotation)

        #if account.file_data:
        #    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
        #    filename = f"{current_datetime}_account_{account.admin_id}.pdf"
        #    file_path = save_base64_file(account.file_data, filename)

        if account.file_path:
            current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
            file_extension = "pdf" if account.file_type == "pdf" else "jpg"
            filename = f"{current_datetime}_account_{account.admin_id}.{file_extension}"
            file_path = save_base64_file(account.file_path, filename)
        else:
            file_path = "" 
            
        db_account = Account(
            admin_id=account.admin_id,
            employee_id=account.employee_id,
            note=account.note,
            quote_id=account.quote_id,  
            file_path=file_path,
            percent_cash=account.percent_cash,
            percent_ac=account.percent_ac,
            adavnce_amt=account.adavnce_amt,
            advance_cash=advance_cash,
            advance_account=advance_account,
            payment_type = account.payment_type,
            adv = account.adavnce_amt,
            acc_status = 1,
            
            rcvd_amt=account.rcvd_amt,
            sent_by=account.sent_by,
            handover_name=account.handover_name,
            payment_date=account.payment_date,
            bank_name=account.bank_name,
            account_holder_name=account.account_holder_name,
            branch_name=account.branch_name,
            ifsc_code=account.ifsc_code,
            ac_no=account.ac_no,
            gst=account.gst,
            payment_method_type=account.payment_method_type,
            cheque_no=account.cheque_no,
            cheque_date=account.cheque_date,
            cheque_image=account.cheque_image,
            upi_number_or_id=account.upi_number_or_id,
            transaction_upi_id=account.transaction_upi_id,
            upi_image=account.upi_image,
            file_path2=account.file_path2


        )
        db.add(db_account)
        db.commit()
        #db.refresh(db_account)

        db_payment = PaymentRequest(
            account_id = db_account.id,
            admin_id = account.admin_id,
            emp_id = account.employee_id,
            rcvd_amt = account.adavnce_amt,
            payment_type = account.payment_type,
            file_path = file_path,
            note = account.note,
            
            sent_by=account.sent_by,
            handover_name=account.handover_name,
            payment_date=account.payment_date,
            bank_name=account.bank_name,
            account_holder_name=account.account_holder_name,
            branch_name=account.branch_name,
            ifsc_code=account.ifsc_code,
            ac_no=account.ac_no,
            gst=account.gst,
            payment_method_type=account.payment_method_type,
            cheque_no=account.cheque_no,
            cheque_date=account.cheque_date,
            cheque_image=account.cheque_image,
            upi_number_or_id=account.upi_number_or_id,
            transaction_upi_id=account.transaction_upi_id,
            upi_image=account.upi_image,
        ) 
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
        
        
        quotation = db.query(Quotation).filter(Quotation.id == account.quote_id).first()
        if quotation:
            quotation.account_status = "1"

        quotation.pi_number = account.pi_number
        quotation.po_number = account.po_number
        quotation.pi_series = account.pi_series
        quotation.pi_date = datetime.now(pytz.timezone("Asia/Kolkata"))
        db.add(quotation)

        db.commit()
        db.refresh(db_account)

        empname = None
        if db_account.employee_id:
            empname = db.query(AdminAddEmployee.employe_name).filter(AdminAddEmployee.id == db_account.employee_id).first()
        else:
            empname = db.query(SuperAdminUserAddNew.full_name).filter(SuperAdminUserAddNew.id == db_account.admin_id).first()
        # Create notification for the admin
        notification = Notification( 
            admin_id=db_account.admin_id,
            title="New Account Created",
            description=f"A new Account has been created by {empname}.",
            type="Account",
            object_id=str(db_account.id),
            created_by_id= db_account.employee_id if db_account.employee_id not in [None , ""] else db_account.admin_id,
            created_by_type="employee" if db_account.employee_id not in [None , ""] else "admin",
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)

        return {
            "status": "true",
            "message": "New account created successfully for this quotation.",
            "data": db_account
        }

    else:
        existing_account = db.query(Account).filter(Account.quote_id == account.quote_id).first()
        
        if existing_account:
            return {
                "status": "false",
                "message": "Account already exists for this quotation ID.",
            }

    #if account.file_data:
    #    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    #    filename = f"{current_datetime}_account_{account.admin_id}.pdf"
    #    file_path = save_base64_file(account.file_data, filename)


    if account.file_path:
        current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
        file_extension = "pdf" if account.file_type == "pdf" else "jpg"
        filename = f"{current_datetime}_account_{account.admin_id}.{file_extension}"
        file_path = save_base64_file(account.file_path, filename)
    else:
        file_path = ""
        
    db_account = Account(
        admin_id=account.admin_id,
        employee_id=account.employee_id,
        note=account.note,
        quote_id=account.quote_id,
        file_path=file_path,
        percent_cash=account.percent_cash,
        percent_ac=account.percent_ac,
        adavnce_amt=account.adavnce_amt,
        advance_cash=advance_cash,
        advance_account=advance_account,
        payment_type = account.payment_type,
        adv = account.adavnce_amt,
        acc_status = 1,
        
        rcvd_amt=account.rcvd_amt,
        sent_by=account.sent_by,
        handover_name=account.handover_name,
        payment_date=account.payment_date,
        bank_name=account.bank_name,
        account_holder_name=account.account_holder_name,
        branch_name=account.branch_name,
        ifsc_code=account.ifsc_code,
        ac_no=account.ac_no,
        gst=account.gst,
        payment_method_type=account.payment_method_type,
        cheque_no=account.cheque_no,
        cheque_date=account.cheque_date,
        cheque_image=account.cheque_image,
        upi_number_or_id=account.upi_number_or_id,
        transaction_upi_id=account.transaction_upi_id,
        upi_image=account.upi_image,
        file_path2=account.file_path2

    )

    db.add(db_account)
    db.commit()
    #db.refresh(db_account)

    db_payment = PaymentRequest(
        account_id = db_account.id,
        admin_id = account.admin_id,
        emp_id = account.employee_id,
        rcvd_amt = account.adavnce_amt,
        payment_type = account.payment_type,
        file_path = file_path,
        note = account.note,
        
        sent_by=account.sent_by,
        handover_name=account.handover_name,
        payment_date=account.payment_date,
        bank_name=account.bank_name,
        account_holder_name=account.account_holder_name,
        branch_name=account.branch_name,
        ifsc_code=account.ifsc_code,
        ac_no=account.ac_no,
        gst=account.gst,
        payment_method_type=account.payment_method_type,
        cheque_no=account.cheque_no,
        cheque_date=account.cheque_date,
        cheque_image=account.cheque_image,
        upi_number_or_id=account.upi_number_or_id,
        transaction_upi_id=account.transaction_upi_id,
        upi_image=account.upi_image,
    ) 
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)


    #db.add(db_account)
    
    quotation = db.query(Quotation).filter(Quotation.id == account.quote_id).first()
    if quotation:
        quotation.account_status = "1"

    quotation.pi_number = account.pi_number
    quotation.po_number = account.po_number
    quotation.pi_series = account.pi_series
    quotation.status = 1  
    quotation.quotation_status = 4
    quotation.pi_date = datetime.now(pytz.timezone("Asia/Kolkata"))
    db.add(quotation)

    db.commit()
    db.refresh(db_account)

    empname = None
    if db_account.employee_id:
        empname = db.query(AdminAddEmployee.employe_name).filter(AdminAddEmployee.id == db_account.employee_id).first()
    else:
        empname = db.query(SuperAdminUserAddNew.full_name).filter(SuperAdminUserAddNew.id == db_account.admin_id).first()
    # Create notification for the admin
    notification = Notification(
        admin_id=db_account.admin_id,
        title="New Account Created",
        description=f"A new Account has been created by {empname}.",
        type="Account",
        object_id=str(db_account.id),
        created_by_id= db_account.employee_id if db_account.employee_id not in [None , ""] else db_account.admin_id,
        created_by_type="employee" if db_account.employee_id not in [None , ""] else "admin",
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)

    return {
        "status": "true",
        "message": "Account created successfully.",
        "data": db_account
    }
















    
# def create_account(db: Session, account: AccountCreate) -> dict:
#     """Create an account, link to quotation, and update quotation details."""
#     file_path = None

#     if account.file_data:  
#         current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
#         filename = f"{current_datetime}_account_{account.admin_id}"  
#         file_path = save_base64_file(account.file_data, filename)

#     # Create Account Entry
#     db_account = Account(
#         admin_id=account.admin_id,
#         employee_id=account.employee_id,
#         note=account.note,
#         quote_id=account.quote_id,
#         file_path=file_path,
#         po_number=account.po_number,
#         pi_number=account.pi_number
#     )

#     db.add(db_account)

#     # Fetch and Update Quotation if quote_id exists
#     quotation = db.query(Quotation).filter(Quotation.id == account.quote_id).first()
#     if quotation:
#         quotation.pi_number = account.pi_number
#         quotation.po_number = account.po_number
#         quotation.pi_date = datetime.now(pytz.timezone("Asia/Kolkata"))
#         db.add(quotation)

#     db.commit()
#     db.refresh(db_account)

#     return {
#         "status": "true",
#         "message": "Account created successfully",
#         "data": db_account
#     }






