from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew
from src.AdminAddEmployee.models import AdminAddEmployee
from sqlalchemy.orm import Session


creator_info = "creator_info"
updator_info = "updator_info"

def get_creator(admin_id: int, emp_id: str, db: Session) -> dict:

    creator_info = {
        "name": "",
        "id": None,
        "admin_emp_name" :"",
        "admin_emp_short_name" :"",
        "employee_id": ""
    }

    if emp_id:
        empd = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == int(emp_id)).first()
        if empd:
            creator_info = {
                "name": empd.employe_name,
                "admin_emp_name": f"{empd.employe_name}({empd.employee_id})",
                "admin_emp_short_name": f"{empd.employe_name.split()[0]}({empd.employee_id})",
                "id": empd.id,
                "employee_id": empd.employee_id,
                "phone_number": empd.employe_phone_number if empd.employe_phone_number else None

            }
    elif admin_id:
        empd = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == int(admin_id)).first()
        if empd:
            creator_info = {
                "name": empd.full_name,
                "admin_emp_name": f"{empd.full_name}(Admin)",
                "admin_emp_short_name": f"{empd.full_name.split()[0]}(Admin)",
                "id": empd.id,
                "employee_id": "Admin",
                "phone_number": empd.phone_number if empd.phone_number else None

            }

    return creator_info

def get_creator_info(admin_emp_id: int, created_by_type: str, db: Session) -> dict:

    creator_info = {
        "name": "",
        "id": None,
        "admin_emp_name" :"",
        "admin_emp_short_name" :"",
        "employee_id": ""
    }

    if admin_emp_id:
        if created_by_type == 'employee':
            empd = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == int(admin_emp_id)).first()
            if empd:
                creator_info = {
                    "name": empd.employe_name,
                    "admin_emp_name": f"{empd.employe_name}({empd.employee_id})",
                    "admin_emp_short_name": f"{empd.employe_name.split()[0]}({empd.employee_id})",
                    "id": empd.id,
                    "employee_id": empd.employee_id,
                    "phone_number": empd.employe_phone_number if empd.employe_phone_number else None

                }
        elif created_by_type == 'admin':
            empd = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == int(admin_emp_id)).first()
            if empd:
                creator_info = {
                    "name": empd.full_name,
                    "admin_emp_name": f"{empd.full_name}(Admin)",
                    "admin_emp_short_name": f"{empd.full_name.split()[0]}(Admin)",
                    "id": empd.id,
                    "employee_id": "Admin",
                    "phone_number": empd.phone_number if empd.phone_number else None
                }

    return creator_info

def get_creator_updator_info(db: Session ,admin_emp_id:int , 
                             created_by_type:str ,updated_admin_emp_id:int , updated_by_type:str):
    return {
        "creator_info":get_creator_info(admin_emp_id=admin_emp_id ,created_by_type= created_by_type ,db=db),
        "updater_info":get_creator_info(admin_emp_id=updated_admin_emp_id ,created_by_type= updated_by_type ,db=db)
    }

def get_creator_updator_infos(db: Session ,admin_emp_id:int , 
                             created_by_type:str ,updated_admin_emp_id:int , 
                             updated_by_type:str, rejacted_admin_emp_id:int, 
                             rejacted_by_type:str,approve_admin_emp_id = int,
                             approve_by_type = str):
    return {
        "creator_info":get_creator_info(admin_emp_id=admin_emp_id ,created_by_type= created_by_type ,db=db),
        "updater_info":get_creator_info(admin_emp_id=updated_admin_emp_id ,created_by_type= updated_by_type ,db=db),
        "approve_info":get_creator_info(admin_emp_id=approve_admin_emp_id ,created_by_type= approve_by_type ,db=db),
        "rejacted_info":get_creator_info(admin_emp_id=rejacted_admin_emp_id ,created_by_type= rejacted_by_type ,db=db)
    }

