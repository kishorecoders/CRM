from typing import List,Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header, Request, Form, Body, Request
from sqlmodel import Session
from src.database import get_db
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew, SuperAdminUserAddNewCreate, SuperAdminUserAddNewUpdate, UpdatePassword, PromptTypeCreate,UserExistenceCheck
from src.SuperAdminUserAddNew.service import create, get_user_by_id, update, get_all_users, update_password, get_prompt_type, create_prompt_type, send_reset_email, verify_token, invalidate_token,delete_superadmin_user_by_id,revert_superadmin_user_by_id,deactivate_superadmin_user_by_id
from src.parameter import get_token
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse , RedirectResponse
from apscheduler.schedulers.background import BackgroundScheduler

router = APIRouter()



@router.get("/ShowAllUserForm")
def get_all_admin_data(
    search: Optional[str] = None,
    filter: Optional[str] = None,
    is_deleted: Optional[bool] = None,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_all_users(db=db, search=search, filter=filter, is_deleted=is_deleted)

    return inner_get_plan(auth_token)



@router.post("/CreateUserNewForm")
def create_plan(super_admin_user_add_new: SuperAdminUserAddNewCreate,
                auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return create(db=db, super_admin_user_add_new=super_admin_user_add_new)

    return inner_get_plan(auth_token)


@router.get("/ShowUserFormByAdminId/{admin_id}")
def read_plan_by_id(admin_id: int, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                    db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_user_by_id(admin_id=admin_id, db=db)

    return inner_get_plan(auth_token)


@router.put("/UpdateUserForm/{admin_id}")
def update_plan(admin_id: int, super_admin_user_add_new: SuperAdminUserAddNewUpdate,
                auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return update(admin_id=admin_id, updated_data=super_admin_user_add_new, db=db)

    return inner_get_plan(auth_token)

# @router.put("/updatepassword/{admin_id}")
# def update_password_details(
#     admin_id: int,
#     password_data: UpdatePassword,
#     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#     db: Session = Depends(get_db)
# ):
#     if auth_token != get_token():
#         return {"status": "false", "message": "Unauthorized Request"}
#     else:
#         return update_password(admin_id=admin_id, password_data=password_data, db=db

# Set up Jinja2 templates
templates = Jinja2Templates(directory="src/templates")

@router.post("/request-password-reset")
def request_password_reset(email: str = Body(..., embed=True, alias="email"), db: Session = Depends(get_db)):
    return send_reset_email(email=email, db=db)


@router.get("/reset-password", response_class=HTMLResponse)
def reset_password_form(request: Request, token: str):
    
    response = templates.TemplateResponse("reset_password.html", {"request": request, "token": token})
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    
    return response

@router.post("/reset-password")
def reset_password(
    request: Request,
    token: str = Form(...), 
    password: str = Form(...), 
    confirm_password: str = Form(...), 
    db: Session = Depends(get_db)
):
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    admin_id = verify_token(token, db)
    password_data = UpdatePassword(password=password)
    update_password(admin_id=admin_id, password_data=password_data, db=db)
    
    invalidate_token
    
    return templates.TemplateResponse("password_update_success.html", {"request": request})
    


@router.post("/create-prompt-type")
def create_prompt_type_details(prompt_type_create: PromptTypeCreate, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    else:
        return create_prompt_type(db=db, prompt_type_create=prompt_type_create) 
    


@router.get("/get-prompt-type")
def read_prompt_type_details(auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    else:
        return get_prompt_type(db=db)    





# @router.delete("/delete_superadmin_user_by_id/{admin_id}")
# def delete_superadmin_user_by_user_id(
#     admin_id: int,
#     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#     db: Session = Depends(get_db)
# ):
#     def inner_user(auth_token: str):
#         if auth_token != get_token():
#             raise HTTPException(status_code=403, detail="Unauthorized Request")
    
#         return delete_superadmin_user_by_id(admin_id=admin_id, db=db)
#     return inner_user(auth_token)
@router.delete("/delete_superadmin_user_by_id/{admin_id}")
def delete_superadmin_user_by_user_id(
    admin_id: int,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=403, detail="Unauthorized Request")
    
    
    return delete_superadmin_user_by_id(admin_id=admin_id, db=db)



@router.put("/revert_superadmin_user_by_id/{admin_id}")
def revert_superadmin_user(
    admin_id: int,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
    ):
    def inner_user(auth_token: str):
        if auth_token != get_token():
            raise HTTPException(status_code=403, detail="Unauthorized Request")
        else:
            return revert_superadmin_user_by_id(admin_id=admin_id, db=db)
        
    return inner_user(auth_token)




@router.put("/deactivate_superadmin_user_by_id/{admin_id}")
def deactivate_superadmin_user_by_user_id(
    admin_id: int,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
    ):
    def inner_user(auth_token: str):
        if auth_token != get_token():
            raise HTTPException(status_code=403, detail="Unauthorized Request")
    
        return deactivate_superadmin_user_by_id(admin_id=admin_id, db=db)
    return inner_user(auth_token)


# @router.post("/check_user_existence/")
# async def check_user_existence(
#     user_check: UserExistenceCheck,  
#     db: Session = Depends(get_db)  
# ):
#     mobile_number = user_check.mobile_number
#     email = user_check.email

    
#     if mobile_number:
#         existing_mobile = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.phone_number == mobile_number).first()
#         if existing_mobile:
#             return {"status":"true","message": "Mobile number already exists."}

    
#     if email:
#         existing_email = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.email == email).first()
#         if existing_email:
#             return {"status":"true","message": "Email already exists."}

#     return {"status":"false","message": "Mobile number or email not exist"}


@router.post("/check_user_existence/")
async def check_user_existence(
    user_check: UserExistenceCheck,  
    db: Session = Depends(get_db)  
):
    mobile_number = user_check.mobile_number
    email = user_check.email

    if mobile_number:
        existing_mobile = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.phone_number == mobile_number).first()
        if existing_mobile:
            return {"status": "true", "message": "Mobile number already exists."}

    if email:
        existing_email = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.email == email).first()
        if existing_email:
            return {"status": "true", "message": "Email already exists."}

    return {"status": "false", "message": "Mobile number or email does not exist"}
