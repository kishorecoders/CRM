from .models import Ocr,OcrCreate
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status,HTTPException

def get_all_ocr(db: Session):
    data = db.query(Ocr).order_by(Ocr.id.desc()).all()
    response = {'status': 'true', 'message': "Data Received Successfully", 'data': data}
    return response

def create(db: Session, ocr_create: OcrCreate):
    db_ocr = Ocr(**ocr_create.dict())
    db.add(db_ocr)
    db.commit()
    db.refresh(db_ocr)
    response = {'status': 'true','message':"Ocr Details Added Successfully",'data':db_ocr}
    return response

def get_ocr_employe_id(employe_id: int, db: Session):
    data = db.query(Ocr).filter(Ocr.employe_id == employe_id).all()
    response = {'status': 'true','message':"Data Recived Successfully",'data':data}
    return response
   

def update(ocr_id:int, ocr_update:Ocr,db:Session):
    ocr_update = ocr_update.dict(exclude_unset=True)
    db.query(Ocr).filter(Ocr.id == ocr_id).update(ocr_update)
    db.commit()
    response = {'status': 'true','message':"Ocr Details Updated Successfully",'data':ocr_update}
    return response

def delete_ocr_by_id(id: int, db: Session):
    ocr_details = db.query(Ocr).filter(Ocr.id == id).first()

    if not ocr_details:
        return {'status': 'false', 'message': "Ocr not found"}

    db.delete(ocr_details)
    db.commit()

    response = {
        'status': 'true',
        'message': "Ocr Details deleted successfully"
    }
    
    return response