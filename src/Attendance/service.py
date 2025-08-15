from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status, HTTPException
from src.Attendance.models import Attendance, AttendanceCreate,CheckIn,CheckOut,SignOut,AttendanceMenualCreate,EmployeeSalaryResponse,DeleteAtt
from sqlalchemy import exc
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from sqlmodel import Session, select
from sqlalchemy.orm import aliased
from datetime import datetime
from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlmodel import select
from datetime import datetime, timedelta
from datetime import datetime, date
from datetime import datetime, time
from typing import Optional, Tuple
from src.PublicHoliday.models import PublicHoliday
from src.AdminAddEmployee.models import AdminAddEmployee
from src.EmployeeFiles.models import EmployeeFiles
from src.TimeConfig.models import TimeConfig
from collections import defaultdict
from sqlalchemy import func
from sqlalchemy import select, desc
from typing import Optional, Set
import calendar
import time
import pytz
from src.cre_upd_name import get_creator_info


TZ = pytz.timezone("Asia/Kolkata")




from apscheduler.schedulers.background import BackgroundScheduler
from datetime import timedelta
from src.database import get_db



from calendar import monthrange



#import face_recognition
from fastapi import UploadFile, HTTPException
from io import BytesIO

def get_current_datetime():
    return datetime.utcnow()



def get_shift_times_for_employee(db: Session, admin_id: int, shift_name: str):
    shift_config = db.execute(
        select(TimeConfig)
        .where(TimeConfig.admin_id == admin_id)
    ).scalars().first()
    
    if not shift_config:
        return {
            "status": "false",
            "message": "Shift not found for the given admin_id and shift_name"
        }

    return shift_config  


# def calculate_late_minutes(sign_in_time: datetime.time, start_time: datetime.time, in_time: datetime.time) -> int:
    
#     if start_time <= sign_in_time <= in_time:
#         return 0
    
#     if sign_in_time > in_time:
#         print()
        
#         base_date = datetime.today().date() 
#         sign_in_datetime = datetime.combine(base_date, sign_in_time)
#         start_datetime = datetime.combine(base_date, start_time)
        
#         late_minutes = int((sign_in_datetime - start_datetime).total_seconds() / 60)
#         return late_minutes
    
    
#     return 0

def calculate_late_minutes_old(sign_in_time: time, start_time: time, in_time: time) -> int:
    base_date = datetime.today().date()
    sign_in_datetime = datetime.combine(base_date, sign_in_time.replace(second=0, microsecond=0))
    start_time_datetime = datetime.combine(base_date, start_time)
    in_time_datetime = datetime.combine(base_date, in_time)

    print(f"Base Date: {base_date}")
    print(f"Sign-in Time (datetime): {sign_in_datetime}")
    print(f"Start Time (datetime): {start_time_datetime}")
    print(f"In-Time (datetime): {in_time_datetime}")

    
    if sign_in_datetime > start_time_datetime:
        late_minutes = int((sign_in_datetime - start_time_datetime).total_seconds() / 60)
        print(f"Sign-in is late by {late_minutes} minutes.")
        return late_minutes

    return 0 
    
    
    
def calculate_late_minutes(sign_in_time: time, start_time: time, in_time: time) -> int:
    if not (sign_in_time and start_time and in_time):
        print("[Warning] One or more time values are None. Skipping late calculation.")
        return 0

    base_date = datetime.today().date()
    sign_in_datetime = datetime.combine(base_date, sign_in_time.replace(second=0, microsecond=0))
    start_time_datetime = datetime.combine(base_date, start_time)
    in_time_datetime = datetime.combine(base_date, in_time)

    print(f"Base Date: {base_date}")
    print(f"Sign-in Time (datetime): {sign_in_datetime}")
    print(f"Start Time (datetime): {start_time_datetime}")
    print(f"In-Time (datetime): {in_time_datetime}")

    if sign_in_datetime > start_time_datetime:
        late_minutes = int((sign_in_datetime - start_time_datetime).total_seconds() / 60)
        print(f"Sign-in is late by {late_minutes} minutes.")
        return late_minutes

    return 0


def get_saturday_week_number(date: datetime) -> int:
    first_day_of_month = date.replace(day=1)
    first_saturday = first_day_of_month + timedelta(days=(5 - first_day_of_month.weekday()) % 7)
    delta_days = (date - first_saturday).days
    return (delta_days // 7) + 1


def is_sign_in_outside_shift(sign_in_time: datetime.time, start_time: datetime.time, end_time: datetime.time) -> bool:
    
    if start_time <= end_time:
        return sign_in_time < start_time or sign_in_time > end_time
    
    else:
        return not (sign_in_time >= start_time or sign_in_time <= end_time)





# def create_attendance(db: Session, attendance_data: AttendanceCreate):
#     employee_id = attendance_data.employee_id
#     admin_id = attendance_data.admin_id
#     today_start = datetime.utcnow().date()
#     today_end = today_start + timedelta(days=1)

#     employee = db.execute(
#         select(AdminAddEmployee)
#         .where(AdminAddEmployee.id == employee_id)
#     ).scalars().first()
#     if not employee:
#         return {
#             "status": "false",
#             "message": "Employee not found"
#         }

#     if not employee.shift_name or employee.shift_name == "Null":
#         return {
#             "status": "false",
#             "message": "Shift name is not defined for the employee"
#         }

#     shift_name = employee.shift_name
#     shift_config = get_shift_times_for_employee(db, admin_id, shift_name)

#     public_holiday = db.execute(
#         select(PublicHoliday)
#         .where(
#             PublicHoliday.admin_id == admin_id,
#             PublicHoliday.event_date >= today_start,
#             PublicHoliday.event_date < today_end
#         )
#     ).scalars().first()

#     if public_holiday:
#         return {
#             "status": "false",
#             "message": f"Employee cannot sign in today due to a public holiday: {public_holiday.event_name}."
#         }

#     if shift_config.weekly_holidays:
#         today_weekday = today_start.weekday()  
#         saturday_week_number = get_saturday_week_number(today_start)

#         if ("All Sunday" in shift_config.weekly_holidays and today_weekday == 6):
#             return {
#                 "status": "false",
#                 "message": "Employee cannot sign in today because it's a Sunday holiday."
#             }

#         if ("All Saturday" in shift_config.weekly_holidays and today_weekday == 5):
#             return {
#                 "status": "false",
#                 "message": "Employee cannot sign in today because it's a Saturday holiday."
#             }

#         if "2 Saturday (1st & 3rd)" in shift_config.weekly_holidays:
#             if today_weekday == 5:
#                 if saturday_week_number == 1:
#                     return {
#                         "status": "false",
#                         "message": "Employee cannot sign in today because it's the 1st Saturday of the month."
#                     }
#                 elif saturday_week_number == 3:
#                     return {
#                         "status": "false",
#                         "message": "Employee cannot sign in today because it's the 3rd Saturday of the month."
#                     }

#         if "2 Saturday (2nd & 4th)" in shift_config.weekly_holidays:
#             if today_weekday == 5:
#                 if saturday_week_number == 2:
#                     return {
#                         "status": "false",
#                         "message": "Employee cannot sign in today because it's the 2nd Saturday of the month."
#                     }
#                 elif saturday_week_number == 4:
#                     return {
#                         "status": "false",
#                         "message": "Employee cannot sign in today because it's the 4th Saturday of the month."
#                     }

   
#     shift_times = {
#         'shift-1': {
#             'start': shift_config.start_time_1st,
#             'in': shift_config.in_time_1st,
#             'end': shift_config.end_time_1st,
#             'lunch_start': shift_config.lunch_time_start_1st,
#             'lunch_end': shift_config.lunch_time_end_1st
#         },
#         'shift-2': {
#             'start': shift_config.start_time_2nd,
#             'in': shift_config.in_time_2nd,
#             'end': shift_config.end_time_2nd,
#             'lunch_start': shift_config.lunch_time_start_2nd,
#             'lunch_end': shift_config.lunch_time_end_2nd
#         },
#         'shift-3': {
#             'start': shift_config.start_time_3rd,
#             'in': shift_config.in_time_3rd,
#             'end': shift_config.end_time_3rd,
#             'lunch_start': shift_config.lunch_time_start_3rd,
#             'lunch_end': shift_config.lunch_time_end_3rd
#         },
#         'shift-general': {
#             'start': shift_config.start_time_general,
#             'in': shift_config.in_time_general,
#             'end': shift_config.end_time_general,
#             'lunch_start': shift_config.lunch_time_start_general,
#             'lunch_end': shift_config.lunch_time_end_general
#         }
#     }

#     if shift_name not in shift_times:
#         return {
#             "status": "false",
#             "message": "Invalid shift name"
#         }

#     times = shift_times[shift_name]
#    # start_time = datetime.strptime(times['start'], "%I:%M %p").time() if times['start'] else None
#     def parse_time_or_none(value, label=''):
#       try:
#           return datetime.strptime(value.strip(), "%I:%M %p").time()
#       except (ValueError, TypeError, AttributeError):
#           print(f"[Warning] Invalid time format for {label}: {value!r}")
#           return None


#     start_time = parse_time_or_none(times.get('start'), 'start_time')
#     in_time = parse_time_or_none(times.get('in'), 'in_time')
#     end_time = parse_time_or_none(times.get('end'), 'end_time')
#     lunch_start_time = parse_time_or_none(times.get('lunch_start'), 'lunch_start_time')
#     lunch_end_time = parse_time_or_none(times.get('lunch_end'), 'lunch_end_time')


#     #in_time = datetime.strptime(times['in'], "%I:%M %p").time() if times['in'] else None
#    # end_time = datetime.strptime(times['end'], "%I:%M %p").time() if times['end'] else None
#    # lunch_start_time = datetime.strptime(times['lunch_start'], "%I:%M %p").time() if times['lunch_start'] else None
#    # lunch_end_time = datetime.strptime(times['lunch_end'], "%I:%M %p").time() if times['lunch_end'] else None

#     sign_in_time = datetime.now(TZ).time()
#     print(f"start_time Time: {start_time.strftime('%I:%M %p') if start_time else 'N/A'}")
#     print(f"sign_in_time Time: {sign_in_time.strftime('%I:%M %p')}")
#     print(f"end_time Time: {end_time.strftime('%I:%M %p') if end_time else 'N/A'}")

   
#     if is_sign_in_outside_shift(sign_in_time, start_time, end_time):
#         return {
#             "status": "false",
#             "message": "Sign-in time is outside the assigned shift time."
#         }

    
#     if lunch_start_time and lunch_end_time and lunch_start_time <= sign_in_time <= lunch_end_time:
#         return {
#             "status": "false",
#             "message": "Employee cannot sign-in during lunch time."
#         }
    
    

    
#     #late_minute = calculate_late_minutes(sign_in_time, start_time, in_time)
#     if start_time and in_time:
#         late_minute = calculate_late_minutes(sign_in_time, start_time, in_time)
#     else:
#         late_minute = 0  # or maybe raise a validation error


#     if late_minute > 0:
#         hours = late_minute // 60
#         minutes = late_minute % 60
#         time_str = f"{hours} hours {minutes} minutes" if hours > 0 else f"{minutes} minutes"

    
    
#         if not attendance_data.remark.strip():  
#             return {
#                 "status": "false",
#                 "message": f"Why are you so late? You are {time_str} late. Please provide a remark to sign in.",
#                 "late_minutes": late_minute
#             }

    
#     existing_sign_in = db.execute(
#         select(Attendance)
#         .where(
#             and_(
#                 Attendance.employee_id == employee_id,
#                 Attendance.date_time >= today_start,
#                 Attendance.date_time < today_end,
#                 Attendance.status == "sign-in"
#             )
#         )
#     ).scalars().first()

#     if existing_sign_in:
#         return {
#             "status": "false",
#             "message": "Sign-in record already exists for this employee today."
#         }

#     db_attendance = Attendance(
#         admin_id=attendance_data.admin_id,
#         employee_id=attendance_data.employee_id,
#         employee_name=employee.employe_name, 
#         latitude=attendance_data.latitude,
#         longitude=attendance_data.longitude,
#         address=attendance_data.address,
#         image=attendance_data.sign_in_img,
#         status="sign-in",
#         late_minute=late_minute,
#         remark=attendance_data.remark.strip()  
#     )
#     db.add(db_attendance)
#     db.commit()
#     db.refresh(db_attendance)

#     return {
#         "status": "true",
#         "message": "Sign-in recorded successfully.",
#         "data":db_attendance 
#     }


def create_attendance(db: Session, attendance_data):
    employee_id = attendance_data.employee_id
    admin_id = attendance_data.admin_id
    today_start = datetime.utcnow().date()
    today_end = today_start + timedelta(days=1)

    employee = db.execute(
        select(AdminAddEmployee).where(AdminAddEmployee.id == employee_id)
    ).scalars().first()

    if not employee:
        return {"status": "false", "message": "Employee not found"}

    if not employee.shift_name or employee.shift_name == "Null":
        return {"status": "false", "message": "Shift name is not defined for the employee"}

    shift_name = employee.shift_name
    shift_config = get_shift_times_for_employee(db, admin_id, shift_name)

    # Public holiday check
    public_holiday = db.execute(
        select(PublicHoliday).where(
            PublicHoliday.admin_id == admin_id,
            PublicHoliday.event_date >= today_start,
            PublicHoliday.event_date < today_end
        )
    ).scalars().first()

    if public_holiday:
        return {
            "status": "false",
            "message": f"Employee cannot sign in today due to a public holiday: {public_holiday.event_name}."
        }

    # Weekly holiday check
    if shift_config.weekly_holidays:
        today_weekday = today_start.weekday()
        saturday_week_number = get_saturday_week_number(today_start)

        if "All Sunday" in shift_config.weekly_holidays and today_weekday == 6:
            return {"status": "false", "message": "Employee cannot sign in today because it's a Sunday holiday."}

        if "All Saturday" in shift_config.weekly_holidays and today_weekday == 5:
            return {"status": "false", "message": "Employee cannot sign in today because it's a Saturday holiday."}

        if "2 Saturday (1st & 3rd)" in shift_config.weekly_holidays and today_weekday == 5:
            if saturday_week_number in [1, 3]:
                return {"status": "false", "message": f"Employee cannot sign in today because it's the {saturday_week_number}rd Saturday."}

        if "2 Saturday (2nd & 4th)" in shift_config.weekly_holidays and today_weekday == 5:
            if saturday_week_number in [2, 4]:
                return {"status": "false", "message": f"Employee cannot sign in today because it's the {saturday_week_number}th Saturday."}

    # Helpers
    def parse_time_or_none(value, label=''):
        try:
            return datetime.strptime(value.strip(), "%I:%M %p").time()
        except (ValueError, TypeError, AttributeError):
            print(f"[Warning] Invalid time format for {label}: {value!r}")
            return None

    def parse_minutes_or_none(value, label=''):
        try:
            return int(value)
        except (ValueError, TypeError):
            print(f"[Warning] Invalid minute format for {label}: {value!r}")
            return None

    # Shift config
    shift_times = {
        'shift-1': {
            'start': shift_config.start_time_1st,
            'in': shift_config.in_time_1st,
            'end': shift_config.end_time_1st,
            'lunch_start': shift_config.lunch_time_start_1st,
            'lunch_end': shift_config.lunch_time_end_1st
        },
        'shift-2': {
            'start': shift_config.start_time_2nd,
            'in': shift_config.in_time_2nd,
            'end': shift_config.end_time_2nd,
            'lunch_start': shift_config.lunch_time_start_2nd,
            'lunch_end': shift_config.lunch_time_end_2nd
        },
        'shift-3': {
            'start': shift_config.start_time_3rd,
            'in': shift_config.in_time_3rd,
            'end': shift_config.end_time_3rd,
            'lunch_start': shift_config.lunch_time_start_3rd,
            'lunch_end': shift_config.lunch_time_end_3rd
        },
        'shift-general': {
            'start': shift_config.start_time_general,
            'in': shift_config.in_time_general,
            'end': shift_config.end_time_general,
            'lunch_start': shift_config.lunch_time_start_general,
            'lunch_end': shift_config.lunch_time_end_general
        }
    }

    if shift_name not in shift_times:
        return {"status": "false", "message": "Invalid shift name"}

    times = shift_times[shift_name]

    start_time_obj = parse_time_or_none(times.get('start'), 'start_time')
    lunch_start_time = parse_time_or_none(times.get('lunch_start'), 'lunch_start')
    lunch_end_time = parse_time_or_none(times.get('lunch_end'), 'lunch_end')
    in_time_offset = parse_minutes_or_none(times.get('in'), 'in_time')
    end_time_offset = parse_minutes_or_none(times.get('end'), 'end_time')

    now = datetime.now(TZ)
    sign_in_time_obj = now.time()
    sign_in_minute = now.hour * 60 + now.minute

    shift_start_minutes = (start_time_obj.hour * 60 + start_time_obj.minute) if start_time_obj else 0
    expected_sign_in_minute = shift_start_minutes + (in_time_offset or 0)

    # Check for valid time range
    if in_time_offset is not None and end_time_offset is not None:
        expected_end_minute = shift_start_minutes + end_time_offset
        if not (expected_sign_in_minute <= sign_in_minute <= expected_end_minute):
            return {"status": "false", "message": "Sign-in time is outside the assigned shift time."}

    if lunch_start_time and lunch_end_time and lunch_start_time <= sign_in_time_obj <= lunch_end_time:
        return {"status": "false", "message": "Employee cannot sign-in during lunch time."}

    late_minute = max(0, sign_in_minute - expected_sign_in_minute)

    # Check for existing sign-in
    existing_sign_in = db.execute(
        select(Attendance).where(
            and_(
                Attendance.employee_id == employee_id,
                Attendance.date_time >= today_start,
                Attendance.date_time < today_end,
                Attendance.status == "sign-in"
            )
        )
    ).scalars().first()

    # Handle sign-out
    if existing_sign_in and attendance_data.type == "operator":
        existing_sign_out = db.execute(
            select(Attendance).where(
                and_(
                    Attendance.employee_id == employee_id,
                    Attendance.date_time >= today_start,
                    Attendance.date_time < today_end,
                    Attendance.status == "sign-out"
                )
            )
        ).scalars().first()

        if existing_sign_out:
            return {"status": "false", "message": "Sign-out record already exists for this employee today."}

        db_attendance = Attendance(
            admin_id=admin_id,
            employee_id=employee_id,
            employee_name=employee.employe_name,
            latitude=attendance_data.latitude,
            longitude=attendance_data.longitude,
            address=attendance_data.address,
            image=attendance_data.sign_in_img,
            status="sign-out",
            late_minute=late_minute,
            remark=attendance_data.remark.strip()
        )

        db.add(db_attendance)
        db.commit()
        db.refresh(db_attendance)

        emp_name = None
        employee = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == int(db_attendance.employee_id)).first()
        if employee:
            emp_name = f"{employee.employe_name}({employee.employee_id})"

        # ? Notification for sign-out
        notification = Notification(
            admin_id=admin_id,
            title="Employee Signed Out",
            description=f"{emp_name} has signed out at {now.strftime('%I:%M %p')}.",
            type="attendance_sign_out",
            object_id=str(db_attendance.id),
            created_by_id=employee_id,
            created_by_type="employee",
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)


        return {
            "status": "true",
            "message": "sign-out successfully.",
            "data": {
                "attendance_id": db_attendance.id,
                "admin_id": admin_id,
                "employee_id": employee_id,
                "employee_id_id": employee.employee_id,
                "employee_name": employee.employe_name,
                "latitude": attendance_data.latitude,
                "longitude": attendance_data.longitude,
                "address": attendance_data.address,
                "image": attendance_data.sign_in_img,
                "in_time": sign_in_time_obj,
                "out_time": end_time_offset,
                "status": "sign-out",
                "late_minute": late_minute,
                "remark": attendance_data.remark.strip()
            }
        }

    elif existing_sign_in:
        return {"status": "false", "message": "Sign-in record already exists for this employee today."}

    # Late without remark
    if late_minute > 0 and not attendance_data.remark.strip():
        employee_id_id = employee.employee_id
        hours = late_minute // 60
        minutes = late_minute % 60
        time_str = f"{hours} hour{'s' if hours != 1 else ''} {minutes} minute{'s' if minutes != 1 else ''}" if hours else f"{minutes} minute{'s' if minutes != 1 else ''}"

        actual_sign_in_str = now.strftime("%I:%M %p")
        expected_time_dt = datetime.combine(now.date(), start_time_obj) + timedelta(minutes=in_time_offset or 0)
        expected_start_str = expected_time_dt.strftime("%I:%M %p") if start_time_obj else "N/A"

        return {
            "status": "false",
            "message": (
                f"Why are you so late? Expected sign-in was at {expected_start_str}, "
                f"but you signed in at {actual_sign_in_str} - {time_str} late. "
                "Please provide a remark to sign in."
            ),
            "late_minutes": late_minute,
            "data": {
                "employee_id": employee_id,
                "employee_id_id": employee_id_id,
                "employee_name": employee.employe_name
            }
        }

    # Sign-in entry
    db_attendance = Attendance(
        admin_id=admin_id,
        employee_id=employee_id,
        employee_name=employee.employe_name,
        latitude=attendance_data.latitude,
        longitude=attendance_data.longitude,
        address=attendance_data.address,
        image=attendance_data.sign_in_img,
        status="sign-in",
        late_minute=late_minute,
        remark=attendance_data.remark.strip()
    )

    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)

    emp_name = None
    employee = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == int(db_attendance.employee_id)).first()
    if employee:
        emp_name = f"{employee.employe_name}({employee.employee_id})"

    # ? Notification for sign-in
    notification = Notification(
        admin_id=admin_id,
        title="Employee Signed In",
        description=f"{emp_name} has signed in at {now.strftime('%I:%M %p')}.",
        type="attendance_sign_in",
        object_id=str(db_attendance.id),
        created_by_id=employee_id,
        created_by_type="employee",
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)


    return {
        "status": "true",
        "message": "Sign-in recorded successfully.",
        "data": {
            "attendance_id": db_attendance.id,
            "admin_id": admin_id,
            "employee_id": employee_id,
            "employee_id_id": employee.employee_id,
            "employee_name": employee.employe_name,
            "latitude": attendance_data.latitude,
            "longitude": attendance_data.longitude,
            "address": attendance_data.address,
            "image": attendance_data.sign_in_img,
            "in_time": sign_in_time_obj,
            "out_time": end_time_offset,
            "status": "sign-in",
            "late_minute": late_minute,
            "remark": attendance_data.remark.strip()
        }
    }



def check_in(db: Session, attendance_data: CheckIn):
    last_attendance = db.execute(
        select(Attendance)
        .where(Attendance.id == attendance_data.sign_in_id)
        .order_by(Attendance.created_at.desc())
    ).scalars().first()

    if not last_attendance:
        return {
            "status": "false",
            "message": "No previous attendance record found for this sign-in ID."
        }

    last_status_date = last_attendance.created_at.date()
    if last_status_date == date.today() and last_attendance.status == "sign-out":
        return {
            "status": "false",
            "message": "Employee has already signed out today. Check-in not allowed."
        }

    employee_id = last_attendance.employee_id
    admin_id = last_attendance.admin_id
    employee = db.execute(select(AdminAddEmployee).where(AdminAddEmployee.id == employee_id)).scalars().first()

    if not employee:
        return {
            "status": "false",
            "message": "Employee details not found."
        }

    shift_name = employee.shift_name
    shift_config = get_shift_times_for_employee(db, admin_id, shift_name)

    if not isinstance(shift_config, TimeConfig):
        return shift_config 

    # Retrieve the shift times based on shift_name
    if shift_name == 'shift-1':
        start_time = datetime.strptime(shift_config.start_time_1st, "%I:%M %p").time()
        end_time = datetime.strptime(shift_config.end_time_1st, "%I:%M %p").time()
        lunch_start_time = datetime.strptime(shift_config.lunch_time_start_1st, "%I:%M %p").time() if shift_config.lunch_time_start_1st else None
        lunch_end_time = datetime.strptime(shift_config.lunch_time_end_1st, "%I:%M %p").time() if shift_config.lunch_time_end_1st else None
    elif shift_name == 'shift-2':
        start_time = datetime.strptime(shift_config.start_time_2nd, "%I:%M %p").time()
        end_time = datetime.strptime(shift_config.end_time_2nd, "%I:%M %p").time()
        lunch_start_time = datetime.strptime(shift_config.lunch_time_start_2nd, "%I:%M %p").time() if shift_config.lunch_time_start_2nd else None
        lunch_end_time = datetime.strptime(shift_config.lunch_time_end_2nd, "%I:%M %p").time() if shift_config.lunch_time_end_2nd else None
    elif shift_name == 'shift-3':
        start_time = datetime.strptime(shift_config.start_time_3rd, "%I:%M %p").time()
        end_time = datetime.strptime(shift_config.end_time_3rd, "%I:%M %p").time()
        lunch_start_time = datetime.strptime(shift_config.lunch_time_start_3rd, "%I:%M %p").time() if shift_config.lunch_time_start_3rd else None
        lunch_end_time = datetime.strptime(shift_config.lunch_time_end_3rd, "%I:%M %p").time() if shift_config.lunch_time_end_3rd else None
    elif shift_name == 'shift-general':
        start_time = datetime.strptime(shift_config.start_time_general, "%I:%M %p").time()
        end_time = datetime.strptime(shift_config.end_time_general, "%I:%M %p").time()
        lunch_start_time = datetime.strptime(shift_config.lunch_time_start_general, "%I:%M %p").time() if shift_config.lunch_time_start_general else None
        lunch_end_time = datetime.strptime(shift_config.lunch_time_end_general, "%I:%M %p").time() if shift_config.lunch_time_end_general else None
    else:
        return {
            "status": "false",
            "message": "Invalid shift name."
        }

    # Get the current time for comparison
    current_time = datetime.now(TZ).time()

    print("---------- Debugging Time Values ----------")
    print(f"Current Time: {current_time.strftime('%I:%M %p')}")
    print(f"Shift Start Time: {start_time.strftime('%I:%M %p')}")
    print(f"Shift End Time: {end_time.strftime('%I:%M %p')}")
    print(f"Lunch Start Time: {lunch_start_time.strftime('%I:%M %p') if lunch_start_time else 'None'}")
    print(f"Lunch End Time: {lunch_end_time.strftime('%I:%M %p') if lunch_end_time else 'None'}")
    print("-------------------------------------------")

    
    if lunch_start_time and lunch_end_time and lunch_start_time <= current_time <= lunch_end_time:
        return {
            "status": "false",
            "message": "Check-in not allowed during lunch time."
        }

   
    if current_time > end_time:
        return {
            "status": "false",
            "message": "Check-in not allowed after the shift end time."
        }

    if current_time < start_time:
        return {
            "status": "false",
            "message": "Check-in not allowed before the shift start time."
        }

  
    new_check_in = Attendance(
        admin_id=last_attendance.admin_id,
        employee_id=last_attendance.employee_id,
        employee_name=last_attendance.employee_name,
        latitude=attendance_data.latitude,
        longitude=attendance_data.longitude,
        address=attendance_data.address,
        status=attendance_data.status,
        sign_in_id=str(attendance_data.sign_in_id),
        check_in_out_reason=attendance_data.check_in_out_reason,
    )

    db.add(new_check_in)
    db.commit()
    db.refresh(new_check_in)

    return {
        "status": "true",
        "message": "Check-in recorded successfully.",
        "data": new_check_in
    }



def check_out(db: Session, attendance_data: CheckOut):
    
    last_attendance = db.execute(
        select(Attendance)
        .where(Attendance.id == attendance_data.sign_in_id)
        .order_by(Attendance.created_at.desc())
    ).scalars().first()

   
    if not last_attendance:
        return {
            "status": "false",
            "message": "No previous attendance record found for this employee."
        }

    
    last_status_date = last_attendance.created_at.date()
    if last_status_date == date.today() and last_attendance.status == "sign-out":
        return {
            "status": "false",
            "message": "Employee has already signed out today. Check-out not allowed."
        }

    employee_id = last_attendance.employee_id
    admin_id = last_attendance.admin_id
    employee = db.execute(select(AdminAddEmployee).where(AdminAddEmployee.id == employee_id)).scalars().first()

    if not employee:
        return {
            "status": "false",
            "message": "Employee details not found."
        }

    shift_name = employee.shift_name
    shift_config = get_shift_times_for_employee(db, admin_id, shift_name)

    if not isinstance(shift_config, TimeConfig):
        return shift_config 

    
    if shift_name == 'shift-1':
        start_time = datetime.strptime(shift_config.start_time_1st, "%I:%M %p").time()
        end_time = datetime.strptime(shift_config.end_time_1st, "%I:%M %p").time()
        lunch_start_time = datetime.strptime(shift_config.lunch_time_start_1st, "%I:%M %p").time() if shift_config.lunch_time_start_1st else None
        lunch_end_time = datetime.strptime(shift_config.lunch_time_end_1st, "%I:%M %p").time() if shift_config.lunch_time_end_1st else None
    elif shift_name == 'shift-2':
        start_time = datetime.strptime(shift_config.start_time_2nd, "%I:%M %p").time()
        end_time = datetime.strptime(shift_config.end_time_2nd, "%I:%M %p").time()
        lunch_start_time = datetime.strptime(shift_config.lunch_time_start_2nd, "%I:%M %p").time() if shift_config.lunch_time_start_2nd else None
        lunch_end_time = datetime.strptime(shift_config.lunch_time_end_2nd, "%I:%M %p").time() if shift_config.lunch_time_end_2nd else None
    elif shift_name == 'shift-3':
        start_time = datetime.strptime(shift_config.start_time_3rd, "%I:%M %p").time()
        end_time = datetime.strptime(shift_config.end_time_3rd, "%I:%M %p").time()
        lunch_start_time = datetime.strptime(shift_config.lunch_time_start_3rd, "%I:%M %p").time() if shift_config.lunch_time_start_3rd else None
        lunch_end_time = datetime.strptime(shift_config.lunch_time_end_3rd, "%I:%M %p").time() if shift_config.lunch_time_end_3rd else None
    elif shift_name == 'shift-general':
        start_time = datetime.strptime(shift_config.start_time_general, "%I:%M %p").time()
        end_time = datetime.strptime(shift_config.end_time_general, "%I:%M %p").time()
        lunch_start_time = datetime.strptime(shift_config.lunch_time_start_general, "%I:%M %p").time() if shift_config.lunch_time_start_general else None
        lunch_end_time = datetime.strptime(shift_config.lunch_time_end_general, "%I:%M %p").time() if shift_config.lunch_time_end_general else None
    else:
        return {
            "status": "false",
            "message": "Invalid shift name."
        }

    current_time = datetime.now(TZ).time()

    
    print("---------- Debugging Time Values ----------")
    print(f"Current Time: {current_time.strftime('%I:%M %p')}")
    print(f"Shift Start Time: {start_time.strftime('%I:%M %p')}")
    print(f"Shift End Time: {end_time.strftime('%I:%M %p')}")
    print(f"Lunch Start Time: {lunch_start_time.strftime('%I:%M %p') if lunch_start_time else 'None'}")
    print(f"Lunch End Time: {lunch_end_time.strftime('%I:%M %p') if lunch_end_time else 'None'}")
    print("-------------------------------------------")

    
    if lunch_start_time and lunch_end_time and lunch_start_time <= current_time <= lunch_end_time:
        return {
            "status": "false",
            "message": "Check-out not allowed during lunch time."
        }

    
    if current_time > end_time:
        return {
            "status": "false",
            "message": "Check-out not allowed after the shift end time."
        }

    
    if current_time < start_time:
        return {
            "status": "false",
            "message": "Check-out not allowed before the shift start time."
        }

    
    new_check_out = Attendance(
        admin_id=last_attendance.admin_id,
        employee_id=last_attendance.employee_id,
        employee_name=last_attendance.employee_name,
        latitude=attendance_data.latitude,
        longitude=attendance_data.longitude,
        address=attendance_data.address,
        status=attendance_data.status,
        sign_in_id=str(attendance_data.sign_in_id),
        check_in_out_reason=attendance_data.check_in_out_reason,
    )

    db.add(new_check_out)
    db.commit()
    db.refresh(new_check_out)

    return {
        "status": "true",
        "message": "Check-out recorded successfully.",
        "data": new_check_out
    }






# def sign_out(db: Session, attendance_data: SignOut):
#     existing_sign_in = db.execute(
#         select(Attendance).where(
#             and_(
#                 Attendance.id == attendance_data.sign_in_id,
#                 Attendance.status == "sign-in",
#             )
#         )
#     ).scalars().first()


#     if not existing_sign_in:
#         return {"status": "false", "message": "Invalid sign_in_id. No matching sign-in record found."}

#     existing_sign_out = db.execute(
#         select(Attendance).where(
#             and_(
#                 Attendance.sign_in_id == str(attendance_data.sign_in_id),
#                 Attendance.status == "sign-out",
#             )
#         )
#     ).scalars().first()

#     if existing_sign_out:
#         return {"status": "false", "message": "Sign-out record already exists for this sign-in."}
    

#     employee = db.execute(select(AdminAddEmployee).where(AdminAddEmployee.id == attendance_data.employee_id)).scalars().first()
#     if not employee:
#         return {
#             "status": "false",
#             "message": f"Employee with ID {attendance_data.employee_id} does not exist."
#         }

#     employee_name = employee.employe_name

#     new_sign_out = Attendance(
#         admin_id=attendance_data.admin_id,
#         employee_id=attendance_data.employee_id,
#         employee_name=employee_name, 
#         latitude=attendance_data.latitude,
#         longitude=attendance_data.longitude,
#         address=attendance_data.address,
#         status="sign-out",
#         sign_in_id=str(attendance_data.sign_in_id),
#         image=attendance_data.sign_out_img,
#     )

#     db.add(new_sign_out)
#     db.commit()
#     db.refresh(new_sign_out)

#     return {"status": "true", "message": "Sign-out recorded successfully.", "data": new_sign_out}


def sign_out(db: Session, attendance_data: SignOut):
    existing_sign_in = db.execute(
        select(Attendance).where(
            and_(
                Attendance.id == attendance_data.sign_in_id,
                Attendance.status == "sign-in",
            )
        )
    ).scalars().first()

    if not existing_sign_in:
        return {"status": "false", "message": "Invalid sign_in_id. No matching sign-in record found."}

    existing_sign_out = db.execute(
        select(Attendance).where(
            and_(
                Attendance.sign_in_id == str(attendance_data.sign_in_id),
                Attendance.status == "sign-out",
            )
        )
    ).scalars().first()

    if existing_sign_out:
        return {"status": "false", "message": "Sign-out record already exists for this sign-in."}

    employee = db.execute(select(AdminAddEmployee).where(AdminAddEmployee.id == attendance_data.employee_id)).scalars().first()
    if not employee:
        return {
            "status": "false",
            "message": f"Employee with ID {attendance_data.employee_id} does not exist."
        }

    shift_config = get_shift_times_for_employee(db, attendance_data.admin_id, employee.shift_name)
    if not isinstance(shift_config, TimeConfig):
        return shift_config  

    
    if employee.shift_name == 'shift-1':
        end_time = datetime.strptime(shift_config.end_time_1st, "%I:%M %p").time()
    elif employee.shift_name == 'shift-2':
        end_time = datetime.strptime(shift_config.end_time_2nd, "%I:%M %p").time()
    elif employee.shift_name == 'shift-3':
        end_time = datetime.strptime(shift_config.end_time_3rd, "%I:%M %p").time()
    elif employee.shift_name == 'shift-general':
        end_time = datetime.strptime(shift_config.end_time_general, "%I:%M %p").time()
    else:
        return {"status": "false", "message": "Invalid shift name."}

    
    current_time = datetime.now()

   
    over_time = None
    if current_time.time() > end_time:
        shift_end_datetime = current_time.replace(hour=end_time.hour, minute=end_time.minute, second=0)
        overtime_duration = current_time - shift_end_datetime
        over_time = str(overtime_duration) 

    new_sign_out = Attendance(
        admin_id=attendance_data.admin_id,
        employee_id=attendance_data.employee_id,
        employee_name=employee.employe_name,
        latitude=attendance_data.latitude,
        longitude=attendance_data.longitude,
        address=attendance_data.address,
        status="sign-out",
        sign_in_id=str(attendance_data.sign_in_id),
        image=attendance_data.sign_out_img,
        over_time=over_time  
    )

    db.add(new_sign_out)
    db.commit()
    db.refresh(new_sign_out)


    emp_name = None
    employee = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == int(new_sign_out.employee_id)).first()
    if employee:
        emp_name = f"{employee.employe_name}({employee.employee_id})"

    # ? Notification for sign-out
    notification = Notification(
        admin_id=new_sign_out.admin_id,
        title="Employee Signed Out",
        description=f"{emp_name} has signed out at {current_time.strftime('%I:%M %p')}.",
        type="attendance_sign_out",
        object_id=str(new_sign_out.id),
        created_by_id=new_sign_out.employee_id,
        created_by_type="employee",
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)

    return {"status": "true", "message": "Sign-out recorded successfully.", "data": new_sign_out}





# def auto_sign_out_users(db: Session):
#     current_time = datetime.now()
#     sixteen_hours_ago = current_time - timedelta(hours=16)
#     print("sixteen_hours_ago",sixteen_hours_ago)

#     expired_sign_ins = db.query(Attendance).filter(
#         Attendance.status == "sign-in",
#     ).all()
#     print("expired_sign_ins",expired_sign_ins)

#     for sign_in in expired_sign_ins:
#         existing_sign_out = db.execute(
#             select(Attendance).where(
#                 and_(
#                     Attendance.sign_in_id == str(sign_in.id),
#                     Attendance.status == "sign-out",
#                 )
#             )
#         ).scalars().first()

#         if existing_sign_out:
#             continue  

        
#         employee = db.execute(
#             select(AdminAddEmployee).where(AdminAddEmployee.id == sign_in.employee_id)
#         ).scalars().first()
        
#         if not employee:
#             continue  

       
#         shift_config = get_shift_times_for_employee(db, sign_in.admin_id, employee.shift_name)
        
#         if not isinstance(shift_config, TimeConfig):
#             continue  

       
#         if employee.shift_name == 'shift-1':
#             shift_start_time = datetime.strptime(shift_config.start_time_1st, "%I:%M %p").time()
#         elif employee.shift_name == 'shift-2':
#             shift_start_time = datetime.strptime(shift_config.start_time_2nd, "%I:%M %p").time()
#         elif employee.shift_name == 'shift-3':
#             shift_start_time = datetime.strptime(shift_config.start_time_3rd, "%I:%M %p").time()
#         else:
#             continue  

        
#         shift_start_datetime = datetime.combine(sign_in.created_at.date(), shift_start_time)
#         sixteen_hours_later = shift_start_datetime + timedelta(hours=16)
#         print("shift_start_datetime",shift_start_datetime)
#         print("sixteen_hours_later",sixteen_hours_later)

        
#         if current_time < sixteen_hours_later:
#             continue  

        
#         new_sign_out = Attendance(
#             admin_id=sign_in.admin_id,
#             employee_id=sign_in.employee_id,
#             employee_name=sign_in.employee_name,
#             latitude=sign_in.latitude,  
#             longitude=sign_in.longitude,
#             address="Auto Sign-Out",
#             status="sign-out",
#             sign_in_id=str(sign_in.id),
#             image=None,
#             over_time="8:00:00"  
#         )

#         db.add(new_sign_out)

#     if expired_sign_ins:
#         db.commit()


        
        
        
def auto_sign_out_users(db: Session):
    current_time = datetime.now(TZ).time()

    expired_sign_ins = db.query(Attendance).filter(
        Attendance.status == "sign-in",
    ).all()

    for sign_in in expired_sign_ins:
        existing_sign_out = db.execute(
            select(Attendance).where(
                and_(
                    Attendance.sign_in_id == str(sign_in.id),
                    Attendance.status == "sign-out",
                )
            )
        ).scalars().first()

        if existing_sign_out:
            continue  

        employee = db.execute(
            select(AdminAddEmployee).where(AdminAddEmployee.id == sign_in.employee_id)
        ).scalars().first()
        
        if not employee:
            continue  

        shift_config = get_shift_times_for_employee(db, sign_in.admin_id, employee.shift_name)
        
        if not isinstance(shift_config, TimeConfig):
            continue  

        
        if employee.shift_name == 'shift-1':
            shift_end_time = datetime.strptime(shift_config.end_time_1st, "%I:%M %p").time()
        elif employee.shift_name == 'shift-2':
            shift_end_time = datetime.strptime(shift_config.end_time_2nd, "%I:%M %p").time()
        elif employee.shift_name == 'shift-3':
            shift_end_time = datetime.strptime(shift_config.end_time_3rd, "%I:%M %p").time()
        elif employee.shift_name == 'shift-general':
            shift_end_time = datetime.strptime(shift_config.end_time_general, "%I:%M %p").time()
        else:
            continue  

        
        shift_end_datetime = datetime.combine(sign_in.created_at.date(), shift_end_time)
        print("shift_end_datetime", shift_end_datetime)

        
        if current_time < shift_end_datetime.time():
            continue  

        
        new_sign_out = Attendance(
            admin_id=sign_in.admin_id,
            employee_id=sign_in.employee_id,
            employee_name=sign_in.employee_name,
            latitude=sign_in.latitude,  
            longitude=sign_in.longitude,
            address="Auto Sign-Out",
            status="sign-out",
            sign_in_id=str(sign_in.id),
            image=None,
            over_time=""  
        )

        db.add(new_sign_out)

    if expired_sign_ins:
        db.commit()





def start_sign_out_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=lambda: auto_sign_out_users(next(get_db())),  
        trigger="interval",  
        seconds=60 
    )
    scheduler.start()











def get_today_date_range():
    today_start = datetime.utcnow().date()
    today_end = today_start + timedelta(days=1)
    return today_start, today_end


def get_today_attendance(
    db: Session,
    employee_id: Optional[int] = None,
    admin_id: Optional[int] = None
) -> List[Attendance]:
    today_start, today_end = get_today_date_range()
    
   
    query = select(Attendance).where(
        Attendance.date_time >= today_start, 
        Attendance.date_time < today_end
    )

   
    if employee_id:
        query = query.where(Attendance.employee_id == employee_id)
    if admin_id:
        query = query.where(Attendance.admin_id == admin_id)

   
    results = db.execute(query).scalars().all()  

    
    for result in results:
        if result.late_minute is None:
            result.late_minute = 0

    return results



def get_date_range(from_date: Optional[datetime], to_date: Optional[datetime]):
    
    today_start = datetime.utcnow().date() if not from_date else from_date
    today_end = today_start + timedelta(days=1) if not to_date else to_date
    return today_start, today_end




def get_filtered_attendance(
    db: Session,
    admin_id: int,
    employee_id: Optional[int] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    employee_name: Optional[str] = None
) -> List[dict]:

    if from_date:
        from_date = from_date.date()
    if to_date:
        to_date = to_date.date()

    query = (
        select(Attendance, AdminAddEmployee)
        .join(AdminAddEmployee, Attendance.employee_id == AdminAddEmployee.id)
        .where(Attendance.admin_id == admin_id)
    )

    if from_date:
        query = query.where(func.date(Attendance.date_time) >= from_date)
    if to_date:
        query = query.where(func.date(Attendance.date_time) <= to_date)
    if employee_id:
        query = query.where(Attendance.employee_id == employee_id)
    if employee_name:
        query = query.where(AdminAddEmployee.employe_name.ilike(f"%{employee_name}%"))

    query = query.order_by(Attendance.date_time.desc())  
    results = db.execute(query).all()

    grouped_data = defaultdict(lambda: defaultdict(lambda: {"attendance": [], "employee_details": None}))

    for attendance, employee in results:
        date_key = attendance.date_time.date()
        employee_key = attendance.employee_id

        grouped_data[date_key][employee_key]["attendance"].append({
            "id": attendance.id,
            "admin_id": attendance.admin_id,
            "employee_id": attendance.employee_id,
            "latitude": attendance.latitude,
            "longitude": attendance.longitude,
            "date_time": attendance.date_time.isoformat(),
            "address": attendance.address,
            "sign_in_id": attendance.sign_in_id,
            "sign_out_id": attendance.sign_out_id,
            "late_minute": attendance.late_minute,
            "status": attendance.status,
            "check_in_id": attendance.check_in_id,
            "check_out_id": attendance.check_out_id,
            "check_in_out_reason": attendance.check_in_out_reason,
            "image": attendance.image,
            "over_time": attendance.over_time,
            "from_time": attendance.from_time,
            "end_time": attendance.end_time,
            "remark": attendance.remark,
            "over_time_remark":attendance.over_time_remark,
            "creator_info": get_creator_info(db =db ,admin_emp_id= attendance.admin_emp_id , created_by_type =  attendance.created_by_type),

        })

        if not grouped_data[date_key][employee_key]["employee_details"]:
            grouped_data[date_key][employee_key]["employee_details"] = {
                "id": employee.id,
                "admin_id": employee.admin_id,
                "employee_id": employee.employee_id,
                "employe_name": employee.employe_name,
                "employe_email_id": employee.employe_email_id,
                "employe_phone_number": employee.employe_phone_number,
                "employe_job_title": employee.employe_job_title,
                "level": employee.level,
                "skills": employee.skills,
                "experience": employee.experience,
                "position": employee.position,
            }

    
    serialized_results = []
    for date, employees in sorted(grouped_data.items(), key=lambda x: x[0], reverse=True):  
        for employee_id, data in employees.items():
           
            data["attendance"].sort(key=lambda x: x["date_time"])
            serialized_results.append({
                "date": str(date),
                "attendance": data["attendance"],
                "employee": data["employee_details"]
            })

    return serialized_results






def create_manual_attendance(db: Session, attendance_data: AttendanceMenualCreate):
    employee_id = attendance_data.employee_id
    today_start = datetime.utcnow().date()
    today_end = today_start + timedelta(days=1)

    
    employee = db.execute(select(AdminAddEmployee).where(AdminAddEmployee.id == employee_id)).scalars().first()
    if not employee:
        return {
            "status": "false",
            "message": f"Employee with ID {employee_id} does not exist."
        }

    employee_name = employee.employe_name

  
    existing_sign_in = db.execute(
        select(Attendance)
        .where(
            and_(
                Attendance.employee_id == employee_id,
                Attendance.date_time >= today_start,
                Attendance.date_time < today_end,
                Attendance.status == "Manual"
            )
        )
    ).scalars().first()

    if existing_sign_in:
        
        db.delete(existing_sign_in)
        db.commit()

        return {
            "status": "true",
            "message": "Previous sign-in record was removed. A new record can now be added."
        }

  
    db_attendance = Attendance(
        admin_id=attendance_data.admin_id,
        employee_id=attendance_data.employee_id,
        employee_name=employee_name,
        latitude=None, 
        longitude=None, 
        address=attendance_data.address,
        image=attendance_data.sign_in_img,
        status="Manual",
        date_time=attendance_data.date_time,
        from_time=attendance_data.from_time,
        end_time=attendance_data.end_time,
        late_minute = 0,
        remark=attendance_data.remark ,
        created_by_type=attendance_data.created_by_type ,
        admin_emp_id=attendance_data.admin_emp_id 
    )

    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)

    return {
        "status": "true",
        "message": "Manual sign-in recorded successfully.",
        "data": db_attendance
    }




# def get_employee_salary(db: Session, admin_id: int, emp_id: Optional[int] = None):
#     attendance_query = db.query(Attendance).filter(Attendance.admin_id == admin_id)
#     if emp_id:
#         attendance_query = attendance_query.filter(Attendance.employee_id == emp_id)

#     attendance_records = attendance_query.all()
#     if not attendance_records:
#         return {'status': 'false', 'message': 'No attendance records found for this employee.'}

#     employee = db.query(AdminAddEmployee).filter(AdminAddEmployee.admin_id == admin_id, AdminAddEmployee.id == emp_id).first()
#     if not employee:
#         return {'status': 'false', 'message': 'Employee not found.'}

#     time_config = db.query(TimeConfig).filter(TimeConfig.admin_id == admin_id).first()
#     if not time_config:
#         return {'status': 'false', 'message': 'Shift configuration not found for the employee.'}

#     weekly_holidays = time_config.weekly_holidays.split(",") if time_config.weekly_holidays else []
#     today = datetime.today()
#     total_days_of_month = monthrange(today.year, today.month)[1]

#     start_date = datetime(today.year, today.month, 1)
#     end_date = datetime(today.year, today.month, total_days_of_month)
#     all_dates = [start_date + timedelta(days=i) for i in range(total_days_of_month)]

    
#     weekly_holiday_dates = []
#     for date in all_dates:
#         day_of_week = date.strftime("%A")
#         week_of_month = (date.day - 1) // 7 + 1
#         if "All Sunday" in weekly_holidays and day_of_week == "Sunday":
#             weekly_holiday_dates.append(date.strftime("%d-%m-%Y"))
#         elif "All Saturday" in weekly_holidays and day_of_week == "Saturday":
#             weekly_holiday_dates.append(date.strftime("%d-%m-%Y"))
#         elif "2 Saturday(1st & 3rd)" in weekly_holidays and day_of_week == "Saturday" and week_of_month in (1, 3):
#             weekly_holiday_dates.append(date.strftime("%d-%m-%Y"))
#         elif "2 Saturday(2nd & 4th)" in weekly_holidays and day_of_week == "Saturday" and week_of_month in (2, 4):
#             weekly_holiday_dates.append(date.strftime("%d-%m-%Y"))

    
#     public_holidays_query = db.query(PublicHoliday).filter(
#         PublicHoliday.admin_id == admin_id,
#         PublicHoliday.event_date >= start_date,
#         PublicHoliday.event_date <= end_date
#     )
#     public_holiday_dates = [holiday.event_date.strftime("%d-%m-%Y") for holiday in public_holidays_query.all()]

   
#     attendance_dates = {record.date_time.date() for record in attendance_records}
#     present_dates = [date.strftime("%d-%m-%Y") for date in all_dates if date.date() in attendance_dates]
#     absent_dates = [
#         date.strftime("%d-%m-%Y") for date in all_dates
#         if date.strftime("%d-%m-%Y") not in present_dates + weekly_holiday_dates + public_holiday_dates
#     ]

#     total_holidays = len(weekly_holiday_dates) + len(public_holiday_dates)
#     total_working_days = total_days_of_month - total_holidays

#     monthly_salary = float(employee.employee_salary)
#     calculated_salary = monthly_salary / 30

#     response_data = EmployeeSalaryResponse(
#         employee_id=str(employee.id),
#         employee_name=employee.employe_name,
#         created_date=employee.created_at,
#         monthly_salary=monthly_salary,
#         calculated_salary=calculated_salary,
#         salary_slip_url="jhfhgfdg",
#         total_day_working=str(total_working_days),
#         public_holiday_dates=public_holiday_dates,
#         weekly_holiday_dates=weekly_holiday_dates,
#         absent_date=absent_dates,
#         present_date=present_dates,
#         total_days_of_month=total_days_of_month,
#         employee_code=str(employee.employee_id),
#         designation=employee.employe_job_title if employee.employe_job_title else None,
#         pan_no="",
#         account_no="",
#         bank_name="",
#         paid_leave=0,
#         dearness_allowance=0.0,
#         HRA=0.0,
#         medical_allowance="No",
#         PF=0.0,
#         professional_tax=0.0,
#         TDS=0.0,
        
#     )

#     return {
#         'status': 'true',
#         'message': 'Salary details fetched successfully.',
#         'data': response_data.dict()
#     }




from src.LateMark.models import LateMark

    
    
def get_employee_salary(db: Session, admin_id: int, emp_id: Optional[int] = None):
    attendance_query = db.query(Attendance).filter(Attendance.admin_id == admin_id)
    if emp_id:
        attendance_query = attendance_query.filter(Attendance.employee_id == emp_id)

    attendance_records = attendance_query.all()
    
    
    employee = db.query(AdminAddEmployee).filter(AdminAddEmployee.admin_id == admin_id, AdminAddEmployee.id == emp_id).first()
    if not employee:
        return {'status': 'false', 'message': 'Employee not found.'}
        
    employeeFile = db.query(EmployeeFiles).filter(EmployeeFiles.admin_id == admin_id, EmployeeFiles.employee_id == emp_id).first()

    time_config = db.query(TimeConfig).filter(TimeConfig.admin_id == admin_id).first()
    if not time_config:
        return {'status': 'false', 'message': 'Shift configuration not found for the employee.'}

    weekly_holidays = time_config.weekly_holidays.split(",") if time_config.weekly_holidays else []
    today = datetime.today()
    total_days_of_month = monthrange(today.year, today.month)[1]

    start_date = datetime(today.year, today.month, 1)
    end_date = datetime(today.year, today.month, total_days_of_month)
    all_dates = [start_date + timedelta(days=i) for i in range(total_days_of_month)]

    weekly_holiday_dates = []
    for date in all_dates:
        day_of_week = date.strftime("%A")
        week_of_month = (date.day - 1) // 7 + 1
        if "All Sunday" in weekly_holidays and day_of_week == "Sunday":
            weekly_holiday_dates.append(date.strftime("%d-%m-%Y"))
        elif "All Saturday" in weekly_holidays and day_of_week == "Saturday":
            weekly_holiday_dates.append(date.strftime("%d-%m-%Y"))
        elif "2 Saturday(1st & 3rd)" in weekly_holidays and day_of_week == "Saturday" and week_of_month in (1, 3):
            weekly_holiday_dates.append(date.strftime("%d-%m-%Y"))
        elif "2 Saturday(2nd & 4th)" in weekly_holidays and day_of_week == "Saturday" and week_of_month in (2, 4):
            weekly_holiday_dates.append(date.strftime("%d-%m-%Y"))

    public_holidays_query = db.query(PublicHoliday).filter(
        PublicHoliday.admin_id == admin_id,
        PublicHoliday.event_date >= start_date,
        PublicHoliday.event_date <= end_date
    )
    public_holiday_dates = [holiday.event_date.strftime("%d-%m-%Y") for holiday in public_holidays_query.all()]

    attendance_dates = {record.date_time.date() for record in attendance_records}
    present_dates = [date.strftime("%d-%m-%Y") for date in all_dates if date.date() in attendance_dates] if attendance_records else []
    absent_dates = [
        date.strftime("%d-%m-%Y") for date in all_dates
        if date.strftime("%d-%m-%Y") not in present_dates + weekly_holiday_dates + public_holiday_dates
    ]

    total_holidays = len(weekly_holiday_dates) + len(public_holiday_dates)
    total_working_days = total_days_of_month - total_holidays

    monthly_salary = float(employee.employee_salary)
    calculated_salary = monthly_salary / 30

    # Step 1: Get employee's assigned shift type
    employee_shift = employee.shift_name  # e.g., "General Shift", "Shift 1", etc.

    # Step 2: Filter LateMark settings by shift type and config
    shift_latemarks = db.query(LateMark).filter(
        LateMark.config_id == time_config.id,
        LateMark.type == employee_shift
    ).all()

    # Step 3: Count how many absent days (or late days, depending on your policy)
    total_absent_days = len(absent_dates)

    # Step 4: Calculate total deduction
    deduction_amount = 0.0


    for day in range(1, total_absent_days + 1):
        lm = next((lm for lm in shift_latemarks if lm.select_type == day), None)
        if not lm:
            lm = shift_latemarks[-1] if shift_latemarks else None
        if lm:
            amount_value = float(lm.amount or 0)
            if lm.amount_type == "Amount":
                deduction_amount += amount_value
            elif lm.amount_type == "Percentage":
                deduction_amount += (monthly_salary * amount_value / 100)


    # Step 5: Final salary after deduction
    net_salary = monthly_salary - deduction_amount


    response_data = EmployeeSalaryResponse(
        employee_id=str(employee.id),
        employee_name=employee.employe_name,
        bank_name=employee.bank_name,
        bank_account_holder_name=employee.bank_account_holder_name,
        bank_account_number=employee.bank_account_number,
        bank_ifsc_code=employee.bank_ifsc_code,
        pan_card=employee.pan_card,
        house_rent_allowance=employee.house_rent_allowance,
        dearness_allowance=employee.dearness_allowance,
        medical_allowance=employee.medical_allowance,
        special_allowance=employee.special_allowance,
        bonus=employee.bonus,
        telephone_reimbursement=employee.telephone_reimbursement,
        fuel_reimbursement=employee.fuel_reimbursement,
        created_date=employee.created_at,
        monthly_salary=monthly_salary,
        calculated_salary=calculated_salary,
        salary_slip_url="jhfhgfdg",
        total_day_working=str(total_working_days),
        public_holiday_dates=public_holiday_dates,
        weekly_holiday_dates=weekly_holiday_dates,
        absent_date=absent_dates,
        present_date=present_dates,
        total_days_of_month=total_days_of_month,
        employee_code=str(employee.employee_id),
        designation=employee.employe_job_title if employee.employe_job_title else None,
        medical_file = employeeFile.medical_file_path,
        m_file_name = employeeFile.m_file_name,
        pan_no="",
        account_no="",
        paid_leave=0,
        professional_tax=0.0,
        TDS=0.0,
        net_salary=0.0,
        deduction_amount=0.0,
    )


    return {
        'status': 'true',
        'message': 'Salary details fetched successfully.',
        'data': response_data.dict()
    }


def delete_attendance(db: Session, salary_request: DeleteAtt):
    attendance_query = db.query(Attendance).filter(
        Attendance.admin_id == int(salary_request.admin_id),
        Attendance.employee_id == int(salary_request.emp_id),
        Attendance.id == int(salary_request.id)
    ).first()

    if not attendance_query:
        return {
            'status': "false",
            'message': 'Attendance not found.'
        }

    db.delete(attendance_query)
    db.commit()

    return {
        'status': "true",
        'message': 'Attendance deleted successfully.'
    }


from .models import AttendanceOvertimeCreate

from datetime import datetime, time

def create_overtime(db: Session, overtime_data: AttendanceOvertimeCreate):
    employee_id = int(overtime_data.employee_id)
    admin_id = int(overtime_data.admin_id)

    today = get_current_datetime().date()
    start_datetime = datetime.combine(today, time.min)  
    end_datetime = datetime.combine(today, time.max)    

    query = db.query(Attendance).filter(
        Attendance.admin_id == admin_id,
        Attendance.employee_id == employee_id,
        Attendance.date_time.between(start_datetime, end_datetime)
    )

    attendance_record = query.first()
    if not attendance_record:
        return {
            "status": "false",
            "message": "Attendance record not found."
        }

    if attendance_record.status != "sign-out":
        return {
            "status": "false",
            "message": "Sign-out required before recording overtime."
        }
    
    if attendance_record.over_time not in [None, "Null"]:
        return {
            "status": "false",
            "message": "Overtime has already been recorded for this attendance."
        }

    attendance_record.over_time = overtime_data.over_time
    attendance_record.over_time_remark = overtime_data.over_time_remark

    db.commit()
    db.refresh(attendance_record)

    return {
        "status": "true",
        "message": "Overtime recorded successfully.",
        "data": attendance_record
    }

