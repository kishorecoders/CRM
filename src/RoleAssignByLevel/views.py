from typing import List
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from src.parameter import get_token
from src.RoleAssignByLevel.models import RoleAssignByLevelCreate
from src.RoleAssignByLevel.service import create,get_employee_assignments,delete_employee_from_to_service,get_employee_assignments_by_from_id,update_employee_to_list_service,delete_employee_first_level,transfer_leads_to_another_employee
from sqlalchemy import exc
from typing import Dict
from fastapi import APIRouter, Depends, Header, HTTPException, Body
from typing import Optional, List
from typing import Optional, Union
router = APIRouter()


@router.post("/employeeAssign")
def create_role_assign_details(
    role_assign: RoleAssignByLevelCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    
    
    return create(db=db, role_assign=role_assign)




@router.post("/getEmployeeAssignByAdmin")
def get_role_assign_details(
    admin_id: int = Body(..., embed=True),  
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    
    return get_employee_assignments(db=db, admin_id=admin_id)







@router.post("/employeeAssignListByFromEmployee")
def get_role_assign_details_by_from_id(
    admin_id: int = Body(..., embed=True),
    employe_id_from: Optional[Union[str, int]] = Body(None, embed=True),
    role_type: Optional[str] = Body(None, embed=True),
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    return get_employee_assignments_by_from_id(
        db=db,
        admin_id=admin_id,
        employe_id_from=employe_id_from,
        role_type=role_type
    )









@router.put("/updateEmployeeToList")
def update_employee_to_list(
    admin_id: int,
    employe_id_from: str,
    new_employe_id_to: List[str],
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
 
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    
    updated_role_assignment = update_employee_to_list_service(
        db=db, admin_id=admin_id, employe_id_from=employe_id_from, new_employe_id_to=new_employe_id_to
    )

    return {
        "status": "true",
        "message": "Employee ID list updated successfully",
        "updated_role_assignment": updated_role_assignment
    }




# @router.delete("/deleteEmployeeFromTo/{role_id}/{employee_id_to_remove}")
# def delete_employee_from_to(
#     role_id: int,
#     employee_id_to_remove: str,
#     admin_id: int,
#     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#     db: Session = Depends(get_db)
# ):
    
#     if auth_token != get_token():
#         raise HTTPException(status_code=401, detail="Unauthorized Request")

 
#     updated_role_assignment = delete_employee_from_to_service(
#         db=db, admin_id=admin_id, role_id=role_id, employee_id_to_remove=employee_id_to_remove
#     )

#     return {
#         "status": "true",
#         "message": "Employee ID removed from role assignment",
#         "updated_role_assignment": updated_role_assignment
#     }


@router.post("/deleteEmployeeFromTo")
def delete_employee_from_to(
    admin_id: int = Body(...),
    from_id: str = Body(...),
    to_id: str = Body(...),
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
   
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

  
    updated_role_assignment = delete_employee_from_to_service(
        db=db, admin_id=admin_id, from_id=from_id, to_id=to_id
    )

    return {
        "status": "true",
        "message": "Employee ID removed from employee assignment",
        "updated_role_assignment": updated_role_assignment
    }



@router.post("/deleteEmployeeFrom")
def delete_employee_from(
    admin_id: int = Body(...),
    from_id: str = Body(...),
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    deleted_role_assignment = delete_employee_first_level(
        db=db, admin_id=admin_id, from_id=from_id
    )

    return {
        "status": "true",
        "message": "Employee ID removed from employee assignment",
        "deleted_role_assignment": deleted_role_assignment
    }




@router.post("/leadTransfer")
def lead_transfer(
    admin_id: int = Body(..., embed=True),
    from_employee_id: int = Body(..., embed=True),
    to_employee_id: int = Body(..., embed=True),
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    return transfer_leads_to_another_employee(db=db, admin_id=admin_id, from_employee_id=from_employee_id, to_employee_id=to_employee_id)
