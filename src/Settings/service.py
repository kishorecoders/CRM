from .models import Setting, SettingCreate
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status, HTTPException

from ..SettingsFiles.models import SettingFiles


def get_all_setting(db: Session):
    data = db.query(Setting).order_by(Setting.id.desc()).all()
    response = {'status': 'true', 'message': "Data Received Successfully", 'data': data}
    return response


def create(db: Session, setting_create: SettingCreate):
    db_setting = Setting(**setting_create.dict())
    db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    response = {'status': 'true', 'message': "Setting Details Added Successfully", 'data': db_setting}
    return response


# def get_setting_by_employe_id_fun(db: Session, admin_id: str, employe_id: Optional[str] = None):
#     setting_query = db.query(Setting).filter(Setting.admin_id == admin_id)

#     if employe_id is not None:
#         setting_query = setting_query.filter(Setting.employe_id.ilike(f"%{employe_id}%"))

#     setting = setting_query.order_by(Setting.created_at.desc()).all()
#     # setting_file_query = db.query(SettingFiles).filter(SettingFiles.settings_id == setting[0].id)
#     setting_id = str(setting[0].id)
#     setting_file_query = db.query(SettingFiles).filter(SettingFiles.settings_id == setting_id).all()
#     response = {'status': 'true', 'message': "Data Received Successfully", 'data': {
#         "settings": setting,
#         "setting_files": setting_file_query
#     }}
#     return response
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew


def get_setting_by_employe_id_fun(db: Session, admin_id: str, employe_id: Optional[str] = None):
    setting_query = db.query(Setting).filter(Setting.admin_id == admin_id)

    if employe_id is not None:
        setting_query = setting_query.filter(Setting.employee_id.ilike(f"%{employe_id}%"))

    setting = setting_query.order_by(Setting.created_at.desc()).all()

    if not setting:
        return {'status': 'false', 'message': "No settings found for the given criteria", 'data': None}

    setting_id = str(setting[0].id)
    setting_file_query = db.query(SettingFiles).filter(SettingFiles.settings_id == setting_id).all()

    setting_list = []
    for sett in setting:
        setdata = vars(sett.copy())
        admin = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == int(sett.admin_id)).first()
        if admin:
            setdata["email"] = admin.email if admin.email else ""
            setdata["contact_number"] = str(admin.phone_number) if admin.phone_number else ""
        setting_list.append(setdata)

    response = {'status': 'true', 'message': "Data Received Successfully", 'data': {
        "admindetails": admin,
        "settings": setting_list,
        "setting_files": setting_file_query
    }}
    
    
    return response


def update(setting_id: int, setting_update: Setting, db: Session):
    setting_update = setting_update.dict(exclude_unset=True)
    db.query(Setting).filter(Setting.id == setting_id).update(setting_update)
    db.commit()
    response = {'status': 'true', 'message': "Setting Details Updated Successfully", 'data': setting_update}
    return response


def delete_setting_by_id_fun(id: int, db: Session):
    ocr_details = db.query(Setting).filter(Setting.id == id).first()

    if not ocr_details:
        return {'status': 'false', 'message': "Setting not found"}

    db.delete(ocr_details)
    db.commit()

    response = {
        'status': 'true',
        'message': "Setting Details deleted successfully"
    }

    return response
