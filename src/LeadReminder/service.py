from .models import LeadReminder, LeadReminderCreate
from sqlmodel import Session
from src.Settings.models import Setting
from sqlalchemy import cast
from sqlalchemy.types import String
from datetime import datetime
from sqlalchemy import desc
from typing import List, Optional,Dict
from src.AdminSales.models import AdminSales
from sqlalchemy import and_, func,text


# def create(db: Session, reminder_create: LeadReminderCreate):
#     db_reminder = LeadReminder(**reminder_create.dict())
#     db.add(db_reminder)
#     db.commit()
#     db.refresh(db_reminder)
#     response = {'status': 'true', 'message': "Lead Reminder Added Successfully", 'data': db_reminder}
#     return response



# def create(db: Session, reminder_create: LeadReminderCreate):
    
#     normalized_time = reminder_create.reminder_time.replace(second=0, microsecond=0)

   
#     existing_reminder = db.query(LeadReminder).filter(
#         and_(
#             LeadReminder.admin_id == reminder_create.admin_id,
#             LeadReminder.employee_id == reminder_create.employee_id,
#             text("strftime('%Y-%m-%d %H:%M', lead_reminder.reminder_time) = :normalized_time")
#         )
#     ).params(normalized_time=normalized_time.strftime('%Y-%m-%d %H:%M')).first()

#     if existing_reminder:
#         return {
#             'status': 'false',
#             'message': 'This reminder time has already been added.'
#         }

    
#     reminder_data = reminder_create.dict()
#     reminder_data['reminder_time'] = normalized_time 

   
#     db_reminder = LeadReminder(**reminder_data)
#     db.add(db_reminder)
#     db.commit()
#     db.refresh(db_reminder)

#     return {
#         'status': 'true',
#         'message': "Lead Reminder Added Successfully",
#         'data': db_reminder
#     }


def create(db: Session, reminder_create: LeadReminderCreate):
    normalized_time = reminder_create.reminder_time.replace(second=0, microsecond=0)

    existing_reminder = db.query(LeadReminder).filter(
        and_(
            LeadReminder.admin_id == reminder_create.admin_id,
            LeadReminder.employee_id == reminder_create.employee_id,
            text("DATE_FORMAT(lead_reminder.reminder_time, '%Y-%m-%d %H:%i') = :normalized_time")
        )
    ).params(normalized_time=normalized_time.strftime('%Y-%m-%d %H:%M')).first()

    if existing_reminder:
        return {
            'status': 'false',
            'message': 'This reminder time has already been added.'
        }

    reminder_data = reminder_create.dict()
    reminder_data['reminder_time'] = normalized_time 

    db_reminder = LeadReminder(**reminder_data)
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)

    return {
        'status': 'true',
        'message': "Lead Reminder Added Successfully",
        'data': db_reminder
    }



def get_lead_reminders_with_details(db: Session, admin_id: int, employee_id: Optional[str] = None) -> List[Dict]:
    
    query = db.query(LeadReminder).filter(LeadReminder.admin_id == admin_id)
    if employee_id:
        query = query.filter(LeadReminder.employee_id == employee_id)
    
    reminders = query.order_by(desc(LeadReminder.id)).all()

    
    response_data = []
    for reminder in reminders:
        lead_details = db.query(AdminSales).filter(AdminSales.id == reminder.Lead_id).first()
        reminder_dict = reminder.dict() 
        reminder_dict["lead_details"] = lead_details.dict() if lead_details else None
        response_data.append(reminder_dict)

    return response_data



def update_lead_reminder(db: Session, reminder_id: int, update_data: dict):
    reminder = db.query(LeadReminder).filter(LeadReminder.id == reminder_id).first()
    if not reminder:
        return {"status": "false", "message": "Reminder not found"}
    
    for key, value in update_data.items():
        setattr(reminder, key, value)
    
    reminder.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(reminder)
    return {"status": "true", "message": "Reminder updated successfully", "data": reminder}




def delete_lead_reminder(db: Session, reminder_id: int, admin_id: int, employee_id: int):
    
    reminder = db.query(LeadReminder).filter(
        LeadReminder.id == reminder_id,
        LeadReminder.admin_id == admin_id,
        LeadReminder.employee_id == employee_id  
    ).first()

    if not reminder:
        return {"status": "false", "message": "Reminder not found or access denied"}
    
    db.delete(reminder)
    db.commit()
    return {"status": "true", "message": "Reminder deleted successfully"}
