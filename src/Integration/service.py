from .models import Integration,IntegrationCreate
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status, HTTPException

def get_integration_by_admin_id(db: Session, admin_id: str):
    data = db.query(Integration).filter(Integration.admin_id == admin_id).order_by(Integration.id.desc()).all()
    response = {'status': 'true', 'message': "Data Received Successfully", 'data': data}
    return response

def create(db: Session, integration_create: IntegrationCreate):
    db_integration = Integration(**integration_create.dict())
    db.add(db_integration)
    db.commit()
    db.refresh(db_integration)
    response = {'status': 'true', 'message': "Integration Details Added Successfully", 'data': db_integration}
    return response

def update(integration_id: int, integration__update: Integration, db: Session):
    db_integration_update = integration__update.dict(exclude_unset=True)
    db.query(Integration).filter(Integration.id == integration_id).update(db_integration_update)
    db.commit()
    response = {'status': 'true', 'message': "Integration Details Updated Successfully", 'data': db_integration_update}
    return response


def delete_integration_by_id(id: int, db: Session):
    integration_details = db.query(Integration).filter(Integration.id == id).first()

    if not integration_details:
        return {'status': 'false', 'message': "Integration not found"}

    db.delete(integration_details)
    db.commit()

    response = {
        'status': 'true',
        'message': "Integration Details deleted successfully"
    }

    return response