from .models import Meetingplanned,MeetingplannedCreate,MeetingplannedReadRequest
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status,HTTPException
from src.AdminSales.models import AdminSales
from src.AdminAddEmployee.models import AdminAddEmployee
from src.Activity.models import ActivityCenter


def create(db: Session, meeting_planned: MeetingplannedCreate):
    
    db_meeting_planned = Meetingplanned(**meeting_planned.dict())
    db.add(db_meeting_planned)
    db.commit()
    db.refresh(db_meeting_planned)

    
    db_activity = ActivityCenter(
        admin_sales_id=meeting_planned.admin_sales_id,
        employe_id=meeting_planned.employe_id,
        activiity_message=meeting_planned.meeting_discription,
        type=f"Meeting : {meeting_planned.meeting_date} {meeting_planned.meeting_time}",
        admin_emp_id=meeting_planned.admin_emp_id,
        created_by_type=meeting_planned.created_by_type,
        meeting_discription=meeting_planned.meeting_discription,
        meeting_link=meeting_planned.meeting_link,
    )

    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)

    response = {
        "status": "true",
        "message": "Meeting and Activity Add Successfully",
        "data": db_meeting_planned,
    }
    return response


from src.cre_upd_name import get_creator_info

def get_meeting_details_post(read_request: MeetingplannedReadRequest, db: Session):
    valid_statuses = ['Pending', 'Completed', 'Canceled']

    query = db.query(Meetingplanned).filter(Meetingplanned.admin_id == read_request.admin_id)

    if read_request.lead_id:
        query = query.filter(Meetingplanned.admin_sales_id == read_request.lead_id)

    if read_request.employee_id:
        query = query.filter(Meetingplanned.employe_id == read_request.employee_id)

    if read_request.meeting_status and read_request.meeting_status in valid_statuses:
        query = query.filter(Meetingplanned.meeting_status == read_request.meeting_status)

    meetings = query.order_by(Meetingplanned.id.desc()).all()

    data_array = [] 

    
    for meeting in meetings:
    
        creater_info = get_creator_info(admin_emp_id=meeting.admin_emp_id ,created_by_type=meeting.created_by_type ,db=db)
    
        admin_details = db.query(AdminSales).filter(AdminSales.id == meeting.admin_sales_id).all()
        
        employee_details = []
        if meeting.employe_id:
            try:
                employee_id = int(meeting.employe_id)
                employee_details = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == employee_id).all()
            except (ValueError, TypeError):
                # Invalid employe_id, leave employee_details empty
                print(f"Skipping invalid employe_id: {meeting.employe_id}")
        
        lead_details = []
        if read_request.name and read_request.name != '':
            for admin_detail in admin_details:
                if read_request.name.lower() in admin_detail.name.lower():
                    lead_details = admin_detail
                    break  
        else:
            lead_details = admin_details[0] if admin_details else []

        data = meeting.__dict__.copy()
        data['creater_info'] = creater_info

        temp = {
            'Meeting_details': data,
            'Lead_details': lead_details,
            'Employee_details': employee_details
        }

        data_array.append(temp)

    response = {
        'status': 'true',
        'message': "Data Received Successfully",
        'data': data_array
    }

    return response




def get_meeting_details(lead_id: int, employee_id: str, meeting_status: Optional[str], name: Optional[str], db: Session):
    valid_statuses = ['Pending', 'Completed', 'Canceled']

    if meeting_status and meeting_status in valid_statuses:
        meetings = db.query(Meetingplanned).filter(
            Meetingplanned.admin_sales_id == lead_id,
            Meetingplanned.employe_id == employee_id,
            Meetingplanned.meeting_status == meeting_status
        ).order_by(Meetingplanned.id.desc()).all()
    else:
        meetings = db.query(Meetingplanned).filter(
            Meetingplanned.admin_sales_id == lead_id,
            Meetingplanned.employe_id == employee_id
        ).order_by(Meetingplanned.id.desc()).all()

    data_array = []

    
    for meeting in meetings:
        admin_details = db.query(AdminSales).filter(AdminSales.id == meeting.admin_sales_id).all()
        employee_details = db.query(AdminAddEmployee).filter(AdminAddEmployee.employee_id == meeting.employe_id).all()

        
        lead_details = []
        if name and name != '':
            for admin_detail in admin_details:
                if name.lower() in admin_detail.name.lower():
                    lead_details = admin_detail
                    break  
        else:
            lead_details = admin_details[0] if admin_details else []

        temp = {
            'Meeting_details': meeting,
            'Lead_details': lead_details,
            'Employee_details': employee_details
        }

        data_array.append(temp)

    response = {
        'status': 'true',
        'message': "Data Received Successfully",
        'data': data_array
    }

    return response

# def get_meeting_details_by_employee(employee_id: str, meeting_status: Optional[str], name: Optional[str], db: Session):
#     valid_statuses = ['Pending', 'Completed', 'Canceled']

#     if meeting_status and meeting_status in valid_statuses:
#         meetings = db.query(Meetingplanned).filter(
#             Meetingplanned.employe_id == employee_id,
#             Meetingplanned.meeting_status == meeting_status
#         ).all()
#     else:
#         meetings = db.query(Meetingplanned).filter(
#             Meetingplanned.employe_id == employee_id
#         ).all()

#     data_array = []

#     # Process meeting records
#     for meeting in meetings:
#         admin_details = db.query(AdminSales).filter(AdminSales.id == meeting.admin_sales_id).all()
#         employee_details = db.query(AdminAddEmployee).filter(AdminAddEmployee.employee_id == meeting.employe_id).all()

#         # Search within admin_details for the name parameter if it exists
#         lead_details = []
#         if name and name != '':
#             for admin_detail in admin_details:
#                 if name.lower() in admin_detail.name.lower():
#                     lead_details = admin_detail
#                     break  # Stop the loop if found
#         else:
#             # If no name parameter provided, assign the first lead detail
#             lead_details = admin_details[0] if admin_details else []


#         temp = {
#             'Meeting_details': meeting,
#             'Lead_details': lead_details,
#             'Employee_details': employee_details
#         }

#         data_array.append(temp)

#     response = {
#         'status': 'true',
#         'message': "Data Received Successfully",
#         'data': data_array
#     }

#     return response

def get_meeting_details_by_employee(employee_id: str, meeting_status: Optional[str], name: Optional[str], db: Session):
    valid_statuses = ['Pending', 'Completed', 'Canceled']

    if meeting_status and meeting_status in valid_statuses:
        meetings = db.query(Meetingplanned).filter(
            Meetingplanned.employe_id == employee_id,
            Meetingplanned.meeting_status == meeting_status
        ).order_by(Meetingplanned.id.desc()).all()
    else:
        meetings = db.query(Meetingplanned).filter(
            Meetingplanned.employe_id == employee_id
        ).order_by(Meetingplanned.id.desc()).all()

    data_array = []

    
    for meeting in meetings:
        admin_details = db.query(AdminSales).filter(AdminSales.id == meeting.admin_sales_id).all()
        employee_details = db.query(AdminAddEmployee).filter(AdminAddEmployee.employee_id == meeting.employe_id).all()

        
        filtered_admin_details = []
        if name and name != '':
            for admin_detail in admin_details:
                if name.lower() in admin_detail.name.lower():
                    filtered_admin_details.append(admin_detail)
        else:
            filtered_admin_details = admin_details

       
        if filtered_admin_details:
            temp = {
                'Meeting_details': meeting,
                'Lead_details': filtered_admin_details[0],  
                'Employee_details': employee_details
            }
            data_array.append(temp)

    response = {
        'status': 'true',
        'message': "Data Received Successfully",
        'data': data_array
    }

    return response

def update(meeting_id:int,meeting_planned:Meetingplanned,db:Session):
    meeting_planned_update = meeting_planned.dict(exclude_unset=True)
    db.query(Meetingplanned).filter(Meetingplanned.id == meeting_id).update(meeting_planned_update)
    db.commit()
    response = {'status': 'true','message':"Data Updated Successfully",'data':meeting_planned_update}
    return response

def delete_meeting(id: int, db: Session):
    meeting_details = db.query(Meetingplanned).filter(Meetingplanned.id == id).first()

    if not meeting_details:
       {'status': 'false', 'message': "Meeting Not Found"}

    db.delete(meeting_details)
    db.commit()

    response = {
        'status': 'true',
        'message': "Meeting deleted successfully"
    }
    
    return response 
    
    


def update_expired_meetings(db: Session):
    current_datetime = datetime.now()
    print("Running meeting expiration check at", current_datetime)

    expired_meetings = db.query(Meetingplanned).filter(
        Meetingplanned.meeting_status != "Meeting Done",
        Meetingplanned.meeting_date <= current_datetime.date()
    ).all()

    for meeting in expired_meetings:
        if meeting.meeting_time:
            try:
                meeting_datetime = datetime.combine(
                    meeting.meeting_date,
                    datetime.strptime(meeting.meeting_time.strip(), "%I:%M %p").time()
                )
            except ValueError:
                print(f"Invalid time format for meeting ID {meeting.id}: {meeting.meeting_time}")
                continue

            if meeting_datetime < current_datetime:
                print(f"Marking meeting ID {meeting.id} as 'Meeting Done'")
                meeting.meeting_status = "Meeting Done"
                db.add(meeting)
        else:
            if meeting.meeting_date < current_datetime.date():
                print(f"Marking meeting ID {meeting.id} as 'Meeting Done' (no time provided)")
                meeting.meeting_status = "Meeting Done"
                db.add(meeting)

    db.commit()



