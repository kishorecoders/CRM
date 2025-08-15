from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session
from src.database import get_db
from .models import EmployeeFilesCreate,FetchEmployeeFilesRequest
from .service import create,fetch_employee_files
from src.parameter import get_token

router = APIRouter()


# @router.post("/add_employee_files")
# def create_employee_details(setting_create: EmployeeFilesCreate,
#                            auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#                            db: Session = Depends(get_db)):
#     if auth_token != get_token():
#         return {"status": "false", "message": "Unauthorized Request"}
#     else:
#         return create(db=db, setting_create=setting_create)
@router.post("/add_employee_files")
def create_employee_details(
    setting_create: EmployeeFilesCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    
    return create(db=db, setting_create=setting_create)    




@router.post("/get_employee_files")
def get_employee_files(
    request: FetchEmployeeFilesRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

   
    results = fetch_employee_files(db=db, admin_id=request.admin_id, employee_id=request.employee_id)

   
    if not results:
        return {"status": "false", "message": "No records found"}
    
    return {"status": "true", "message": "Employee Files retrieved successfully", "data": results}