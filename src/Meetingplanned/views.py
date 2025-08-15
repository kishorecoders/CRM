from typing import List,Optional
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from src.Meetingplanned.models import Meetingplanned,MeetingplannedCreate,MeetingplannedReadRequest
from src.Meetingplanned.service import create,get_meeting_details,update,delete_meeting,get_meeting_details_by_employee,get_meeting_details_post
from src.parameter import get_token

router = APIRouter()

@router.post("/")
def create_meeting_details(meeting_planned: MeetingplannedCreate,
                auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return create(db=db, meeting_planned=meeting_planned)
    
    return inner_get_plan(auth_token)



@router.post("/ShowMeeting")
def read_meeting_detailspost(
     read_request: MeetingplannedReadRequest,
     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), 
     db: Session = Depends(get_db)
     ):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_meeting_details_post(db=db ,read_request=read_request)

    return inner_get_plan(auth_token)

@router.get("/ShowMeeting/{lead_id}/{employee_id}")
def read_meeting_details(lead_id: int, employee_id: str, meeting_status: Optional[str] = None, name: Optional[str] = None, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
        def inner_get_plan(auth_token: str):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return get_meeting_details(lead_id=lead_id, employee_id=employee_id,meeting_status=meeting_status,name=name, db=db)
    
        return inner_get_plan(auth_token)
    
@router.get("/ShowMeetingbyEmployee/{employee_id}")
def read_meeting_by_employee_details(employee_id: str, meeting_status: Optional[str] = None, name: Optional[str] = None, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
        def inner_get_plan(auth_token: str):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return get_meeting_details_by_employee(employee_id=employee_id, meeting_status=meeting_status, name=name, db=db)
    
        return inner_get_plan(auth_token)    

@router.put("/UpdateMeeting/{id}")
def update_meeting_details(id:int,meeting_planned:MeetingplannedCreate,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db:Session=Depends(get_db)):
       def inner_get_plan(auth_token: str):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return update(meeting_id=id,meeting_planned=meeting_planned,db=db)
    
       return inner_get_plan(auth_token)
   
@router.delete("/deleteMeeting/{id}")
def delete_meeting_details(id:int,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db:Session=Depends(get_db)):
       def inner_get_plan(auth_token: str):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return delete_meeting(id=id,db=db)
    
       return inner_get_plan(auth_token)