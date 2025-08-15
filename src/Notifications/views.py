from typing import List,Optional
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from .models import NotificationRead
from .service import get_notification
from src.parameter import get_token

router = APIRouter()

@router.post("/Notifications")
def get_notification_api(
    notification: NotificationRead,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
   
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    

    return get_notification(db=db, notification=notification)



