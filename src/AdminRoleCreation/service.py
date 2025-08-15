from .models import AdminRoleCreation,AdminRoleCreationCreate
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status,HTTPException
from src.AdminAssignRoleEmployee.models import AdminAssignRoleEmployee
from src.cre_upd_name import get_creator_updator_info


def get_all_role(db: Session):
    data = db.query(AdminRoleCreation).order_by(AdminRoleCreation.id.desc()).all()
    response = {'status': 'true', 'message': "Data Received Successfully", 'data': data}
    return response

def create(db: Session, admin_role_creation: AdminRoleCreationCreate):
    db_admin_role_creation = AdminRoleCreation(**admin_role_creation.dict())
    db.add(db_admin_role_creation)
    db.commit()
    db.refresh(db_admin_role_creation)
    response = {'status': 'true','message':"Role Creation Details Added Successfully",'data':db_admin_role_creation}
    return response

def get_role_by_admin_id(admin_id: int, db: Session):
    data = (
        db.query(AdminRoleCreation)
        .filter(AdminRoleCreation.admin_id == admin_id)
        .order_by(AdminRoleCreation.id.desc())
        .all()
    )
    result = []

    for role in data:
        # Convert model to dict and remove internal state
        role_data = vars(role).copy()
        role_data.pop("_sa_instance_state", None)

        # Add custom data
        created_updated_data = get_creator_updator_info(
            admin_emp_id=role.admin_emp_id,
            created_by_type=role.created_by_type,
            updated_admin_emp_id=role.updated_admin_emp_id,
            updated_by_type=role.updated_by_type,
            db=db,
        )

        # Merge and append
        result.append({**role_data, **created_updated_data})

    return {
        "status": "true",
        "message": "Data Received Successfully",
        "data": result,
    }
    
def get_role_detail_by_id(admin_id: int, role_id: int, db: Session):
    role = (
        db.query(AdminRoleCreation)
        .filter(
            AdminRoleCreation.admin_id == admin_id,
            AdminRoleCreation.id == role_id
        )
        .first()
    )

    if not role:
        return {
            "status": "false",
            "message": "Role not found",
            "data": None
        }

    # Merge and return
    return {
        "status": "true",
        "message": "Data Received Successfully",
        "data":role,
    }


def update(role_id:int,admin_role_creation:AdminRoleCreation,db:Session):
    admin_role_creation_update = admin_role_creation.dict(exclude_unset=True)
    db.query(AdminRoleCreation).filter(AdminRoleCreation.id == role_id).update(admin_role_creation_update)
    db.commit()
    response = {'status': 'true','message':"Data Updated Successfully",'data':admin_role_creation_update}
    return response

def deactivate_role(db: Session, role_id, authenticated_admin_id, status):
    role_delete = db.query(AdminRoleCreation).filter(AdminRoleCreation.id == role_id).first()

    if not role_delete:
        return {"status":"false", "message":"Role not found"}

    if role_delete.admin_id != authenticated_admin_id:
        return {"status":"false", "message":"You are not authorized to Deactivate this Role"}

    role_delete.status = status
    db.commit()

    
    db.query(AdminAssignRoleEmployee).filter(AdminAssignRoleEmployee.role_id == role_id).update({
        'status': status
    })
    db.commit()

    return {
        'status': 'true',
        'message': 'Role Updated Successfully'
    }

# def delete_role(db: Session, role_id: int, authenticated_admin_id: int):
#     role_delete = db.query(AdminRoleCreation).filter(
#         AdminRoleCreation.id == role_id,
#         AdminRoleCreation.admin_id == authenticated_admin_id
#     ).first()

#     if not role_delete:
#         return {"status":"false", "message":"Role not found"}

#     if role_delete.admin_id != authenticated_admin_id:
#        return {"status":"false", "message":"You are not authorized to Delete this Role"}

#     # Get employee_ids associated with the role
#     employee_ids = db.query(AdminAssignRoleEmployee.employe_id).filter(
#         AdminAssignRoleEmployee.role_id == role_id
#     ).all()

#     # Flatten the result and convert it to a list
#     employee_ids = [item for sublist in employee_ids for item in sublist]

#     # Update AdminSales table
#     db.query(AdminSales).filter(
#         AdminSales.allocated_emplyee_id.in_(employee_ids)
#     ).update({
#         'allocated_emplyee_id': None,
#         'lead_status': 'Not Assigned'
#     })

#     # Delete records from AdminAssignRoleEmployee table
#     db.query(AdminAssignRoleEmployee).filter(
#         AdminAssignRoleEmployee.role_id == role_id
#     ).delete()

#     # Delete the role
#     db.delete(role_delete)
#     db.commit()

#     return {
#         'status': 'true',
#         'message': 'Role Delete Successfully'
#     }

def delete_admin_role(id: int, db: Session):
    admin_role = db.query(AdminRoleCreation).filter(AdminRoleCreation.id == id).first()

    if not admin_role:
       {'status': 'false', 'message': "Role Not Found"}

    db.delete(admin_role)
    db.commit()

    response = {
        'status': 'true',
        'message': "Role deleted successfully"
    }
    
    return response