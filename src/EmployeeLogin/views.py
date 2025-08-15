from fastapi import HTTPException, Depends, APIRouter, Header,Body
from sqlmodel import Session
from src.database import get_db
from src.EmployeeLogin.service import login,login_with_email,login_with_phone
from src.parameter import get_token
from typing import List, Optional
router = APIRouter()

@router.post("/")
def employee_login(email: str = Body(...), password: str = Body(...),auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return login(db=db, email=email, password=password)
    return inner_get_plan(auth_token)



@router.post("/EmployeeloginWithEmail")
def employee_login_with_email(employe_email_id: str = Body(..., embed=True, alias="employe_email_id"),auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return login_with_email(db=db, employe_email_id=employe_email_id)
    
    return inner_get_plan(auth_token)



@router.post("/EmployeeloginWithPhone")
def employee_login_with_phone(
             phone: str = Body(..., embed=True, alias="phone"),
             auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             device_type: Optional[str] = Body(None, embed=True, alias="device_type"),
             device_token: Optional[str] = Body(None, embed=True, alias="device_token"),
             db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return login_with_phone(db=db, phone=phone, device_type=device_type, device_token=device_token)

    return inner_get_plan(auth_token)