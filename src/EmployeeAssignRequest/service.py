from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status, HTTPException
from src.EmployeeAssignRequest.models import EmployeeAssignRequest
from src.AdminAddEmployee.models import AdminAddEmployee
from .models import EmployeeAssignRequestCreate
from sqlalchemy import exc
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from sqlmodel import Session, select
from sqlalchemy.orm import aliased
from src.RoleAssignByLevel.models import RoleAssignByLevel
from src.AdminRoleCreation.models import AdminRoleCreation
from src.AdminAssignRoleEmployee.models import AdminAssignRoleEmployee



def get_current_datetime():
    return datetime.utcnow()

# def createRequest(db: Session, role_assign: EmployeeAssignRequestCreate):
#     admin_id = role_assign.admin_id
#     employee_id_from = role_assign.employe_id_from
#     employee_ids_to = role_assign.employe_id_to

    
#     employee_from = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == employee_id_from).first()
#     if not employee_from:
#         return {"status": "false", "message": "Employee ID (from) not found."}

   
#     for employee_id in employee_ids_to:
#         employee_to = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == employee_id).first()
#         if not employee_to:
#             return {"status": "false", "message": f"Employee ID (to) {employee_id} not found."}

#     try:
        
#         created_rows = []
#         for employee_id in employee_ids_to:
#             new_assignment = EmployeeAssignRequest(
#                 admin_id=admin_id,
#                 employe_id_from=employee_id_from,
#                 employe_id_to=[employee_id], 
#                 status=role_assign.status,
#                 created_at=datetime.utcnow(),
#                 updated_at=datetime.utcnow(),
#             )
#             db.add(new_assignment)
#             created_rows.append(new_assignment)

        
#         db.commit()

        
#         for row in created_rows:
#             db.refresh(row)

#         return {
#             "status": "true",
#             "message": f"Employee Assign Request Send Successfully",
#             "data": [row for row in created_rows]
#         }
#     except SQLAlchemyError as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")



def createRequest(db: Session, role_assign: EmployeeAssignRequestCreate):
    admin_id = role_assign.admin_id
    employee_id_from = role_assign.employe_id_from
    employee_ids_to = role_assign.employe_id_to

    
    employee_from = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == employee_id_from).first()
    if not employee_from:
        return {"status": "false", "message": "Employee ID (from) not found."}

    
    non_existing_ids = []
    for employee_id in employee_ids_to:
        employee_to = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == employee_id).first()
        if not employee_to:
            non_existing_ids.append(employee_id)

    if non_existing_ids:
        return {
            "status": "false",
            "message": f"The following Employee IDs (to) do not exist: {non_existing_ids}."
        }

    
    already_sent_ids = []
    for employee_id in employee_ids_to:
        existing_request = (
            db.query(EmployeeAssignRequest)
            .filter(
                EmployeeAssignRequest.admin_id == admin_id,
                EmployeeAssignRequest.employe_id_from == employee_id_from,
                EmployeeAssignRequest.employe_id_to.contains([employee_id])
            )
            .first()
        )
        if existing_request:
            already_sent_ids.append(employee_id)

    
    if len(already_sent_ids) == len(employee_ids_to):
        return {
            "status": "false",
            "message": f"Requests have already been sent for the following Employee IDs: {already_sent_ids}.",
        }

   
    ids_to_create = [emp_id for emp_id in employee_ids_to if emp_id not in already_sent_ids]

    try:
       
        created_rows = []
        created_names = []
        for employee_id in ids_to_create:
            new_assignment = EmployeeAssignRequest(
                admin_id=admin_id,
                employe_id_from=employee_id_from,
                employe_id_to=[employee_id], 
                status=role_assign.status,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            db.add(new_assignment)
            created_rows.append(new_assignment)
            
            # Get name for response
            emp = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == employee_id).first()
            if emp:
                created_names.append(emp.employe_name)
        
        
        db.commit()

        
        for row in created_rows:
            db.refresh(row)

        # Prepare short list of names
        name_count = len(created_names)
        if name_count > 3:
            first_three = created_names[:3]
            remaining = name_count - 3
            formatted_names = f"{', '.join(first_three)} and {remaining} others"

        else:
            formatted_names = ", ".join(created_names)



        return {
            "status": "true",
            # "message": f"Employee Assign Request sent successfully for the following IDs: {ids_to_create}.",
            "message": f"Employee Assign Request sent successfully for: {formatted_names}.",
            "already_sent": already_sent_ids,
            "data": [row for row in created_rows],
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")



# def fetch_employee_assignments(db: Session, admin_id: Optional[int] = None, employe_id_from: Optional[str] = None):
    
  
#     employee_from_alias = aliased(AdminAddEmployee)

    
#     query = db.query(
#         EmployeeAssignRequest,
#         employee_from_alias.employe_name.label("employee_from_name")
#     ).join(
#         employee_from_alias, 
#         EmployeeAssignRequest.employe_id_from == employee_from_alias.id, 
#         isouter=True
#     )

    
#     if admin_id:
#         query = query.filter(EmployeeAssignRequest.admin_id == admin_id)
#     if employe_id_from:
#         query = query.filter(EmployeeAssignRequest.employe_id_from == employe_id_from)

#     assignments = query.all()

#     results = []
#     for assignment, employee_from_name in assignments:
       
#         employee_to_names = []
#         if assignment.employe_id_to:
#             employee_to_names = [
#                 db.query(AdminAddEmployee.employe_name).filter(
#                     AdminAddEmployee.id == emp_id
#                 ).scalar()
#                 for emp_id in assignment.employe_id_to
#             ]

#         results.append({
#             "assignment_id": assignment.id,
#             "admin_id": assignment.admin_id,
#             "status":assignment.status,
#             "employee_from": {
#                 "id": assignment.employe_id_from,
#                 "name": employee_from_name
#             },
#             "employees_to": [
#                 {"id": emp_id, "name": emp_name} for emp_id, emp_name in zip(assignment.employe_id_to, employee_to_names)
#             ],
#             "created_at": assignment.created_at,
#             "updated_at": assignment.updated_at,
#         })

#     return results
    

from src.AssignRequestRemark.models import AssignRequestRemark

from src.cre_upd_name import get_creator_info


def fetch_employee_assignments(db: Session, admin_id: Optional[int] = None, employe_id_from: Optional[str] = None):
    employee_from_alias = aliased(AdminAddEmployee)

    
    query = db.query(
        EmployeeAssignRequest,
        employee_from_alias.employe_name.label("employee_from_name"),
        employee_from_alias.level.label("employee_level"),
        employee_from_alias.employee_id.label("employee_from_id")

    ).join(
        employee_from_alias,
        EmployeeAssignRequest.employe_id_from == employee_from_alias.id,
        isouter=True
    )

    if admin_id:
        query = query.filter(EmployeeAssignRequest.admin_id == admin_id)
    if employe_id_from:
        query = query.filter(EmployeeAssignRequest.employe_id_from == employe_id_from)

    assignments = query.all()

    results = []
    for assignment, employee_from_name, employee_level , employee_from_id in assignments:
        
        employee_from_role = (
            db.query(AdminRoleCreation.role_name)
            .join(AdminAssignRoleEmployee, AdminAssignRoleEmployee.role_id == AdminRoleCreation.id)
            .filter(AdminAssignRoleEmployee.asign_employe_id == assignment.employe_id_from)
            .scalar()
        )

        employee_to_data = []
        if assignment.employe_id_to:
            for emp_id in assignment.employe_id_to:
                emp_name = db.query(AdminAddEmployee.employe_name).filter(AdminAddEmployee.id == emp_id).scalar()
                emp_level = db.query(AdminAddEmployee.level).filter(AdminAddEmployee.id == emp_id).scalar()
                employee_id = db.query(AdminAddEmployee.employee_id).filter(AdminAddEmployee.id == emp_id).scalar()

                
                emp_role_name = (
                    db.query(AdminRoleCreation.role_name)
                    .join(AdminAssignRoleEmployee, AdminAssignRoleEmployee.role_id == AdminRoleCreation.id)
                    .filter(AdminAssignRoleEmployee.asign_employe_id == emp_id)
                    .scalar()
                )

                employee_to_data.append({
                    "id": emp_id,
                    "name": emp_name,
                    "level": emp_level,
                    "employee_id":employee_id,
                    "role_name": emp_role_name
                })

                remark = db.query(AssignRequestRemark).filter(
                    AssignRequestRemark.admin_id == assignment.admin_id,
                    AssignRequestRemark.employee_asssign_request_id == assignment.id,
                ).all()

            remark_data = []
            for r in remark:
                created_by = None
                admin_emp_id = None

                if r.employee_id:
                    created_by = "employee"
                    admin_emp_id = r.employee_id 
                else:
                    created_by = "admin"
                    admin_emp_id = r.admin_id

                created_by_data = get_creator_info(admin_emp_id,created_by,db)

                r_dict = {key: value for key, value in r.__dict__.items() if not key.startswith("_")}
                r_dict["creater_info"] = created_by_data  # ? adding to dictionary
                remark_data.append(r_dict)

        results.append({
            "assignment_id": assignment.id,
            "admin_id": assignment.admin_id,
            "status": assignment.status,
            "employee_from": {
                "id": assignment.employe_id_from,
                "name": employee_from_name,
                "level": employee_level,
                "employee_id":employee_from_id,
                "role_name": employee_from_role
            },
            "employees_to": employee_to_data,
            "remark": remark_data,

            "created_at": assignment.created_at,
            "updated_at": assignment.updated_at,
        })

    return results



from src.AssignRequestRemark.models import AssignRequestRemark


def update_status(db: Session, admin_id: int, request_id: int, new_status: str,employee_id: Optional[str] = None, remark: Optional[str] = None):
    
    assignment_request = (
        db.query(EmployeeAssignRequest)
        .filter(EmployeeAssignRequest.id == request_id, EmployeeAssignRequest.admin_id == admin_id)
        .first()
    )
    if not assignment_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee assignment request not found with the given admin id and request id.",
        )

    try:
        
        assignment_request.status = new_status
        assignment_request.updated_at = get_current_datetime()

        
        if new_status == "Approved":
            
            role_assign = (
                db.query(RoleAssignByLevel)
                .filter(RoleAssignByLevel.admin_id == admin_id,
                        RoleAssignByLevel.employe_id_from == assignment_request.employe_id_from)
                .first()
            )

            
            if role_assign:
                current_to_ids = set(role_assign.employe_id_to)  
            else:
                current_to_ids = set()  

           
            for emp_id in assignment_request.employe_id_to:
                current_to_ids.add(emp_id)

           
            updated_to_ids = list(current_to_ids)

           
            if role_assign:
                role_assign.employe_id_to = updated_to_ids
                role_assign.updated_at = get_current_datetime()
            else:
                new_role_assign = RoleAssignByLevel(
                    admin_id=admin_id,
                    employe_id_from=assignment_request.employe_id_from,
                    employe_id_to=updated_to_ids,
                    created_at=get_current_datetime(),
                    updated_at=get_current_datetime()
                )
                db.add(new_role_assign)

        
        db.commit()
        db.refresh(assignment_request)

        remarkdb = AssignRequestRemark(
            admin_id=admin_id,
            employee_id=employee_id,
            employee_asssign_request_id=assignment_request.id,
            status=new_status,
            remark= remark if remark else "No remark provided",
        )
        db.add(remarkdb)
        db.commit()


        return {
            "status": "true",
            "message": "Status updated successfully",
            "data": assignment_request,
        }

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )
    


    



def process_delete_request(db: Session, admin_id: int, from_id: str, request_id: int):
   
    assignment_request = (
        db.query(EmployeeAssignRequest)
        .filter(
            EmployeeAssignRequest.id == request_id,
            EmployeeAssignRequest.admin_id == admin_id,
            EmployeeAssignRequest.employe_id_from == from_id
        )
        .first()
    )

    
    if not assignment_request:
        return {
            "status": "false",
            "message": f"Request ID {request_id}, Admin ID {admin_id}, or From ID {from_id} not found in the database."
        }

    try:
       
        db.delete(assignment_request)
        db.commit()

        return {
            "status": "true",
            "message": "Request deleted successfully."
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
