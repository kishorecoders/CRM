from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session
from src.database import get_db
from .models import LeadReminderCreate,LeadReminderFilterRequest,UpdateReminderRequest,DeleteReminderRequest
from .service import create,get_lead_reminders_with_details,update_lead_reminder,delete_lead_reminder
from src.parameter import get_token

router = APIRouter()


@router.post("/create_reminder")
def create_reminder_details(
    reminder_create: LeadReminderCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    if not reminder_create.Lead_id:
        return {"status": "false", "message": "Lead ID is required"}

    return create(db=db, reminder_create=reminder_create)



@router.post("/get_lead_reminders")
def get_reminders_with_details(
    filter_request: LeadReminderFilterRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    reminders_with_details = get_lead_reminders_with_details(
        db=db,
        admin_id=filter_request.admin_id,
        employee_id=filter_request.employee_id
    )

    if not reminders_with_details:
        return {"status": "false", "message": "No reminders found for the given criteria"}

    return {"status": "true", "message": "Reminders retrieved successfully", "data": reminders_with_details}




@router.post("/update_reminder")
def update_reminder_details(
    update_request: UpdateReminderRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    
    update_data = update_request.dict(exclude={"reminder_id"}, exclude_unset=True)
    result = update_lead_reminder(db=db, reminder_id=update_request.reminder_id, update_data=update_data)
    return result





@router.post("/delete_reminder")
def delete_reminder(
    delete_request: DeleteReminderRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    
    
    result = delete_lead_reminder(
        db=db,
        reminder_id=delete_request.reminder_id,
        admin_id=delete_request.admin_id,
        employee_id=delete_request.employee_id
    )
    return result
