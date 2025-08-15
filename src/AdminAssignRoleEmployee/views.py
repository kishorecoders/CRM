from typing import List
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from src.AdminAssignRoleEmployee.models import AdminAssignRoleEmployee,AdminAssignRoleEmployeeCreate
from src.AdminAssignRoleEmployee.service import create,get_all_assign_role,get_assign_role_by_admin_id,update,get_module_by_admin_id,show_role_by_user
from src.parameter import get_token

router = APIRouter()

@router.get("/")
def get_all_assgin_role_details(auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_all_assign_role(db=db)
    
    return inner_get_plan(auth_token)


@router.post("/")
def create_role_assign_details(
    admin_assign_role: AdminAssignRoleEmployeeCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return create(db=db, admin_assign_role=admin_assign_role)

    return inner_get_plan(auth_token)


@router.get("/{admin_id}")
def read_role_assign_by_admin(admin_id: int, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_assign_role_by_admin_id(admin_id=admin_id, db=db)
    
    return inner_get_plan(auth_token)    


@router.get("showmodulebyadmin/{admin_id}")
def read_module_by_admin(admin_id: int, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
        def inner_get_plan(auth_token: str):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return get_module_by_admin_id(admin_id=admin_id, db=db)
    
        return inner_get_plan(auth_token) 
    

@router.put("/{assgin_id}")
def update_role_assign_details(assgin_id:int,admin_assign_role:AdminAssignRoleEmployeeCreate,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db:Session=Depends(get_db)):
       def inner_get_plan(auth_token: str):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return update(assgin_id=assgin_id,admin_assign_role=admin_assign_role,db=db)
    
       return inner_get_plan(auth_token)
         

@router.get("/showrolebyuser/{admin_id}")
def read_role_by_user(
    admin_id: int,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return show_role_by_user(admin_id=admin_id, db=db)

    return inner_get_plan(auth_token)

