from sqlalchemy.orm import Session
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew
from datetime import datetime, timedelta
from src.AdminAddEmployee.models import AdminAddEmployee
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew
from src.AdminAssignRoleEmployee.models import AdminAssignRoleEmployee
from src.AdminRoleCreation.models import AdminRoleCreation
from sqlalchemy import or_

from typing import List, Optional


def login(db: Session, email: str, password: str):
    employee = db.query(AdminAddEmployee).filter(AdminAddEmployee.employe_email_id == email).first()
    if employee:
    
        if not employee.is_active:
            return {
                'status': 'false',
                'message': 'You cannot log in because you have been deactivated by the admin. Please contact the admin.'
            }
    
    
        employee_login = db.query(AdminAddEmployee).filter(
            AdminAddEmployee.employee_id == employee.employee_id,
            AdminAddEmployee.employe_password == password
        ).first()

        if employee_login:
            usage = db.query(SuperAdminUserAddNew).filter(
                SuperAdminUserAddNew.id == employee_login.admin_id,
                SuperAdminUserAddNew.expiry_date >= datetime.now()
            ).first()

            if usage:
                assigned_role = db.query(AdminAssignRoleEmployee).filter(
                    AdminAssignRoleEmployee.asign_employe_id == employee.id
                ).first()

                if assigned_role:
                    role = db.query(AdminRoleCreation).filter(
                        AdminRoleCreation.id == assigned_role.role_id
                    ).first()

                    if role:
                        # Fetch company name
                        company = db.query(SuperAdminUserAddNew).filter(
                            SuperAdminUserAddNew.id == employee.admin_id
                        ).first()

                        company_name = company.company_name if company else "Unknown"
                        phone_number = company.phone_number if company else ""

                        return {
                            'status': 'true',
                            'message': 'Login successful',
                            'id': employee.id,  
                            'employee_id': employee.employee_id,
                            'admin_id': employee_login.admin_id,
                            'role': role,
                            'level': employee.level,
                            'employe_email_id': employee.employe_email_id,
                            'employe_name': employee.employe_name,
                            'employe_phone_number': employee.employe_phone_number,
                            'employe_job_title': employee.employe_job_title,
                            'employe_user_name': employee.employe_user_name,
                            'employe_remark': employee.employe_remark,
                            'school_or_college_name': employee.school_or_college_name,
                            'education_passout_year': employee.education_passout_year,
                            'description': employee.description,
                            'bank_name': employee.bank_name,
                            'bank_account_holder_name': employee.bank_account_holder_name,
                            'bank_account_number': employee.bank_account_number,
                            'bank_ifsc_code': employee.bank_ifsc_code,
                            'skills_list': employee.skills_list,
                            'position': employee.position,
                            'past_company_name': employee.past_company_name,
                            'experience': employee.experience,
                            'company_name': company_name,  # Include company name
                            'phone_number': phone_number
                        }
                    else:
                        return {'status': 'false', 'message': 'Insufficient permissions. Please contact the admin.'}
                else:
                    return {'status': 'false', 'message': 'Role not assigned. Please contact the admin.'}
            else:
                return {'status': 'false', 'message': 'Your access has expired. Please contact the admin.'}
        else:
            return {'status': 'false', 'message': 'Incorrect password'}
    else:
        return {'status': 'false', 'message': 'Email not found'}


def login_with_email(db: Session, employe_email_id: str):
    
    employee = db.query(AdminAddEmployee).filter_by(employe_email_id=employe_email_id).first()

    if employee:
        
        assigned_role = db.query(AdminAssignRoleEmployee).filter_by(asign_employe_id=employee.id).first()

        if assigned_role:
            
            role = db.query(AdminRoleCreation).filter(
                AdminRoleCreation.id == assigned_role.role_id,
                or_(
                    AdminRoleCreation.sales_read == 1,
                    AdminRoleCreation.sales_write == 1,
                    AdminRoleCreation.sales_edit == 1,
                    AdminRoleCreation.sales_delete == 1
                )
            ).first()

            if role:
                
                admin_data = db.query(AdminAddEmployee.admin_id).filter_by(employe_email_id=employe_email_id).first()
                expiry_date = db.query(SuperAdminUserAddNew.expiry_date).filter_by(id=admin_data.admin_id).first()

                admin_details = db.query(
                    SuperAdminUserAddNew.expiry_date,
                    SuperAdminUserAddNew.company_name,
                    SuperAdminUserAddNew.phone_number,
                ).filter_by(id=admin_data.admin_id).first()

                if expiry_date and expiry_date[0] >= datetime.now():
                    return {
                        'status': 'true',
                        'message': 'Login successful',
                        'employee_id': employee.employee_id,
                        'admin_id': admin_data.admin_id,
                        'company_name': admin_details.company_name,
                        'admin_phone_number':admin_details.phone_number,
                        'employe_name': employee.employe_name,
                        'level': employee.level
                    }
                else:
                    
                    return {
                        'status': 'false',
                        'message': 'Your access has expired. Please contact the admin.'
                    }
            else:
                
                return {
                    'status': 'false',
                    'message': 'Insufficient permissions. Please contact the admin.'
                }
        else:
            
            return {
                'status': 'false',
                'message': 'Role not assigned. Please contact the admin.'
            }
    else:
       
        return {
            'status': 'false',
            'message': 'Email not found'
        }



from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew
from src.Settings.models import Setting

def login_with_phone(db: Session, phone: str,device_type: Optional[str] = None, device_token: Optional[str] = None):

    device_token = None if device_token in [None, ""] else device_token
    device_type = None if device_type in [None, ""] else device_type

    phone_admin = phone
    phone1 = None
    if phone_admin.startswith("91") and len(phone) == 12:
        phone1 = phone_admin[2:]
    else:
        phone1 = phone
    

    alladmin_user = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.phone_number == phone1).all()

    admin_dataall = []

    for admin_user in alladmin_user:
        if admin_user:
            Sett = db.query(Setting).filter(Setting.admin_id == admin_user.id).first()
            if Sett:
                address = Sett.address if  Sett.address else ""
                logo = Sett.logo if  Sett.logo else ""

            if admin_user.is_deleted:
                return {'status': 'false', 'message': 'User account deleted by Super Admin'}

            if not admin_user.is_active:
                return {'status': 'false', 'message': 'User account is deactivated'}
            current_date = datetime.now()
            if admin_user.expiry_date and admin_user.expiry_date >= current_date:
                if device_token:
                    admin_user.device_token = device_token
                if device_type:
                    admin_user.device_type = device_type
                db.add(admin_user)
                db.commit()
                data_admin ={
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
                admin_dataall.append(data_admin)
                role = db.query(AdminRoleCreation).filter(AdminRoleCreation.admin_id == admin_user.id,
                                                          AdminRoleCreation.role_name == "Operator").first()
                if role:
                    data_admin ={
                        'type': 'operator',
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
                    admin_dataall.append(data_admin)
            else:
                # data_emp['message'] = 'Your access has expired. Please contact the admin.'

                return {'status': 'false', 'message': 'Your plan has expired'}

    employee = db.query(AdminAddEmployee).filter(AdminAddEmployee.employe_phone_number == phone).first()
    if employee:
        
        if not employee.is_active:
            return {
                'status': 'false',
                'message': 'You cannot log in because you have been deactivated by the admin. Please contact the admin.'
            }
        
        if device_token:
            employee.device_token = device_token
        if device_type:
            employee.device_type = device_type
        db.add(employee)
        db.commit()
        data_emp ={}
        data_emp =  {
            'type': 'employee',
            'id': employee.id,
            'employee_id': employee.employee_id,
            'admin_id': employee.admin_id,
            'employe_name': employee.employe_name,
            'employe_job_title': employee.employe_job_title,

            'employe_email_id': employee.employe_email_id,
            'employe_phone_number': employee.employe_phone_number,
            'employe_user_name': employee.employe_user_name,
            'employee_salary': employee.employee_salary,
            'employe_remark': employee.employe_remark,
            'level': employee.level,
            'shift_name': employee.shift_name,
            'paid_leave': employee.paid_leave,
            'date_of_birth': employee.date_of_birth,
            'Designation': employee.Designation,
            'past_company_name': employee.past_company_name,

            # Newly added fields
            'school_or_college_name': employee.school_or_college_name,
            'education_passout_year': employee.education_passout_year,
            'description': employee.description,

            'bank_name': employee.bank_name,
            'bank_account_holder_name': employee.bank_account_holder_name,
            'bank_account_number': employee.bank_account_number,
            'bank_ifsc_code': employee.bank_ifsc_code,

            'skills_list': employee.skills_list,
            'position': employee.position,
            'experience': employee.experience,
            
        }
        assigned_role = db.query(AdminAssignRoleEmployee).filter_by(asign_employe_id=employee.id).first()
        if assigned_role:
          
            # admin_data = db.query(AdminAddEmployee).filter_by(employe_phone_number=phone).first()
            
            
            admin_details = db.query(
                SuperAdminUserAddNew.expiry_date,
                SuperAdminUserAddNew.company_name
            ).filter_by(id=employee.admin_id).first()
            if admin_details and admin_details.expiry_date >= datetime.now():
                pass
                
            else:
                data_emp['message'] = 'Your access has expired. Please contact the admin.'
                data_emp['status'] = 'false'

        else:
            data_emp['message'] = 'Role not assigned. Please contact the admin.'
            data_emp['status'] = 'false'
        
        data_emp['message'] = ''
        data_emp['status'] = 'true'
        admin_dataall.append(data_emp)
    else:
        pass
        # print(f"Employee with phone {phone} not found. Employee object: {employee}")
        # data_emp1['message'] = 'Employee with phone not found'
        # data_emp1['status'] = 'false'
        # admin_dataall.append(data_emp1)
        # return {
        #     'status': 'false',
        #     'message': 'Phone number not found.'
        # }

    if admin_dataall:
        return {
            'status': 'true',
            'message': 'Login Successfully',
            'data': admin_dataall
        }



