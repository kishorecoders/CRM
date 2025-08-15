from .models import SuperAdminUserAddNew, SuperAdminUserAddNewCreate, SuperAdminUserAddNewUpdate, UpdatePassword, PromptType, PromptTypeCreate
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime, timedelta
from fastapi import status, HTTPException
from src.SuperAdminPlanAndPrice.models import SuperAdminPlanAndPrice
from src.AdminAddEmployee.models import AdminAddEmployee
import string
import random
from sqlalchemy import or_
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64
from fastapi.responses import RedirectResponse
import pytz
from sqlalchemy import func
from src.Settings.models import Setting
from src.SuperAdminBilling.models import SuperAdminBilling


from src.email_service import send_welcome_email,send_status_update_email
import asyncio



def get_all_users(db: Session, search: Optional[str] = None, filter: Optional[str] = None, is_deleted: Optional[bool] = None):
    user_query = db.query(SuperAdminUserAddNew)

    if is_deleted is not None:  
        user_query = user_query.filter(SuperAdminUserAddNew.is_deleted == is_deleted)

    if search is not None:
        search_term = f"%{search}%"
        user_query = user_query.filter(
            or_(
                SuperAdminUserAddNew.full_name.ilike(search_term),
                SuperAdminUserAddNew.email.ilike(search_term),
            )
        )

    current_datetime = datetime.now()

    if filter == 'plan':
        user_query = user_query.filter(SuperAdminUserAddNew.plan_id != 0)  
        
    elif filter == 'demo':
        user_query = user_query.filter(
            SuperAdminUserAddNew.expiry_date >= current_datetime,
            SuperAdminUserAddNew.demo_period_day != 0
        )
        
    elif filter == 'expired':
        user_query = user_query.filter(SuperAdminUserAddNew.expiry_date <= current_datetime)
        
    elif filter == 'active':
        user_query = user_query.filter(
            SuperAdminUserAddNew.expiry_date >= current_datetime,
            SuperAdminUserAddNew.amount != 0 
        )

    # Fetch users and their employee counts
    subquery = (
        db.query(AdminAddEmployee.admin_id, func.count(AdminAddEmployee.id).label("employee_count"))
        .group_by(AdminAddEmployee.admin_id)
        .subquery()
    )

    users = (
        user_query.outerjoin(subquery, SuperAdminUserAddNew.id == subquery.c.admin_id)
        .with_entities(SuperAdminUserAddNew, subquery.c.employee_count)
        .order_by(SuperAdminUserAddNew.id.desc())
        .all()
    )

    ist = pytz.timezone('Asia/Kolkata')
    formatted_users = []
    for user, employee_count in users:
        user_data = user.__dict__.copy()  
        if user.created_at:
            user_data['created_at'] = user.created_at.astimezone(ist).strftime('%Y-%m-%dT%H:%M:%S.%f')
        if user.updated_at:
            user_data['updated_at'] = user.updated_at.astimezone(ist).strftime('%Y-%m-%dT%H:%M:%S.%f')
        user_data['employee_count'] = employee_count or 0  # Default to 0 if None
        formatted_users.append(user_data)

    response = {'status': 'true', 'message': "Data Received Successfully", 'data': formatted_users}
    return response



def generate_character(length=5):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return ''.join(random.choice(characters) for _ in range(length))


import hashlib
import random
import string
import time
from datetime import datetime

def generate_transaction_id(admin_id: int, plan_id: int) -> str:
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')  # e.g., 20250716124359
    base_str = f"{admin_id}-{plan_id}-{time.time()}"
    hash_part = hashlib.sha1(base_str.encode()).hexdigest().upper()[:6]  # Short unique hash
    txn_id = f"TXN-A{admin_id}P{plan_id}-{timestamp}-{hash_part}"
    return txn_id


def create(db: Session, super_admin_user_add_new: SuperAdminUserAddNewCreate):
    email = super_admin_user_add_new.email
    phone = super_admin_user_add_new.phone_number
    input_password = super_admin_user_add_new.password
    input_confirm_password = super_admin_user_add_new.confirm_password
    # gst_number = super_admin_user_add_new.gst_number


    
    existing_email_employee = db.query(AdminAddEmployee).filter(
        AdminAddEmployee.employe_email_id == email
    ).first()

    
    existing_email_admin = db.query(SuperAdminUserAddNew).filter(
        SuperAdminUserAddNew.email == email
    ).first()

    if email and (existing_email_employee or existing_email_admin):
        return {"status": "false", "message": "Email is already registered. Please use a different email."}

    
    existing_phone_employee = db.query(AdminAddEmployee).filter(
        AdminAddEmployee.employe_phone_number == phone
    ).first()

    
    existing_phone_admin = db.query(SuperAdminUserAddNew).filter(
        SuperAdminUserAddNew.phone_number == phone
    ).first()

    if phone and (existing_phone_employee or existing_phone_admin):
        return {"status": "false", "message": "Phone number is already registered. Please use a different phone number."}
        

    # if gst_number and db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.gst_number == gst_number).first():
    #     return {'status': 'false', 'message': "Gst Number is already registered. Try another Gst Number"}

    
    newform = SuperAdminUserAddNew(**super_admin_user_add_new.dict())

    
    if newform.demo_period_day:
        newform.expiry_date = newform.created_at + timedelta(days=newform.demo_period_day)
    else:
        subscription_plan = db.query(SuperAdminPlanAndPrice).filter(SuperAdminPlanAndPrice.id == newform.plan_id).first()
        if subscription_plan:
            if newform.amount == subscription_plan.one_month_price:
                newform.expiry_date = newform.created_at + timedelta(days=30)
            elif newform.amount == subscription_plan.three_month_price:
                newform.expiry_date = newform.created_at + timedelta(days=90)
            elif newform.amount == subscription_plan.twelve_month_price:
                newform.expiry_date = newform.created_at + timedelta(days=365)

    db.add(newform)
    db.commit()
    db.refresh(newform)

    
    db.flush()
  

   
    if input_password:
        newform.password = input_password
        newform.confirm_password = input_confirm_password or input_password
    else:
        company_code = newform.company_name[:5]
        unique_character = generate_character()
        generated_password = f'{company_code}_{newform.id}_{unique_character}'
        newform.password = generated_password
        newform.confirm_password = generated_password

    db.commit()

    
    try:
        new_setting = Setting(
            admin_id=str(newform.id),
            employe_id="",
            company_title=newform.company_name,
            gst_number="",
            state="",
            logo="",
            address="",
            account_holder_name="xx",
            account_number="xx",
            ifsc_code="xx",
            trems_condition="xx",
            custom_series="",
            bank_name="xx",
            branch="xx",
            email=newform.email,
            contact_number=str(newform.phone_number),
            

        )
        db.add(new_setting)
        db.commit()
        db.refresh(new_setting)
        
        
        #asyncio.run(send_welcome_email(newform.email, newform.full_name, newform))

        teansection_id = generate_transaction_id(admin_id=newform.id , plan_id= newform.plan_id)

        bill = SuperAdminBilling(
            user_add_new_id = newform.id,
            transection_id = teansection_id,
            reffral_code_id = 0,
            gst_number = newform.gst_number,
            address = "",
            city = "",
            state = newform.state,
            pin_code = "",
            country = "India",
            amount_of_transection = newform.amount
        )
        db.add(bill)
        db.commit()
        db.refresh(bill)        

        
    except Exception as e:
        db.rollback()
        
        return {'status': 'false', 'message': "Failed to create setting record","error": f"[ERROR] Failed to create setting: {e}"}

    return {
        'status': 'true',
        'message': "Super Admin User Add New Form Details Added Successfully",
        'data': newform.id
    }




def get_user_by_id(admin_id: int, db: Session):
    data = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == admin_id).all()
    dataArray = []
    for item in data:
        plan_details = db.query(SuperAdminPlanAndPrice).filter(SuperAdminPlanAndPrice.id == item.plan_id).all()

        temp = {
            'user_details': item,
            'plan_details': plan_details
        }
        dataArray.append(temp)
    response = {'status': 'true', 'message': "Data Recived Successfully", 'data': dataArray}
    return response


# def update(admin_id:int,super_admin_user_add_new:SuperAdminUserAddNewCreate,db:Session):
#     super_admin_user_add_new_update = super_admin_user_add_new.dict(exclude_unset=True)
#     db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == admin_id).update(super_admin_user_add_new_update)
#     db.commit()
#     response = {'status': status.HTTP_200_OK,'message':"Data Updated Successfully",'data':super_admin_user_add_new_update}
#     return response


def update(db: Session, admin_id: int, updated_data: SuperAdminUserAddNewUpdate):
    db_user = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == admin_id).first()

    if not db_user:
       return {'status': 'false', 'message': 'User not found'}

    
    for field, value in updated_data.dict(exclude_unset=True).items():
        setattr(db_user, field, value)

    
    if updated_data.plan_id:
       
        subscription_plan = db.query(SuperAdminPlanAndPrice).filter(
            SuperAdminPlanAndPrice.id == updated_data.plan_id).first()

        if subscription_plan:
           
            if db_user.amount == subscription_plan.one_month_price:
                db_user.expiry_date = datetime.now() + timedelta(days=30)
            elif db_user.amount == subscription_plan.three_month_price:
                db_user.expiry_date = datetime.now() + timedelta(days=90)
            elif db_user.amount == subscription_plan.twelve_month_price:
                db_user.expiry_date = datetime.now() + timedelta(days=365)

    elif updated_data.demo_period_day:
        
        db_user.expiry_date = datetime.now() + timedelta(days=updated_data.demo_period_day)

   
    if updated_data.expiry_date == 0:
        db_user.expiry_date = None  

   
    db_user.updated_at = datetime.now()

    db.commit()
    db.refresh(db_user)

    response = {
        'status': 'true',
        'message': 'Super Admin User Add New Form Details Updated Successfully',
        'data': db_user
    }

    return response


def user_by_user_id(admin_id: int, db: Session):
    data = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == admin_id).order_by(
        SuperAdminUserAddNew.id.asc()).all()
    response = {'status': 'true', 'message': "Data Recived Successfully", 'data': data}
    return response

# def update_password(admin_id: int, password_data: UpdatePassword, db: Session):
#     # Fetch main part data
#     admin_data = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == admin_id).first()

#     if not admin_data:
#         return {"status": 'false', 'message': "Admin not found"}

#     # Update part_ordered value in main part
#     admin_data.password = password_data.password
#     admin_data.confirm_password = password_data.password
#     admin_data.updated_at = datetime.now()
    
#     # Commit changes to the database
#     db.commit()

#     return {
#         'status': 'true',
#         'message': "Password Update Successfully"
#     }

def invalidate_token(token: str, db: Session):
    # Implement logic to invalidate token, for example, deleting it from the database
    # This depends on how tokens are managed in your application
    pass

def update_password(admin_id: int, password_data: UpdatePassword, db: Session):
    admin_data = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == admin_id).first()
    if not admin_data:
        {"status": "false", "message": "Admin not found"}

    admin_data.password = password_data.password
    admin_data.confirm_password = password_data.password
    admin_data.updated_at = datetime.now()
    db.commit()
    

def send_reset_email(email: str, db: Session):
    admin_data = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.email == email).first()
    if not admin_data:
        return {"status": "false", "message": "Email not found"}

    token = base64.urlsafe_b64encode(f"{admin_data.id}:{datetime.now().timestamp()}".encode()).decode()
    reset_link = f"https://api.entraguru.in/v1/SuperAdminUserAddNew/reset-password?token={token}"

    # sender_email = "password@sphurit.com"
    # sender_password = "Modi@123456"
    # smtp_server = "mail.sphurit.com"
    # smtp_port = 465
    sender_email = "anantkaaldeveloper@gmail.com"
    username = "7560cc001@smtp-brevo.com"
    sender_password = "tY41hIz3s08jdHxn"
    smtp_server = "smtp-relay.brevo.com"
    smtp_port = 587
    receiver_email = email
    subject = "Password Reset Request"
    body = f"Click the link to reset your password: {reset_link}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.login(username, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "true", "message": "Password reset link sent successfully"}

def verify_token(token: str, db: Session):
    try:
        decoded = base64.urlsafe_b64decode(token).decode().split(':')
        admin_id = int(decoded[0])
        
        return admin_id
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid token")



def create_prompt_type(db: Session, prompt_type_create: PromptTypeCreate):
    
    existing_prompt_type = db.query(PromptType).filter(PromptType.id == "1").first()
    
    if existing_prompt_type:
        
        for key, value in prompt_type_create.dict().items():
            setattr(existing_prompt_type, key, value)
        existing_prompt_type.updated_at = datetime.now()    
        db.commit()
        db.refresh(existing_prompt_type)
        response = {'status': 'true', 'message': 'Prompt Type Details Updated Successfully', 'data': existing_prompt_type}
        return response
    else:
       
        db_prompt_type_create = PromptType(**prompt_type_create.dict())
        db.add(db_prompt_type_create)
        db.commit()
        db.refresh(db_prompt_type_create)
        response = {'status': 'true', 'message': 'Prompt Type Details Added Successfully', 'data': db_prompt_type_create}
        return response
    
def get_prompt_type(db:Session):
    data = db.query(PromptType).order_by(PromptType.id.desc()).all()
    response = {'status': 'true','message':"Data Recived Successfully",'data':data}
    return response    


# def delete_superadmin_user_by_id(admin_id: int, db: Session):
    
#     admin = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == admin_id).first()
    
#     if admin:
        
#         admin.is_deleted = True
#         admin.deleted_date = datetime.utcnow()
#         db.add(admin)
#         db.commit()
        
        
#         return {
#             'status': 'true',
#             'message': "Super Admin user marked as deleted successfully",
#             'data': {
#                 'id': admin.id,
#                 'is_deleted': admin.is_deleted,
#                 'deleted_date': admin.deleted_date
#             }
#         }
    
#     return {"status": 'false', 'message': "User not found"}
def delete_superadmin_user_by_id(admin_id: int, db: Session):
    
    admin = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == admin_id).first()
    
    if not admin:
        return {"status": 'false', 'message': "User not found"}
    
    
    if admin.is_active:
        return {"status": 'false', 'message': "User is currently active. Please deactivate the user first."}
    
    
    admin.is_deleted = True
    admin.deleted_date = datetime.utcnow()
    db.add(admin)
    db.commit()
    
    return {
        'status': 'true',
        'message': "Super Admin user marked as deleted successfully",
        'data': {
            'id': admin.id,
            'is_deleted': admin.is_deleted,
            'deleted_date': admin.deleted_date
        }
    }



def revert_superadmin_user_by_id(admin_id: int, db: Session):
    admin = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == admin_id).first()
    if admin:
        admin.is_deleted = False
        admin.deleted_date = None  
        db.add(admin)
        db.commit()
        return {'status': 'true', 'message': "Super Admin user reverted successfully", 'data': admin}
    return {"status": 'false', 'message': "User not found"}



def deactivate_superadmin_user_by_id(admin_id: int, db: Session):
    admin = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == admin_id).first()
    if admin:
        admin.is_active = not admin.is_active
        db.add(admin)
        db.commit() 
        
        try:
            asyncio.run(send_status_update_email(admin.email, admin.full_name, admin.is_active))
        except Exception as e:
            db.rollback()
            return {'status': 'false', 'message': f"Failed to send email: {str(e)}"}
        
        
        return {
            'status': 'true',
            'message': f"Super Admin user {'activated' if admin.is_active else 'deactivated'} successfully",
            'data': {
                'id': admin.id,
                'is_active': admin.is_active,
            }
        }
    return {"status": 'false', 'message': "User not found"}

