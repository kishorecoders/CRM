from fastapi import HTTPException, Depends, APIRouter, Header,Body
from sqlmodel import Session
from src.database import get_db
from src.AdminLogin.service import login_admin,show_admin_deshbord_count
from src.parameter import get_token
from datetime import datetime
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew
from src.AdminAddEmployee.models import AdminAddEmployee


from src.SmtpEmail.Smtp_mail import send_login_email , send_password_reset_confirmation_email
from fastapi import Request
import secrets
from datetime import datetime, timedelta
from src.Settings.models import Setting



router = APIRouter()


# @router.post("/")
# def admin_login(email: str = Body(...), password: str = Body(...),auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#              db: Session = Depends(get_db)):
#     def inner_get_plan(auth_token: str):
#         if auth_token != get_token():
#             return {"status": "false", "message": "Unauthorized Request"}
#         else:
#             return login_admin(db=db, email=email, password=password)
    
#     return inner_get_plan(auth_token)
@router.post("/")
def admin_login(
    email: str = Body(...),
    password: str = Body(...),
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return login_admin(db=db, email=email, password=password)
    
    return inner_get_plan(auth_token)
    
    
    
    



@router.post("/login/")
def unified_login(
    request: Request,
    email: str = Body(...),
    password: str = Body(...),
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    def inner_login(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        client_ip = request.client.host
        # Check in SuperAdminUserAddNew (admin)
        admin_user = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.email == email).first()


        if admin_user:
            Sett = db.query(Setting).filter(Setting.admin_id == admin_user.id).first()
            if Sett:
                address = Sett.address if  Sett.address else ""
                logo = Sett.logo if  Sett.logo else ""

            if admin_user.is_deleted:
                return {'status': 'false', 'message': 'User account deleted by Super Admin'}

            if not admin_user.is_active:
                return {'status': 'false', 'message': 'User account is deactivated'}

            if password == admin_user.password:
                current_date = datetime.now()
                send_login_email(
                    to_email="poojaevolve20@gmail.com",
                    subject="Admin Login Successful",
                    body = (
                            f"Hello {admin_user.full_name},\n\n"
                            f"You have successfully logged in on {current_date.strftime('%Y-%m-%d %H:%M:%S')}.\n"
                            f"IP Address of login: {client_ip}.\n\n"
                            f"Regards,\n"
                            f"SphuritCrm Team"
                        )
                )
                if admin_user.expiry_date and admin_user.expiry_date >= current_date:
                    return {
                        'status': 'true',
                        'message': 'Admin Login Successfully',
                        'type': 'admin',
                        'admin_id': admin_user.id,
                        'company_name': admin_user.company_name,
                        'full_name': admin_user.full_name,
                        
                        'designation': admin_user.designation,
                        'email': admin_user.email,
                        'phone_number': str(admin_user.phone_number),
                        'plan_id': admin_user.plan_id,
                        'amount': admin_user.amount,
                        'demo_period_day': admin_user.demo_period_day,
                        'expiry_date': admin_user.expiry_date,
                        'gst_number': admin_user.gst_number,
                        'state': admin_user.state,
                        'address': address,
                        'logo': logo
                    }
                else:
                    return {'status': 'false', 'message': 'Your plan has expired'}
            else:
                return {'status': 'false', 'message': 'Invalid Email or Password'}

        # Check in AdminAddEmployee (employee)
        employee_user = db.query(AdminAddEmployee).filter(AdminAddEmployee.employe_email_id == email).first()

        if employee_user:
            if not employee_user.is_active:
                return {'status': 'false', 'message': 'Employee account is deactivated'}

            if password == employee_user.employe_password:
                send_login_email(
                    to_email="poojaevolve20@gmail.com",
                    subject="Employee Login Successful",
                    body = (
                            f"Hello {employee_user.employe_name},\n\n"
                            f"You have successfully logged in on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.\n"
                            f"IP Address of login: {client_ip}.\n\n"
                            f"Regards,\n"
                            f"SphuritCrm Team"
                        )
                )
                return {
                    'status': 'true',
                    'message': 'Employee Login Successfully',
                    'type': 'employee',
                    'id': employee_user.id,
                    'employee_id': employee_user.employee_id,
                    'admin_id': employee_user.admin_id,
                    'employe_name': employee_user.employe_name,
                    'employe_job_title': employee_user.employe_job_title,

                    'employe_email_id': employee_user.employe_email_id,
                    'employe_phone_number': employee_user.employe_phone_number,
                    'employe_user_name': employee_user.employe_user_name,
                    'employee_salary': employee_user.employee_salary,
                    'employe_remark': employee_user.employe_remark,
                    'level': employee_user.level,
                    'shift_name': employee_user.shift_name,
                    'paid_leave': employee_user.paid_leave,
                    'date_of_birth': employee_user.date_of_birth,
                    'Designation': employee_user.Designation,
                    'past_company_name': employee_user.past_company_name,

                    # Newly added fields
                    'school_or_college_name': employee_user.school_or_college_name,
                    'education_passout_year': employee_user.education_passout_year,
                    'description': employee_user.description,

                    'bank_name': employee_user.bank_name,
                    'bank_account_holder_name': employee_user.bank_account_holder_name,
                    'bank_account_number': employee_user.bank_account_number,
                    'bank_ifsc_code': employee_user.bank_ifsc_code,

                    'skills_list': employee_user.skills_list,
                    'position': employee_user.position,
                    'experience': employee_user.experience,
                    
                }
            else:
                return {'status': 'false', 'message': 'Invalid Email or Password'}

        return {'status': 'false', 'message': 'Email is not registered in system'}

    return inner_login(auth_token)



@router.get("/showDesboardCount/{admin_id}")
def read_admin_deshbord_coun(admin_id:str,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db:Session=Depends(get_db)):
       def inner_get_plan(auth_token: str):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return show_admin_deshbord_count(admin_id=admin_id,db=db)
    
       return inner_get_plan(auth_token)
       
       

@router.post("/forgot-password/")
def forgot_password(email: str = Body(...), db: Session = Depends(get_db)):
    token = secrets.token_urlsafe(32)
    expiry = datetime.utcnow() + timedelta(minutes=30)  # Token valid for 30 minutes

    # Check Admin
    user = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.email == email).first()
    if user:
        if not user.is_active:
            return {"status": "false", "message": "Account is deactivated"}
        
        user.reset_token = token
        user.reset_token_expiry = expiry
        db.commit()

        reset_link = f"https://admin.sphuritcrm.in/reset-password?token={token}&email={email}"
        send_login_email(
            to_email=email,
            subject="Reset Your Password - SphuritCrm",
            body=f"""Hello {user.full_name},

You requested to reset your password.
Click the link below to set a new password:

{reset_link}

If you did not request this, please ignore this email.

Regards,
SphuritCrm Team"""
        )
        return {"status": "true", "message": "Reset password link sent to your email"}

    # Check Employee
    employee = db.query(AdminAddEmployee).filter(AdminAddEmployee.employe_email_id == email).first()
    if employee:
        if not employee.is_active:
            return {"status": "false", "message": "Account is deactivated"}
        
        employee.reset_token = token
        employee.reset_token_expiry = expiry
        db.commit()

        reset_link = f"https://admin.sphuritcrm.in/reset-password?token={token}&email={email}"
        send_login_email(
            to_email=email,
            subject="Reset Your Password - SphuritCrm",
            body=f"""Hello {employee.employe_name},

You requested to reset your password.
Click here to set a new one:

{reset_link}

If you didn't request this, ignore this email.

Regards,
SphuritCrm Team"""
        )
        return {"status": "true", "message": "Reset password link sent to your email"}

    return {"status": "false", "message": "Email not found"}


@router.post("/reset-password/")
def reset_password(
    email: str = Body(...),
    token: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(get_db)
):
    now = datetime.utcnow()

    # Admin reset
    user = db.query(SuperAdminUserAddNew).filter(
        SuperAdminUserAddNew.email == email,
        SuperAdminUserAddNew.reset_token == token,
        SuperAdminUserAddNew.reset_token_expiry > now
    ).first()
    if user:
        user.password = new_password
        user.confirm_password = new_password
        user.reset_token = None
        user.reset_token_expiry = None
        db.commit()

        send_password_reset_confirmation_email(email=email, full_name=user.full_name)
        return {"status": "true", "message": "Admin password updated successfully"}

    # Employee reset
    employee = db.query(AdminAddEmployee).filter(
        AdminAddEmployee.employe_email_id == email,
        AdminAddEmployee.reset_token == token,
        AdminAddEmployee.reset_token_expiry > now
    ).first()
    if employee:
        employee.employe_password = new_password
        employee.employe_confirm_password = new_password
        employee.reset_token = None
        employee.reset_token_expiry = None
        db.commit()

        send_password_reset_confirmation_email(email=email, full_name=employee.employe_name)
        return {"status": "true", "message": "Employee password updated successfully"}

    return {"status": "false", "message": "Invalid token or expired or email not found"}

      
