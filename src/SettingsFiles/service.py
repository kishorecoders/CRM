from .models import SettingFiles, SettingFilesCreate
from sqlmodel import Session
from src.Settings.models import Setting
from sqlalchemy import cast
from sqlalchemy.types import String


def create(db: Session, setting_create: SettingFilesCreate):
    db_setting = SettingFiles(**setting_create.dict())
    db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    response = {'status': 'true', 'message': "Setting Files Added Successfully", 'data': db_setting}
    return response

def get_setting_file_by_admin(db: Session, admin_id: str):
    setting_data = db.query(Setting).filter(Setting.admin_id == admin_id).all()
    
    dataArray = []
    for setting in setting_data:
        setting_files_data = db.query(SettingFiles).filter(
            SettingFiles.settings_id == cast(setting.id, String)
        ).all()
        
        temp = {
            "setting": setting,
            "setting_files": setting_files_data
        }
        dataArray.append(temp)
    
    response = {'status': 'true', 'message': "Data Received Successfully", 'data': dataArray}
    return response

def delete_file_settings_by_id(id: int, db: Session):
    setting_files_details = db.query(SettingFiles).filter(SettingFiles.id == id).first()

    if not setting_files_details:
        return {'status': 'false', 'message': "Setting Files Issue not found"}

    db.delete(setting_files_details)
    db.commit()

    response = {
        'status': 'true',
        'message': "Setting Files Details deleted successfully"
    }
    
    return response
