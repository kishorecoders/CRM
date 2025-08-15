from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session
from src.database import get_db
from .models import Setting, SettingCreate
from .service import create, get_all_setting, update, \
    get_setting_by_employe_id_fun, delete_setting_by_id_fun
from src.parameter import get_token

router = APIRouter()


@router.get("/showallsettings")
def get_all_setting_details(auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                            db: Session = Depends(get_db)):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    else:
        return get_all_setting(db=db)


@router.post("/Createsettings")
def create_setting_details(setting_create: SettingCreate,
                           auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                           db: Session = Depends(get_db)):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    else:
        return create(db=db, setting_create=setting_create)


@router.get("/Showsettings/{admin_id}")
def get_setting_by_employe_id(admin_id: str, employe_id: Optional[str] = None,
                              auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                              db: Session = Depends(get_db)):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    else:
        return get_setting_by_employe_id_fun(db=db, admin_id=admin_id, employe_id=employe_id)


@router.put("/Updatesettings/{setting_id}")
def update_setting_details(setting_id: int, setting_update: SettingCreate,
                           auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                           db: Session = Depends(get_db)):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    else:
        return update(setting_id=setting_id, setting_update=setting_update, db=db)


@router.delete("/deletesettings/{id}")
def delete_setting_by_id(id: int, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                         db: Session = Depends(get_db)):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    else:
        return delete_setting_by_id_fun(id=id, db=db)
