from typing import List
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from .models import Ocr,OcrCreate
from .service import create,get_all_ocr,get_ocr_employe_id,update,delete_ocr_by_id
from src.parameter import get_token

router = APIRouter()

@router.get("/showallOcr")
def get_all_ocr_details(auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_all_ocr(db=db)

@router.post("/CreateOCR")
def create_ocr_details(ocr_create: OcrCreate,
                auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return create(db=db, ocr_create=ocr_create)

@router.get("/ShowOcr/{employeId}")
def get_ocr_by_employe_id(employe_id:str, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_ocr_employe_id(db=db, employe_id=employe_id)
     
@router.put("/UpdateOcr/{ocr_id}")
def update_ocr_details(ocr_id:int,ocr_update:OcrCreate,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db:Session=Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return update(ocr_id=ocr_id,ocr_update=ocr_update,db=db)

@router.delete("/deleteOcr/{id}")
def delete_ocr_by_id(id: int, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return delete_ocr_by_id(id=id, db=db)