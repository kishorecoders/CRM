from typing import List
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from src.parameter import get_token
from sqlalchemy import exc
from typing import Dict
from fastapi import APIRouter, Depends, Header, HTTPException, Body
from typing import Optional, List
from src.Attendance.models import  Attendance,AttendanceCreate,CheckIn,CheckOut,SignOut,AttendanceRequest,AttendanceFilterRequest,AttendanceMenualCreate,SalaryDetailsRequest,UpdateSignOutRequest,TimerRequest,DeleteAtt
from src.Attendance.service import create_attendance,check_in,check_out,sign_out,get_today_attendance,get_filtered_attendance,create_manual_attendance,get_employee_salary,delete_attendance
from pydantic import BaseModel
import calendar
from src.TimeConfig.models import TimeConfig 
from src.PublicHoliday.models import PublicHoliday



from fastapi import APIRouter, UploadFile, Depends, Header, HTTPException
from sqlmodel import Session, select
from datetime import datetime, timedelta
from src.AdminAddEmployee.models import AdminAddEmployee

router = APIRouter()


import time
import pytz
TZ = pytz.timezone("Asia/Kolkata")



# @router.post("/att_sign_in")
# def create_attendance_entry(
#     attendance: AttendanceCreate,
#     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#     db: Session = Depends(get_db)
# ):
#     if auth_token != get_token():
#         return {"status": "false", "message": "Unauthorized Request"}

#     return create_attendance(db=db, attendance_data=attendance)

@router.post("/att_sign_in")
def create_attendance_entry(
    attendance: AttendanceCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    return create_attendance(db=db, attendance_data=attendance)



@router.post("/check_in")
def record_check_in(
    check_in_data: CheckIn,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    return check_in(db=db, attendance_data=check_in_data)




@router.post("/check_out")
def record_check_out(
    check_out_data: CheckOut,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    return check_out(db=db, attendance_data=check_out_data)




@router.post("/att_sign_out")
def create_sign_out_entry(
    attendance: SignOut,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    return sign_out(db=db, attendance_data=attendance)
    
    
    
    

@router.post("/update_signout_status")
def update_sign_out(data: UpdateSignOutRequest, db: Session = Depends(get_db)):
    sign_out_record = db.query(Attendance).filter(Attendance.id == data.sign_out_id, Attendance.status == "sign-out").first()
    
    if not sign_out_record:
        raise HTTPException(status_code=404, detail="Sign-out record not found.")
    
    sign_out_record.over_time = data.over_time
    sign_out_record.remark = data.remark
    sign_out_record.updated_at = datetime.now()
    
    db.commit()
    db.refresh(sign_out_record)
    
    return {"status": "true", "message": "Sign-out record updated successfully.", "data": sign_out_record}





@router.post("/get_today_attendance")
def get_today_attendance_route(
    attendance_request: AttendanceRequest = Body(...), 
    auth_token: str = Header(...),  
    db: Session = Depends(get_db)  
):
    employee_id = attendance_request.employee_id
    admin_id = attendance_request.admin_id

   
    attendance_data = get_today_attendance(db, employee_id, admin_id)

   
    if attendance_data:
        response = {
            "status": "true",
            "message": "Attendance records retrieved successfully.",
            "data": attendance_data  
        }
    else:
        response = {
            "status": "false",
            "message": "No attendance records found for today.",
            "data": []  
        }

    return response





@router.post("/get_filtered_attendance")
def get_filtered_attendance_route(
    attendance_request: AttendanceFilterRequest = Body(...),
    auth_token: str = Header(...),
    db: Session = Depends(get_db)
):
    admin_id = attendance_request.admin_id
    employee_id = attendance_request.employee_id
    from_date = attendance_request.from_date
    to_date = attendance_request.to_date
    employee_name = attendance_request.employee_name

    if not admin_id:
        return {
            "status": "false",
            "message": "admin_id is mandatory."
        }

    try:
        attendance_data = get_filtered_attendance(
            db=db,
            admin_id=admin_id,
            employee_id=employee_id,
            from_date=from_date,
            to_date=to_date,
            employee_name=employee_name
        )

        if attendance_data:
            return {
                "status": "true",
                "message": "Attendance records retrieved successfully.",
                "data": attendance_data
            }
        else:
            return {
                "status": "false",
                "message": "No attendance records found for the given criteria.",
                "data": []
            }
    except Exception as e:
        return {
            "status": "false",
            "message": f"An error occurred: {str(e)}",
            "data": []
        }

    

@router.post("/mark_manual_attendance")
def mark_manual_attendance(
    attendance: AttendanceMenualCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    
    return create_manual_attendance(db=db, attendance_data=attendance)






@router.post("/get_employee_salary")
def get_salary_details(
    salary_request: SalaryDetailsRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():  
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    return get_employee_salary(db=db, admin_id=salary_request.admin_id, emp_id=salary_request.emp_id)
    
    
    
    
    



timers = {}


@router.post("/start")
def start_timer(request: TimerRequest):
    sign_out_id = request.sign_out_id

    if sign_out_id in timers and timers[sign_out_id]["start_time"] is not None:
        return {"status":"true","message": "Timer already running", "start_time": timers[sign_out_id]["start_time"]}
    
    timers[sign_out_id] = {"start_time": datetime.now(TZ), "end_time": None}
    return {
        "status": "true",
        "message": "Timer started",
        "start_time": timers[sign_out_id]["start_time"].strftime("%Y-%m-%d %H:%M:%S")
    }

@router.post("/stop")
def stop_timer(request: TimerRequest):
    sign_out_id = request.sign_out_id

    if sign_out_id not in timers or timers[sign_out_id]["start_time"] is None:
        return {"status":"false","message": "No active timer found"}

    timers[sign_out_id]["end_time"] = datetime.now(TZ)
    elapsed_time = timers[sign_out_id]["end_time"] - timers[sign_out_id]["start_time"]
    
    response = {
        "status": "true",
        "message": "Timer stopped",
        "start_time": timers[sign_out_id]["start_time"].strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": timers[sign_out_id]["end_time"].strftime("%Y-%m-%d %H:%M:%S"),
        "interval_time": str(elapsed_time)
    }
    
    del timers[sign_out_id]

    return response


@router.post("/delete_attendance")
def delete_att(
    salary_request: DeleteAtt,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():  
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    return delete_attendance(db=db, salary_request=salary_request)



from .service import create_overtime
from .models import AttendanceOvertimeCreate

@router.post("/overtimecreate")
def create_overtime_entry(
    overtime: AttendanceOvertimeCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")


    return create_overtime(db=db, overtime_data=overtime)


