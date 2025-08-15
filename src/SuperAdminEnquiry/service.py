from .models import SuperAdminEnquiry,SuperAdminEnquiryCreate
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime, timedelta
from fastapi import status,HTTPException


def get_all_enquiry(db: Session):
    data = db.query(SuperAdminEnquiry).order_by(SuperAdminEnquiry.id.desc()).all()
    response = {'status': 'true', 'message': "Data Received Successfully", 'data': data}
    return response

def create(db: Session, super_admin_enquiry: SuperAdminEnquiryCreate):
    db_super_admin_enquiry = SuperAdminEnquiry(**super_admin_enquiry.dict())
    db.add(db_super_admin_enquiry)
    db.commit()
    db.refresh(db_super_admin_enquiry)
    response = {'status': 'true','message':"Super Admin Billing Create Successfully",'data':db_super_admin_enquiry}
    return response

def update(enquiry_id:int,super_admin_enquiry:SuperAdminEnquiry,db:Session):
    super_admin_enquiry_update = super_admin_enquiry.dict(exclude_unset=True)
    db.query(SuperAdminEnquiry).filter(SuperAdminEnquiry.id == enquiry_id).update(super_admin_enquiry_update)
    db.commit()
    response = {'status': 'true','message':"Data Updated Successfully",'data':super_admin_enquiry_update}
    return response