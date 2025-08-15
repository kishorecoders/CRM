from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session
from src.database import get_db
from .models import SettingFilesCreate
from .service import create,delete_file_settings_by_id,get_setting_file_by_admin
from src.parameter import get_token

router = APIRouter()


@router.post("/create_settings_files")
def create_setting_details(setting_create: SettingFilesCreate,
                           auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                           db: Session = Depends(get_db)):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    else:
        return create(db=db, setting_create=setting_create)
    
@router.get("/get_Settings_files/{admin_id}")
def read_setting_file_by_admin(admin_id: str, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    else:
        return get_setting_file_by_admin(admin_id=admin_id, db=db)     
    
@router.delete("/deleteFileSettings/{id}")
def delete_file_settings_by_id_view(id: int, db: Session = Depends(get_db)):
    return delete_file_settings_by_id(id=id, db=db)    
