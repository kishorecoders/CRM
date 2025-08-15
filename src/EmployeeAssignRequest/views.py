from typing import List
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from src.parameter import get_token
from src.EmployeeAssignRequest.models import EmployeeAssignRequestCreate,EmployeeAssignRequestFilter,UpdateStatusRequest,DeleteRequest
from src.EmployeeAssignRequest.service import createRequest,fetch_employee_assignments,update_status,process_delete_request
from sqlalchemy import exc
from typing import Dict
from fastapi import APIRouter, Depends, Header, HTTPException, Body
from typing import Optional, List

router = APIRouter()



@router.post("/employeeAssignRequest")
def create_role_assign_details(
    role_assign: EmployeeAssignRequestCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
   
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    
    return createRequest(db=db, role_assign=role_assign)



@router.post("/get_employee_assignments")
def get_employee_assignments(
    filter_params: Optional[EmployeeAssignRequestFilter] = None,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
   
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    admin_id = filter_params.admin_id if filter_params else None
    employe_id_from = filter_params.employe_id_from if filter_params else None

    results = fetch_employee_assignments(db=db, admin_id=admin_id, employe_id_from=employe_id_from)

    if not results:
        return {"status": "false", "message": "No assignments found."}

    return {
        "status": "true",
        "message": f"Found {len(results)} Request",
        "data": results
    }




@router.post("/updateEmployeeAssignRequestStatus")
def update_assignment_status(
    update_request: UpdateStatusRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db),
):
    
    if auth_token != get_token():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized request",
        )

    
    return update_status(
        db=db,
        admin_id=update_request.admin_id,
        employee_id=update_request.employee_id,
        request_id=update_request.request_id,
        new_status=update_request.status,
        remark=update_request.remark,

    )




@router.post("/deleteEmployeeAssignRequest")
def delete_employee_assign_request(
    delete_request: DeleteRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token(): 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized Request"
        )

    
    return process_delete_request(
        db=db,
        admin_id=delete_request.admin_id,
        from_id=delete_request.from_id,
        request_id=delete_request.request_id
    )
