from .models import Leads,LeadsCreate
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status, HTTPException

def get_leads_by_admin(db: Session):
    data = db.query(Leads).order_by(Leads.id.desc()).all()
    response = {'status': 'true', 'message': "Data Received Successfully", 'data': data}
    return response

def create(db: Session, leads_create: LeadsCreate):
    db_leads = Leads(**leads_create.dict())
    db.add(db_leads)
    db.commit()
    db.refresh(db_leads)
    response = {'status': 'true', 'message': "Leads Details Added Successfully", 'data': db_leads}
    return response

def update(leads_id: int, leads_update: Leads, db: Session):
    db_leads_update = leads_update.dict(exclude_unset=True)
    db.query(Leads).filter(Leads.id == leads_id).update(db_leads_update)
    db.commit()
    response = {'status': 'true', 'message': "Leads Details Updated Successfully", 'data': db_leads_update}
    return response


def delete_leads_by_id(id: int, db: Session):
    leads_details = db.query(Leads).filter(Leads.id == id).first()

    if not leads_details:
        return {'status': 'false', 'message': "Leads not found"}

    db.delete(leads_details)
    db.commit()

    response = {
        'status': 'true',
        'message': "Leads Details deleted successfully"
    }

    return response