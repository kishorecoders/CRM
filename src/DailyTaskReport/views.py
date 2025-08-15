from fastapi import APIRouter, Depends, HTTPException, Header
from sqlmodel import Session
from .models import ReportRequestCreate , ReportRequestCreatelist, ReportRequestGet, ReportRequestDelete ,ReportRequestUpdate
from .service import create_report , create_multi_report ,get_report,delete_report,update_report
from src.database import get_db
from src.parameter import get_token


router = APIRouter()


@router.post("/createDailyreport")
def create_report_route(
    report_create: ReportRequestCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    
    return create_report(db=db, report_create=report_create)


@router.post("/createmultipleDailyreport")
def create_multi_report_route(
    paylode: ReportRequestCreatelist,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    
    return create_multi_report(db=db, paylode=paylode)

@router.post("/GetDailyreport")
def get_task_route(
    getpaylode: ReportRequestGet,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    
    return get_report(db=db, getpaylode=getpaylode)


@router.post("/DeleteDailyreport")
def delete_report_route(
    deletepaylode: ReportRequestDelete,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    
    return delete_report(db=db, deletepaylode=deletepaylode)


@router.post("/updateDailyreport")
def update_report_route(
    updatepaylode: ReportRequestUpdate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    
    return update_report(db=db, updatepaylode=updatepaylode)

