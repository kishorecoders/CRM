from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session
from src.database import get_db
from .models import Leads,LeadsCreate
from .service import create,get_leads_by_admin,delete_leads_by_id,update

router = APIRouter()


@router.get("/showallleads")
def read_leads_by_admin(db: Session = Depends(get_db)):
    return get_leads_by_admin(db=db)


@router.post("/Createleads")
def create_setting_details(leads_create: LeadsCreate, db: Session = Depends(get_db)):
    return create(db=db, leads_create=leads_create)


@router.put("/Updateleads/{leads_id}")
def update_setting_details(leads_id: int, leads_update: LeadsCreate, db: Session = Depends(get_db)):
    return update(leads_id=leads_id, leads_update=leads_update, db=db)


@router.delete("/deleteleads/{id}")
def delete_leads_details_by_id(id: int, db: Session = Depends(get_db)):
    return delete_leads_by_id(id=id, db=db)
