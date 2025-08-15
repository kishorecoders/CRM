from .models import AdminAssignRoleEmployee, AdminAssignRoleEmployeeCreate
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status, HTTPException
from src.AdminAddEmployee.models import AdminAddEmployee
from src.SuperAdminPlanAndPrice.models import SuperAdminPlanAndPrice
from src.AdminRoleCreation.models import AdminRoleCreation
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew
from src.cre_upd_name import get_creator_info
from src.AdminAssignRoleDetail.models import AdminAssignRoleDetails


def get_all_assign_role(db: Session):
    data = db.query(AdminAssignRoleEmployee).order_by(AdminAssignRoleEmployee.id.desc()).all()
    response = {'status': 'true', 'message': "Data Received Successfully", 'data': data}
    return response




def create(db: Session, admin_assign_role: AdminAssignRoleEmployeeCreate):
    admin_id = admin_assign_role.admin_id
    employee_id = admin_assign_role.asign_employe_id
    #role_id = admin_assign_role.role_id

   
    existing_record = db.query(AdminAssignRoleEmployee).filter(
        AdminAssignRoleEmployee.admin_id == admin_id,
        AdminAssignRoleEmployee.asign_employe_id == employee_id

    ).first()

    if existing_record:
        return {
            'status': 'false',
            'message': 'Role alredy assign this employee'
        }

    
    db_admin_assign_role = AdminAssignRoleEmployee(**admin_assign_role.dict())
    db.add(db_admin_assign_role)
    db.commit()
    db.refresh(db_admin_assign_role)

    return {
        'status': 'true',
        'message': 'New Role Assign Details Added Successfully',
        'data': db_admin_assign_role
    }



def get_assign_role_by_admin_id(admin_id: int, db: Session):
    
    data = db.query(AdminAssignRoleEmployee).filter(AdminAssignRoleEmployee.admin_id == admin_id).order_by(AdminAssignRoleEmployee.id.desc()).all()

    dataArray = []
    for item in data:
        
        role_details = db.query(AdminRoleCreation).filter(AdminRoleCreation.id == item.role_id).all()

        
        employee_details = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == item.asign_employe_id).first()
        employee_id_company = employee_details.employee_id if employee_details else None
        employee_name = employee_details.employe_name if employee_details else None

        if item.employe_id:
            admin_emp_id = item.employe_id
            created_by_type = "employee"
        else:
            admin_emp_id = item.admin_id
            created_by_type = "admin"

        created = get_creator_info(
            admin_emp_id=admin_emp_id,
            created_by_type=created_by_type,
            db=db
        )
        created["current_role_id"] = item.role_id
        created["switched_role_id"] = item.role_id
        created["created_at"] = item.created_at
        created["updated_at"] = item.updated_at


        AssignRoleDetails = db.query(AdminAssignRoleDetails).filter(AdminAssignRoleDetails.admin_asign_id == item.id).all()

        update_list = []
        for asign in AssignRoleDetails:
            current_role_NAME = ""
            switched_role_NAME = ""

            if asign.current_role_id:
                current_role = db.query(AdminRoleCreation).filter(AdminRoleCreation.id == int(asign.current_role_id)).first()
                if current_role:
                    current_role_NAME = current_role.role_name or ""

            if asign.switched_role_id:
                switched_role = db.query(AdminRoleCreation).filter(AdminRoleCreation.id == int(asign.switched_role_id)).first()
                if switched_role:
                    switched_role_NAME = switched_role.role_name or ""


            if asign.employe_id:
                admin_emp_id = asign.employe_id
                created_by_type = "employee"
            else:
                admin_emp_id = asign.admin_id
                created_by_type = "admin"

            updated = get_creator_info(
                admin_emp_id=admin_emp_id,
                created_by_type=created_by_type,
                db=db
            )
            updated["current_role_id"] = asign.current_role_id
            updated["switched_role_id"] = asign.switched_role_id
            updated["current_role_name"] = current_role_NAME
            updated["switched_role_name"] = switched_role_NAME
            updated["started_at"] = asign.started_at
            updated["ended_at"] = asign.created_at
            update_list.append(updated)


        temp = {
            'role_assign_details': {**item.dict(),'employee_id_company': employee_id_company, 'employee_name':employee_name ,"creator_info":created ,"updater_info":update_list},

            'role_details': role_details
        }
        dataArray.append(temp)

    response = {'status': 'true', 'message': 'Data Received Successfully', 'data': dataArray}
    return response





def get_module_by_admin_id(admin_id: int, db: Session):
    
    admin_data = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == admin_id).all()

    dataArray = []
    for item in admin_data:
        
        plan_details = db.query(SuperAdminPlanAndPrice).filter(SuperAdminPlanAndPrice.id == item.plan_id).all()

        
        if not plan_details:
            
            plan_details = [{
                "name_of_the_subscription": "Demo",
                "store_engineer": True,
                "id": 0,
                "purchase": True,
                "dispatch": True,
                "account": True,
                "customer": True,
                "admin": True,
                "status": "Activate",
                "sales": True,
                "total_access": 5000,
                "project_manager": True,
                "status_update": True
            }]

        temp = {
            'role_assign_details': item,
            'plan_details': plan_details
        }
        dataArray.append(temp)

    response = {'status': 'true', 'message': 'Data Received Successfully', 'data': dataArray}
    return response

from src.AdminAssignRoleDetail.models import AdminAssignRoleDetails


def update(assgin_id: int, admin_assign_role: AdminAssignRoleEmployee, db: Session):
    # Fetch the existing record before updating
    existing_role = db.query(AdminAssignRoleEmployee).filter(AdminAssignRoleEmployee.id == assgin_id).first()

    if not existing_role:
        return {'status': 'false', 'message': 'Role assignment not found'}

    # Capture the 'before' updated_at timestamp
    previous_updated_at = existing_role.updated_at
    previous_role_id = existing_role.role_id

    admin_assign_role_update = admin_assign_role.dict(exclude_unset=True)
    db.query(AdminAssignRoleEmployee).filter(AdminAssignRoleEmployee.id == assgin_id).update(admin_assign_role_update)
    db.commit()

    # Fetch the updated record to access its fields (like id and updated_at)
    updated_role = db.query(AdminAssignRoleEmployee).filter(AdminAssignRoleEmployee.id == assgin_id).first()

    if updated_role:
        # Create a new role switch log
        role_details = AdminAssignRoleDetails(
            admin_id=updated_role.admin_id,
            employe_id=updated_role.employe_id if updated_role.employe_id else None,
            current_role_id=previous_role_id,  # Adjust logic if this isn't correct
            switched_role_id=updated_role.role_id,
            status=updated_role.status,
            admin_asign_id=updated_role.id,
            started_at=previous_updated_at
        )
        db.add(role_details)
        db.commit()

    response = {'status': 'true', 'message': "Data Updated Successfully", 'data': admin_assign_role_update}
    return response





def show_role_by_user(admin_id: int, db: Session):
    # Query to get all the roles assigned to this admin
    role_assignments = db.query(AdminAssignRoleEmployee).filter(
        AdminAssignRoleEmployee.admin_id == admin_id
    ).all()

    print(f"Role Assignments for admin_id {admin_id}: {role_assignments}")  # Debug log to check role assignments

    if not role_assignments:
        return {"status": "false", "message": "No roles found for the given admin_id"}

    counted_roles = {}

    # Loop through the role assignments and count the occurrences of each role
    for assignment in role_assignments:
        role_id = assignment.role_id
        print(f"Processing role_id: {role_id}, current counted_roles: {counted_roles}")  # Debug log to check role_id processing

        if role_id not in counted_roles:
            counted_roles[role_id] = {
                "role_id": role_id,
                "role_id_use_count": 1,
                "data": [assignment],
            }
        else:
            counted_roles[role_id]["role_id_use_count"] += 1
            counted_roles[role_id]["data"].append(assignment)

    print(f"Counted roles after processing: {counted_roles}")  # Debug log to check final role counts

    # Get all roles from admin_role_creation (even those not assigned)
    all_roles = db.query(AdminRoleCreation).all()  # Get all roles in the database
    print(f"All roles in database: {all_roles}")  # Debug log to check all roles

    # Ensure all roles from admin_role_creation are included, even if they have no assignments
    for role in all_roles:
        if role.id not in counted_roles:
            print(f"Adding missing role: {role}")  # Debug log to check missing role
            counted_roles[role.id] = {
                "role_id": role.id,
                "role_id_use_count": 0,
                "data": [],  # No assignments for this role
            }

    # Final response with grouped roles
    response_data = list(counted_roles.values())

    response = {
        "status": "true",
        "message": "Roles fetched successfully",
        "counted_data": response_data,
    }
    return response


