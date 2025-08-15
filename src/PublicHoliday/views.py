from fastapi import APIRouter, Depends, Header, HTTPException, Body
from sqlalchemy.orm import Session
from .service import create_public_holiday_service,get_public_holiday_list_service,delete_public_holiday_service
from .models import PublicHolidayCreate,PublicHolidayAdminRequest,PublicHolidayDeleteRequest
from src.database import get_db
from src.parameter import get_token
from sqlalchemy import select

router = APIRouter()


@router.post("/create-holiday")
def create_public_holiday(
    holiday: PublicHolidayCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db),
):
   
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    
    return create_public_holiday_service(db=db, holiday=holiday)



@router.post("/get-public-holidays")
def get_public_holiday_list(
    request: PublicHolidayAdminRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db),
):
   
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    try:
        holidays = get_public_holiday_list_service(db=db, admin_id=request.admin_id)

        if not holidays:
            return {
                "status": "true",
                "message": "No public holidays found",
                "data": []
            }

        return {
            "status": "true",
            "message": "Public holidays fetched successfully",
            "data": holidays
        }
    except ValueError as ve:
        return {
            "status": "false",
            "message": str(ve)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail={"status": "false", "message": str(e)}
        )





@router.post("/delete-public-holiday")
def delete_public_holiday(
    request: PublicHolidayDeleteRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db),
):
    
    # Step 1: Check authentication
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

   
    response = delete_public_holiday_service(db=db, admin_id=request.admin_id, public_holiday_id=request.public_holiday_id)
    
    
    return response