from .models import AdminAddEmployee, AdminAddEmployeeCreate,DeleteEmployee
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status, HTTPException
from src.SuperAdminPlanAndPrice.models import SuperAdminPlanAndPrice
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew
from src.AdminAssignRoleEmployee.models import AdminAssignRoleEmployee
from src.AdminRoleCreation.models import AdminRoleCreation
import re  

from sqlalchemy import select
import json

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from src.RoleAssignByLevel.models import RoleAssignByLevel


def get_all_admin_employee(db: Session):
    data = db.query(AdminAddEmployee).order_by(AdminAddEmployee.id.desc()).all()
    response = {'status': 'true', 'message': "Data Received Successfully", 'data': data}
    return response


def create(db: Session, admin_add_employee: AdminAddEmployee, first_employee_id: Optional[str] = None):
    email = admin_add_employee.employe_email_id
    phone = admin_add_employee.employe_phone_number
    admin_id = admin_add_employee.admin_id

   
    existing_email_employee = db.query(AdminAddEmployee).filter(
        AdminAddEmployee.admin_id == admin_id,
        AdminAddEmployee.employe_email_id == email
    ).first()

   
    existing_email_admin = db.query(SuperAdminUserAddNew).filter(
        SuperAdminUserAddNew.email == email
    ).first()

    if email and (existing_email_employee or existing_email_admin):
        return {"status": "false", "message": "Email is already registered. Please use a different email."}

    
    existing_phone_employee = db.query(AdminAddEmployee).filter(
        AdminAddEmployee.admin_id == admin_id,
        AdminAddEmployee.employe_phone_number == phone
    ).first()

    
    existing_phone_admin = db.query(SuperAdminUserAddNew).filter(
        SuperAdminUserAddNew.phone_number == phone
    ).first()

    if phone and (existing_phone_employee or existing_phone_admin):
        return {"status": "false", "message": "Phone number is already registered. Please use a different phone number."}

    
    super_admin_user = db.query(SuperAdminUserAddNew).filter(
        SuperAdminUserAddNew.id == admin_id
    ).first()
    if not super_admin_user:
        return {"status": "false", "message": "Invalid admin_id"}

    
    admin_plan = db.query(SuperAdminPlanAndPrice).filter(
        SuperAdminPlanAndPrice.id == super_admin_user.plan_id
    ).first()
    if not admin_plan:
        return {"status": "false", "message": "Admin's plan not found"}

    total_employees = db.query(AdminAddEmployee).filter(
        AdminAddEmployee.admin_id == admin_id
    ).count()

    if total_employees >= admin_plan.total_access:
        return {
            "status": "false",
            "message": f"Employee creation limit is over. Maximum allowed: {admin_plan.total_access}. Please upgrade your plan to add more employees.",
        }

   
    prefix = None 
    counter = 1   

    if total_employees == 0:
    
        if first_employee_id:
            match = re.match(r"([a-zA-Z#_]+)(\d+)", first_employee_id)
            if match:
                prefix, counter = match.groups()
                counter = int(counter) 
            else:
                return {"status": "false", "message": "Invalid first_employee_id format. Expected format: PREFIX###"}
    else:
      
        last_employee = db.query(AdminAddEmployee).filter(
            AdminAddEmployee.admin_id == admin_id
        ).order_by(AdminAddEmployee.id.desc()).first()
        if last_employee and last_employee.employee_id:
            match = re.match(r"([a-zA-Z#_]+)(\d+)", last_employee.employee_id)
            if match:
                prefix, last_counter = match.groups()
                counter = int(last_counter) + 1
            else:
                return {"status": "false", "message": "Invalid employee_id format for the last employee"}

    
    if not prefix:
        return {"status": "false", "message": "Prefix could not be determined"}

   
    employee_id = f"{prefix}{str(counter).zfill(3)}" 
    admin_add_employee.employee_id = employee_id

    db_admin_add_employee = AdminAddEmployee(**admin_add_employee.dict())
    db.add(db_admin_add_employee)
    db.commit()
    db.refresh(db_admin_add_employee)

    return {
        "status": "true",
        "message": "Employee Details Added Successfully",
        "data": db_admin_add_employee,
    }


from src.TimeConfig.models import TimeConfig


def get_employee_by_admin_id(admin_id: int, role: Optional[str] ,db: Session):
    employee_data = db.query(AdminAddEmployee).filter(AdminAddEmployee.admin_id == admin_id).order_by(AdminAddEmployee.id.desc()).all()

    response = {'status': 'true', 'message': "Data Received Successfully", 'data': []}

    for employee in employee_data:
        
        # Get assigned role
        role_data = db.query(AdminAssignRoleEmployee).filter(
            AdminAssignRoleEmployee.admin_id == admin_id,
            AdminAssignRoleEmployee.asign_employe_id == employee.id
        ).first()

        assign_status = 'Not Assign'
        roleName = None

        if role_data:
            role_details = db.query(AdminRoleCreation).filter(
                AdminRoleCreation.id == role_data.role_id
            ).first()
            if role_details:
                roleName = role_details.role_name
                assign_status = 'Assign'

        # Filter by role if specified
        if role:
            if roleName and role and roleName.lower() != role.lower() or roleName == None:
                continue

        shift_map = {
            "shift-1": "1st",
            "shift-2": "2nd",
            "shift-3": "3rd",
            "general": "general"
        }

        start_time = ""
        end_time = ""

        if employee.shift_name:
            shift_key = shift_map.get(employee.shift_name.strip(), "").lower()
            
            if shift_key:
                time_config = db.query(TimeConfig).filter(
                    TimeConfig.admin_id == admin_id,
                    TimeConfig.shift_name == employee.shift_name
                ).first()

                if time_config:
                    start_time = getattr(time_config, f"start_time_{shift_key}", "")
                    end_time = getattr(time_config, f"end_time_{shift_key}", "")
                 

        employee_info = {
            'admin_id': employee.admin_id,
            'employee_id': employee.employee_id,
            'employe_name': employee.employe_name,
            'employe_password': employee.employe_password,
            'employe_remark': employee.employe_remark,
            'created_at': employee.created_at,
            'employe_job_title': employee.employe_job_title,
            'employe_email_id': employee.employe_email_id,
            'employe_phone_number': employee.employe_phone_number,
            'employe_user_name': employee.employe_user_name,
            'employe_confirm_password': employee.employe_confirm_password,
            'id': employee.id,
            'updated_at': employee.updated_at,
            'assign_status': assign_status,
            'role_name': roleName,
            'level': employee.level,
            'shift_name' : employee.shift_name,
            'employe_email_id': employee.employe_email_id,
            'employe_name': employee.employe_name,
            'designation' : employee.Designation,
            'employe_phone_number': employee.employe_phone_number,
            'employe_job_title': employee.employe_job_title,
            'employee_id': employee.employee_id,
            'employe_user_name': employee.employe_user_name,
            'employe_remark': employee.employe_remark,
            'employee_salary': employee.employee_salary,
            'school_or_college_name': employee.school_or_college_name,
            'education_passout_year': employee.education_passout_year,
            'description': employee.description,
            'bank_name': employee.bank_name,
            'bank_account_holder_name': employee.bank_account_holder_name,
            'bank_account_number': employee.bank_account_number,
            'bank_ifsc_code': employee.bank_ifsc_code,
            'skills': employee.skills_list,
            'position': employee.position,
            'past_company_name': employee.past_company_name,
            'experience': employee.experience,
            'paid_leave':employee.paid_leave,
            'is_active':employee.is_active,
            'start_time' : start_time,
            'end_time' : end_time,
            'pan_card': employee.pan_card,
            'house_rent_allowance' : employee.house_rent_allowance,
            'dearness_allowance': employee.dearness_allowance,
            'medical_allowance': employee.medical_allowance,
            'special_allowance':employee.special_allowance,
            'bonus': employee.bonus,
            'telephone_reimbursement': employee.telephone_reimbursement,
            'fuel_reimbursement': employee.fuel_reimbursement,

            
        }
        response['data'].append(employee_info)
    return response


def show_by_employee(admin_id: int, employee_id: str, db: Session):
    admin_add_employee = db.query(AdminAddEmployee).filter(AdminAddEmployee.admin_id == admin_id,
                            AdminAddEmployee.id == employee_id).first()

    if not admin_add_employee:
        return {'status': 'false', 'message': "Employee not found"}

    role_details = None

   
    if admin_id and employee_id:
        admin_assign_role = db.query(AdminAssignRoleEmployee).filter(
            AdminAssignRoleEmployee.admin_id == admin_id,
            AdminAssignRoleEmployee.asign_employe_id == employee_id
        ).first()

        if admin_assign_role:
           
            role_details = db.query(AdminRoleCreation).filter(AdminRoleCreation.id == admin_assign_role.role_id).first()

    return {
        'status': 'true',
        'message': 'Data Received Successfully',
        'data': {
            'employee_details': admin_add_employee,
            'role_details': role_details,
        },
    }



def delete_employee(request: DeleteEmployee, db: Session):
    employee_delete = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == int(request.employee_id)).first()

    if not employee_delete:
        return {'status': 'false', 'message': "Employee not found"}

    if employee_delete.admin_id != request.admin_id:
        return {'status': 'false', 'message': "You are not authorized to delete this Employee"}

    employee_data = employee_delete.id

    assigned_roles = db.query(AdminAssignRoleEmployee).filter(
        AdminAssignRoleEmployee.asign_employe_id == str(employee_data)
    ).first()

    if assigned_roles:
        return {
            'status': 'false',
            'message': 'Cannot delete employee with assigned roles.'
        }

    db.delete(employee_delete)
    db.commit()

    return {
        'status': 'true',
        'message': 'Employee deleted successfully'
    }


#def update(employe_id: int, admin_add_employee: AdminAddEmployee, db: Session):
#    admin_add_employee_update = admin_add_employee.dict(exclude_unset=True)
#    db.query(AdminAddEmployee).filter(AdminAddEmployee.id == employe_id).update(admin_add_employee_update)
#    db.commit()
#    response = {'status': 'true', 'message': "Data Updated Successfully", 'data': admin_add_employee_update}
#    return response
    
    
    
    




def update(employe_id: int, admin_add_employee: AdminAddEmployeeCreate, db: Session):
    existing_employee = db.get(AdminAddEmployee, employe_id)
    if not existing_employee:
        return {"status": "false", "message": "Employee not found"}

    new_level = admin_add_employee.level
    
    old_level = existing_employee.level
    
    employee_id_str = str(existing_employee.id)  # Make sure it's string for comparison
    
    admin_id = existing_employee.admin_id
    
    
    if new_level != old_level :
        print("jvdjfkgfd")
        # Fetch only relevant assignments with matching admin_id
        assignments = (
            db.query(RoleAssignByLevel)
            .filter(RoleAssignByLevel.admin_id == admin_id)
            .all()
        )

        

        for assignment in assignments:
            try:
                employee_list = assignment.employe_id_to or []
                print("employee_list",employee_list)
                if employee_id_str in employee_list:
                    return {
                        "status": "false",
                        "message": f"Level cannot be updated because this employee is already assigned."
                    }
            except Exception as e:
                
                continue

    # Proceed with update
    update_data = admin_add_employee.dict(exclude_unset=True)
    db.query(AdminAddEmployee).filter(AdminAddEmployee.id == employe_id).update(update_data)
    db.commit()
    return {"status": "true", "message": "Data Updated Successfully", "data": update_data}





    
    
    
  
def update_employee_status(admin_id: int, employee_id: str, is_active: bool, db: Session):
    employee = db.query(AdminAddEmployee).filter(
        AdminAddEmployee.admin_id == admin_id,
        AdminAddEmployee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    employee.is_active = is_active
    employee.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(employee)

    return {
        "status": "true",
        "message": "Employee status updated successfully",
        "data": {
            "admin_id": admin_id,
            "employee_id": employee_id,
            "is_active": is_active
        }
    }
  

