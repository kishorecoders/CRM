from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status, HTTPException
from src.RoleAssignByLevel.models import RoleAssignByLevel
from src.AdminAddEmployee.models import AdminAddEmployee
from src.AdminAssignRoleEmployee.models import AdminAssignRoleEmployee
from src.AdminRoleCreation.models import AdminRoleCreation
from src.AdminSales.models import AdminSales
from .models import RoleAssignByLevelCreate
from sqlalchemy import exc
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from typing import Optional, Union

def get_current_datetime():
    return datetime.utcnow()



# def create(db: Session, role_assign: RoleAssignByLevelCreate):
#     admin_id = role_assign.admin_id
#     employee_id_from = role_assign.employe_id_from

    
#     employee_from = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == employee_id_from).first()
#     if not employee_from:
#         return {'status': 'false', 'message': 'Employee ID (from) not found.'}

    
#     employee_ids_to = role_assign.employe_id_to
#     if employee_ids_to:
#         for employee_id in employee_ids_to:
#             employee_to = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == employee_id).first()
#             if not employee_to:
#                 return {'status': 'false', 'message': f'Employee ID (to) {employee_id} not found.'}

#     existing_role = db.query(RoleAssignByLevel).filter(
#         RoleAssignByLevel.admin_id == admin_id, 
#         RoleAssignByLevel.employe_id_from == employee_id_from
#     ).first()

#     if existing_role:
#         return {'status': 'false', 'message': 'This Employee assignment already exists for the given admin and employee.'}
    
#     try:
#         db_role_assign = RoleAssignByLevel(**role_assign.dict())
#         db.add(db_role_assign)
#         db.commit()
#         db.refresh(db_role_assign)

#         response = {
#             'status': 'true',
#             'message': "Employee Assignment Successfully",
#             'data': db_role_assign
#         }
#         return response
#     except exc.SQLAlchemyError as e:
#         db.rollback()  
#         raise HTTPException(status_code=500, detail=str(e))
def create(db: Session, role_assign: RoleAssignByLevelCreate):
    admin_id = role_assign.admin_id
    employee_id_from = role_assign.employe_id_from

    
    employee_from = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == employee_id_from).first()
    if not employee_from:
        return {'status': 'false', 'message': 'Employee ID (from) not found.'}

   
    employee_ids_to = role_assign.employe_id_to
    if employee_ids_to:
        for employee_id in employee_ids_to:
            employee_to = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == employee_id).first()
            if not employee_to:
                return {'status': 'false', 'message': f'Employee ID (to) {employee_id} not found.'}

    
    existing_role = db.query(RoleAssignByLevel).filter(
        RoleAssignByLevel.admin_id == admin_id, 
        RoleAssignByLevel.employe_id_from == employee_id_from
    ).first()

    try:
        if existing_role:
           
            existing_role.employe_id_to = list(set(existing_role.employe_id_to + employee_ids_to))
            existing_role.updated_at = get_current_datetime()  
            db.commit()
            db.refresh(existing_role)
            response = {
                'status': 'true',
                'message': "Employee Assignment Updated Successfully",
                'data': existing_role
            }
        else:
            
            db_role_assign = RoleAssignByLevel(**role_assign.dict())
            db.add(db_role_assign)
            db.commit()
            db.refresh(db_role_assign)
            response = {
                'status': 'true',
                'message': "Employee Assignment Successfully Created",
                'data': db_role_assign
            }
        return response
    except exc.SQLAlchemyError as e:
        db.rollback()  
        raise HTTPException(status_code=500, detail=str(e))



 

# def get_employee_assignments(db: Session, admin_id: int):
#     role_assignments = db.query(RoleAssignByLevel).filter(
#         RoleAssignByLevel.admin_id == admin_id
#     ).all()

#     if not role_assignments:
#         return {'status': 'false', 'message': 'No Employee assignments found for this admin.'}

#     response_data = []

#     try:
#         for role in role_assignments:
            
#             employee_from = db.query(AdminAddEmployee).filter(
#                 AdminAddEmployee.id == role.employe_id_from  
#             ).first()
            
           
#             if employee_from:
#                 assigned_role_from = db.query(AdminAssignRoleEmployee).filter(
#                     AdminAssignRoleEmployee.employe_id== role.employe_id_from,
#                     AdminAssignRoleEmployee.admin_id == admin_id
#                 ).first()
                
                
#                 if assigned_role_from:
#                     role_details_from = db.query(AdminRoleCreation).filter(
#                         AdminRoleCreation.id == assigned_role_from.role_id
#                     ).first()
#                     employee_from_role_data = role_details_from.dict() if role_details_from else None
#                 else:
#                     employee_from_role_data = None
#             else:
#                 employee_from_role_data = None

            
#             employees_to_details = []
#             for emp_id in role.employe_id_to:
#                 emp = db.query(AdminAddEmployee).filter(
#                     AdminAddEmployee.id == emp_id  
#                 ).first()
                
#                 if emp:
#                     emp_data = emp.dict()

                  
#                     assigned_role = db.query(AdminAssignRoleEmployee).filter(
#                         AdminAssignRoleEmployee.employe_id == emp_id,
#                         AdminAssignRoleEmployee.admin_id == admin_id
#                     ).first()

                   
#                     if assigned_role:
#                         role_details = db.query(AdminRoleCreation).filter(
#                             AdminRoleCreation.id == assigned_role.role_id
#                         ).first()
#                         emp_data['assigned_role'] = role_details.dict() if role_details else None
#                     else:
#                         emp_data['assigned_role'] = None

#                     employees_to_details.append(emp_data)

          
#             role_data = {
#                 "id": role.id,
#                 "admin_id": role.admin_id,
#                 "created_at": role.created_at,
#                 "updated_at": role.updated_at,
#                 "employe_id_from": {
#                     "id": role.employe_id_from,
#                     "details": employee_from.dict() if employee_from else None,
#                     "assigned_role": employee_from_role_data  
#                 },
#                 "employe_id_to": {
#                     "ids": role.employe_id_to,
#                     "details": employees_to_details
#                 }
#             }

#             response_data.append(role_data)

#         response = {
#             'status': 'true',
#             'message': 'Employee records fetched successfully',
#             'data': response_data
#         }
#         return response

#     except SQLAlchemyError as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))
def get_employee_assignments(db: Session, admin_id: int):
    role_assignments = db.query(RoleAssignByLevel).filter(
        RoleAssignByLevel.admin_id == admin_id
    ).all()

    if not role_assignments:
        return {'status': 'false', 'message': 'No Employee assignments found for this admin.'}

    response_data = []

    try:
        for role in role_assignments:
            # Fetch employee_from details
            employee_from = db.query(AdminAddEmployee).filter(
                AdminAddEmployee.id == role.employe_id_from
            ).first()

            # Fetch roles for employee_from
            if employee_from:
                assigned_role_from = db.query(AdminAssignRoleEmployee).filter(
                    AdminAssignRoleEmployee.asign_employe_id == role.employe_id_from,
                    AdminAssignRoleEmployee.admin_id == admin_id
                ).first()
                
                role_details_from = None
                if assigned_role_from:
                    role_details_from = db.query(AdminRoleCreation).filter(
                        AdminRoleCreation.id == assigned_role_from.role_id
                    ).first()
                
                employee_from_role_data = role_details_from.dict() if role_details_from else None
            else:
                employee_from_role_data = None

            # Fetch leads for employee_from
            leads_from = db.query(AdminSales).filter(
                AdminSales.allocated_emplyee_id == role.employe_id_from
            ).all()
            leads_from_details = [lead.dict() for lead in leads_from]

            # Fetch employee_to details
            employees_to_details = []
            for emp_id in role.employe_id_to:
                emp = db.query(AdminAddEmployee).filter(
                    AdminAddEmployee.id == emp_id
                ).first()

                if emp:
                    emp_data = emp.dict()

                    # Fetch roles for employee_to
                    assigned_role = db.query(AdminAssignRoleEmployee).filter(
                        AdminAssignRoleEmployee.asign_employe_id == emp_id,
                        AdminAssignRoleEmployee.admin_id == admin_id
                    ).first()

                    role_details = None
                    if assigned_role:
                        role_details = db.query(AdminRoleCreation).filter(
                            AdminRoleCreation.id == assigned_role.role_id
                        ).first()
                    
                    emp_data['assigned_role'] = role_details.dict() if role_details else None

                    # Fetch leads for employee_to
                    leads_to = db.query(AdminSales).filter(
                        AdminSales.allocated_emplyee_id == emp_id
                    ).all()
                    emp_data['assigned_leads'] = [lead.dict() for lead in leads_to]

                    employees_to_details.append(emp_data)

            # Build response data
            role_data = {
                "id": role.id,
                "admin_id": role.admin_id,
                "created_at": role.created_at,
                "updated_at": role.updated_at,
                "employe_id_from": {
                    "id": role.employe_id_from,
                    "details": employee_from.dict() if employee_from else None,
                    "assigned_role": employee_from_role_data,
                    "assigned_leads": leads_from_details
                },
                "employe_id_to": {
                    "ids": role.employe_id_to,
                    "details": employees_to_details
                }
            }

            response_data.append(role_data)

        response = {
            'status': 'true',
            'message': 'Employee and lead assignments fetched successfully.',
            'data': response_data
        }
        return response

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))






# def get_employee_assignments_by_from_id(db: Session, admin_id: int, employe_id_from: Optional[Union[int, str]] = None):
#     # Determine if we should fetch all or filter by one employee
#     if employe_id_from in ("", None):
#         role_assignments = db.query(RoleAssignByLevel).filter(
#             RoleAssignByLevel.admin_id == admin_id
#         ).all()
#     else:
#         role_assignments = db.query(RoleAssignByLevel).filter(
#             RoleAssignByLevel.admin_id == admin_id,
#             RoleAssignByLevel.employe_id_from == int(employe_id_from)
#         ).all()

#     if not role_assignments:
#         return {'status': 'false', 'message': 'No Employee assignments found for this admin.'}

#     response_data = []

#     try:
#         for role in role_assignments:
#             employee_from = db.query(AdminAddEmployee).filter(
#                 AdminAddEmployee.id == role.employe_id_from
#             ).first()

#             if employee_from:
#                 assigned_role_from = db.query(AdminAssignRoleEmployee).filter(
#                     AdminAssignRoleEmployee.employe_id == role.employe_id_from,
#                     AdminAssignRoleEmployee.admin_id == admin_id
#                 ).first()

#                 role_details_from = None
#                 if assigned_role_from:
#                     role_details_from = db.query(AdminRoleCreation).filter(
#                         AdminRoleCreation.id == assigned_role_from.role_id
#                     ).first()

#                 leads_from_employee = db.query(AdminSales).filter(
#                     AdminSales.allocated_emplyee_id == role.employe_id_from
#                 ).all()

#                 employee_from_lead_details = [lead.dict() for lead in leads_from_employee]
#                 employee_from_role_data = role_details_from.dict() if role_details_from else None
#             else:
#                 employee_from_lead_details = []
#                 employee_from_role_data = None

#             employees_to_details = []
#             for emp_id in role.employe_id_to:
#                 emp = db.query(AdminAddEmployee).filter(
#                     AdminAddEmployee.id == emp_id
#                 ).first()

#                 if emp:
#                     emp_data = emp.dict()
#                     assigned_role = db.query(AdminAssignRoleEmployee).filter(
#                         AdminAssignRoleEmployee.employe_id == emp_id,
#                         AdminAssignRoleEmployee.admin_id == admin_id
#                     ).first()

#                     if assigned_role:
#                         role_details = db.query(AdminRoleCreation).filter(
#                             AdminRoleCreation.id == assigned_role.role_id
#                         ).first()
#                         emp_data['assigned_role'] = role_details.dict() if role_details else None
#                     else:
#                         emp_data['assigned_role'] = None

#                     lead_details = db.query(AdminSales).filter(
#                         AdminSales.allocated_emplyee_id == emp_id
#                     ).all()

#                     emp_data['lead_details'] = [lead.dict() for lead in lead_details]
#                     employees_to_details.append(emp_data)

#             role_data = {
#                 "id": role.id,
#                 "admin_id": role.admin_id,
#                 "created_at": role.created_at,
#                 "updated_at": role.updated_at,
#                 "employe_id_from": {
#                     "id": role.employe_id_from,
#                     "details": employee_from.dict() if employee_from else None,
#                     "assigned_role": employee_from_role_data,
#                     "lead_details": employee_from_lead_details
#                 },
#                 "employe_id_to": {
#                     "ids": role.employe_id_to,
#                     "details": employees_to_details
#                 }
#             }

#             response_data.append(role_data)

#         return {
#             'status': 'true',
#             'message': 'Employee records fetched successfully',
#             'data': response_data
#         }

#     except SQLAlchemyError as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))
        
from src.TimeConfig.models import TimeConfig

        
def get_employee_assignments_by_from_id(db: Session, admin_id: int, employe_id_from: Optional[Union[int, str]] = None,role_type: Optional[str] = None):
    try:
        if employe_id_from in ("", 0 ,None):
            # Fetch all employees directly from AdminAddEmployee for this admin
            all_employees = db.query(AdminAddEmployee).filter(
                AdminAddEmployee.admin_id == admin_id
            ).all()

            if not all_employees:
                return {'status': 'false', 'message': 'No employees found for this admin.'}

            response_data = []

            for emp in all_employees:
                emp_data = emp.dict()

                shift_map = {
                    "shift-1": "1st",
                    "shift-2": "2nd",
                    "shift-3": "3rd",
                    "general": "general"
                }

                start_time = ""
                end_time = ""

                if emp.shift_name:
                    shift_key = shift_map.get(emp.shift_name.strip(), "").lower()
                    
                    if shift_key:
                        time_config = db.query(TimeConfig).filter(
                            TimeConfig.admin_id == admin_id,
                            TimeConfig.shift_name == emp.shift_name
                        ).first()

                        if time_config:
                            start_time = getattr(time_config, f"start_time_{shift_key}", "")
                            end_time = getattr(time_config, f"end_time_{shift_key}", "")
                        
                emp_data['end_time'] = start_time
                emp_data['start_time'] = end_time

                # Assigned role
                assigned_role = db.query(AdminAssignRoleEmployee).filter(
                    AdminAssignRoleEmployee.asign_employe_id == emp.id,
                    AdminAssignRoleEmployee.admin_id == admin_id
                ).first()
                

                if assigned_role:
                    role_details = db.query(AdminRoleCreation).filter(
                        AdminRoleCreation.id == assigned_role.role_id
                    ).first()
                    emp_data['assigned_role'] = role_details.dict() if role_details else None
                    emp_data['assign_status'] = "Assign"
                    emp_data['role_name'] = role_details.role_name
                else:
                    emp_data['assigned_role'] = None
                    emp_data['assign_status'] = "Not Assign"
                    emp_data['role_name'] = None

                if role_type:
                    if not role_details or not getattr(role_details, role_type, False) or not assigned_role:
                        continue
                                                
                # Sales leads
                lead_details = db.query(AdminSales).filter(
                    AdminSales.allocated_emplyee_id == emp.id
                ).all()

                emp_data['lead_details'] = [lead.dict() for lead in lead_details]

                response_data.append(emp_data)

            return {
                'status': 'true',
                'message': 'All employees fetched successfully',
                'data': response_data
            }

        else:
            # When employe_id_from is provided ? your original logic
            role_assignments = db.query(RoleAssignByLevel).filter(
                RoleAssignByLevel.admin_id == admin_id,
                RoleAssignByLevel.employe_id_from == int(employe_id_from)
            ).all()

            if not role_assignments:
                return {
                'status': 'true', 
                'message': 'No Employee assignments found for this admin.',
                'data': []
                }

            response_data = []

            for role in role_assignments:
                employee_from = db.query(AdminAddEmployee).filter(
                    AdminAddEmployee.id == role.employe_id_from
                ).first()

                if employee_from:
                    assigned_role_from = db.query(AdminAssignRoleEmployee).filter(
                        AdminAssignRoleEmployee.asign_employe_id == role.employe_id_from,
                        AdminAssignRoleEmployee.admin_id == admin_id
                    ).first()

                    role_details_from = None
                    if assigned_role_from:
                        role_details_from = db.query(AdminRoleCreation).filter(
                            AdminRoleCreation.id == assigned_role_from.role_id
                        ).first()

                    leads_from_employee = db.query(AdminSales).filter(
                        AdminSales.allocated_emplyee_id == role.employe_id_from
                    ).all()

                    employee_from_lead_details = [lead.dict() for lead in leads_from_employee]
                    employee_from_role_data = role_details_from.dict() if role_details_from else None
                else:
                    employee_from_lead_details = []
                    employee_from_role_data = None

                employees_to_details = []
                for emp_id in role.employe_id_to:
                    emp = db.query(AdminAddEmployee).filter(
                        AdminAddEmployee.id == emp_id
                    ).first()

                    rolec = db.query(RoleAssignByLevel).filter(
                        RoleAssignByLevel.admin_id == admin_id
                    ).all()

                    emp_from_list = [
                        role.employe_id_from
                        for role in rolec
                        if emp_id in role.employe_id_to
                    ]


                    if emp:
                        emp_data = emp.dict()
                        
                        shift_map = {
                            "shift-1": "1st",
                            "shift-2": "2nd",
                            "shift-3": "3rd",
                            "general": "general"
                        }

                        start_time = ""
                        end_time = ""

                        if emp.shift_name:
                            shift_key = shift_map.get(emp.shift_name.strip(), "").lower()
                            
                            if shift_key:
                                time_config = db.query(TimeConfig).filter(
                                    TimeConfig.admin_id == admin_id,
                                    TimeConfig.shift_name == emp.shift_name
                                ).first()

                                if time_config:
                                    start_time = getattr(time_config, f"start_time_{shift_key}", "")
                                    end_time = getattr(time_config, f"end_time_{shift_key}", "")
                                
                        emp_data['end_time'] = start_time
                        emp_data['start_time'] = end_time
                        emp_data['list_emp'] = emp_from_list
                        
                        
                        assigned_role = db.query(AdminAssignRoleEmployee).filter(
                            AdminAssignRoleEmployee.asign_employe_id == emp_id,
                            AdminAssignRoleEmployee.admin_id == admin_id
                        ).first()

                        if assigned_role:
                            role_details = db.query(AdminRoleCreation).filter(
                                AdminRoleCreation.id == assigned_role.role_id
                            ).first()
                            emp_data['assigned_role'] = role_details.dict() if role_details else None
                            emp_data['assign_status'] = "Assign"
                            emp_data['role_name'] = role_details.role_name
                            
                        else:
                            emp_data['assigned_role'] = None
                            emp_data['assign_status'] = "Not Assign"
                            emp_data['role_name'] = None



                        if role_type:
                            if not role_details or not getattr(role_details, role_type, False) or not assigned_role:
                                continue

                        lead_details = db.query(AdminSales).filter(
                            AdminSales.allocated_emplyee_id == emp_id
                        ).all()

                        emp_data['lead_details'] = [lead.dict() for lead in lead_details]
                        employees_to_details.append(emp_data)

                role_data = {
                    "id": role.id,
                    "admin_id": role.admin_id,
                    "created_at": role.created_at,
                    "updated_at": role.updated_at,
                    "employe_id_from": {
                        "id": role.employe_id_from,
                        "details": employee_from.dict() if employee_from else None,
                        "assigned_role": employee_from_role_data,
                        "lead_details": employee_from_lead_details
                    },
                    "employe_id_to": {
                        "ids": role.employe_id_to,
                        "details": employees_to_details
                    }
                }

                response_data.append(role_data)

            return {
                'status': 'true',
                'message': 'Employee records fetched successfully',
                'data': response_data
            }

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))






def update_employee_to_list_service(
    db: Session, admin_id: int, employe_id_from: str, new_employe_id_to: List[str]
) -> RoleAssignByLevel:
    try:
       
        role_assignment = db.query(RoleAssignByLevel).filter(
            RoleAssignByLevel.admin_id == admin_id,
            RoleAssignByLevel.employe_id_from == employe_id_from
        ).first()

        if not role_assignment:
            raise HTTPException(status_code=404, detail="Employee assignment not found.")

        
        role_assignment.employe_id_to = new_employe_id_to

     
        db.add(role_assignment)
        db.commit()
        db.refresh(role_assignment)

        return role_assignment

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))




# def delete_employee_from_to_service(
#     db: Session, admin_id: int, role_id: int, employee_id_to_remove: str
# ) -> RoleAssignByLevel:
#     try:
        
#         role_assignment = db.query(RoleAssignByLevel).filter(
#             RoleAssignByLevel.id == role_id,
#             RoleAssignByLevel.admin_id == admin_id
#         ).first()

#         if not role_assignment:
#             raise HTTPException(status_code=404, detail="Role assignment not found.")

       
#         if employee_id_to_remove not in role_assignment.employe_id_to:
#             raise HTTPException(status_code=404, detail="Employee ID not found in employe_id_to.")

       
#         updated_employee_id_to = role_assignment.employe_id_to.copy()
#         updated_employee_id_to.remove(employee_id_to_remove)
#         role_assignment.employe_id_to = updated_employee_id_to  
       

      
#         db.add(role_assignment)
#         db.commit()
#         db.refresh(role_assignment)

#         return role_assignment

#     except SQLAlchemyError as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail="Database error: " + str(e))
    

def delete_employee_from_to_service(
    db: Session, admin_id: int, from_id: str, to_id: str
) -> RoleAssignByLevel:
    try:
        
        role_assignment = db.query(RoleAssignByLevel).filter(
            RoleAssignByLevel.admin_id == admin_id,
            RoleAssignByLevel.employe_id_from == from_id
        ).first()

        if not role_assignment:
            raise HTTPException(status_code=404, detail="Employee assignment not found.")

       
        if to_id not in role_assignment.employe_id_to:
            raise HTTPException(status_code=404, detail="Employee ID not found in employe_id_to.")

       
        updated_employee_id_to = role_assignment.employe_id_to.copy()
        updated_employee_id_to.remove(to_id)
        role_assignment.employe_id_to = updated_employee_id_to  

        
        db.add(role_assignment)
        db.commit()
        db.refresh(role_assignment)

        return role_assignment

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    




def delete_employee_first_level(
    db: Session, admin_id: int, from_id: str
) -> RoleAssignByLevel:
    try:
        role_assignment = db.query(RoleAssignByLevel).filter(
            RoleAssignByLevel.admin_id == admin_id,
            RoleAssignByLevel.employe_id_from == from_id
        ).first()

        if not role_assignment:
            raise HTTPException(status_code=404, detail="Employee assignment not found.")

        db.delete(role_assignment)
        db.commit()

        return role_assignment

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    



def transfer_leads_to_another_employee(db: Session, admin_id: int, from_employee_id: int, to_employee_id: int):
   
    leads = db.query(AdminSales).filter(
        AdminSales.allocated_emplyee_id == from_employee_id
    ).all()

    if not leads:
        return {'status': 'false', 'message': 'No leads found for this employee.'}

    try:
       
        for lead in leads:
            lead.allocated_emplyee_id = to_employee_id
            db.add(lead)

        db.commit()  

        
        updated_leads = db.query(AdminSales).filter(
            AdminSales.allocated_emplyee_id == to_employee_id
        ).all()

        
        lead_details = [
            {
                "id": lead.id,
                "lead_source": lead.lead_source,
                "name": lead.name,
                "business_name": lead.business_name,
                "email": lead.email,
                "contact_details": lead.contact_details,
                "lead_status": lead.lead_status,
            }
            for lead in updated_leads
        ]

        response = {
            'status': 'true',
            'message': 'Leads transferred successfully',
            'data': lead_details
        }

        return response

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

