from fastapi import APIRouter, Depends,  Header
from sqlalchemy.orm import Session
from src.database import get_db
from src.parameter import get_token
from src.CheckPoint.models import CheckPointCreate , CheckPointRead , CheckPointDeletee , CheckPointUpdate
from src.CheckPoint.service import create , get_checkPoint , check_PointDeletee_by_id , update_checkPoint

router = APIRouter()


@router.post("/add_check_point")
def add_check_point(
    checkPointCreate: CheckPointCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    
    return create(db=db, checkPointCreate=checkPointCreate)


@router.post("/get_CheckPoint")
def create_quotation_details(
    checkPointRead: CheckPointRead,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    
    return get_checkPoint(db=db, checkPointRead=checkPointRead)


@router.post("/delete_checkpoint")
def delete_subproduct(
    checkPoint_id: CheckPointDeletee, 
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    return check_PointDeletee_by_id(db=db, checkPoint_id=checkPoint_id)


@router.post("/Update_checkpoint")
def update_checkPoint_by_id(
    checkPointUpdate: CheckPointUpdate, 
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    return update_checkPoint(db=db, checkPointUpdate = checkPointUpdate)



