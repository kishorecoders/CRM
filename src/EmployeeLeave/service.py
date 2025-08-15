from .models import EmployeeLeave
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from src.EmployeeLeave.models import EmployeeLeaveCreate,EmployeeLeaveStatusUpdate,EmployeeLeaveUpdate,EmployeeLeaveDelete
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from fastapi import HTTPException
from src.parameter import get_current_datetime
from src.Notifications.models import Notification



def create(db: Session, leave: EmployeeLeaveCreate):
    
    start_date = datetime.combine(leave.start_date, datetime.min.time())
    end_date = datetime.combine(leave.end_date, datetime.max.time())

   
    overlapping_leave = db.query(EmployeeLeave).filter(
        EmployeeLeave.employee_id == leave.employee_id,
        EmployeeLeave.start_date <= end_date,
        EmployeeLeave.end_date >= start_date,
    ).first()

    if overlapping_leave:
        return JSONResponse(
            status_code=200,
            content={
                'status': 'false',
                'message': "Leave already exists for the selected dates."
            }
        )

   
    db_leave = EmployeeLeave(
        admin_id=leave.admin_id,
        employee_id=leave.employee_id,
        leave_type=leave.leave_type,
        start_date=start_date,
        end_date=end_date,
        leave_priority=leave.leave_priority,
        pdf_file_or_image=leave.pdf_file_or_image,
        type=leave.type,
        leave_matter=leave.leave_matter,
        status=leave.status,
        half_or_full_day=leave.half_or_full_day,
        created_by_type=leave.created_by_type,
        admin_emp_id=leave.admin_emp_id,
    )
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)

    emp_name = None
    employee = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == int(db_leave.employee_id)).first()
    if employee:
        emp_name = f"{employee.employe_name}({employee.employee_id})"

    # Create notification for leave application
    notification = Notification(
        admin_id=leave.admin_id,
        title="Leave Application Submitted",
        description=f"Employee {emp_name} has applied for leave from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}.",
        type="leave_applied",
        object_id=str(db_leave.id),
        created_by_id=leave.admin_emp_id,
        created_by_type=leave.created_by_type,
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    
    response = {
        'status': 'true',
        'message': "Leave Details Added Successfully",
        'data': {
            "id": db_leave.id,
            "admin_id": db_leave.admin_id,
            "employee_id": db_leave.employee_id,
            "leave_type": db_leave.leave_type,
            "start_date": db_leave.start_date.strftime("%Y-%m-%d"),
            "end_date": db_leave.end_date.strftime("%Y-%m-%d"),
            "leave_priority": db_leave.leave_priority,
            "pdf_file_or_image": db_leave.pdf_file_or_image,
            "type": db_leave.type,
            "leave_matter": db_leave.leave_matter,
            "status": db_leave.status,
            "half_or_full_day":db_leave.half_or_full_day,
        }
    }
    return response



from src.AdminAddEmployee.models import AdminAddEmployee
from src.cre_upd_name import get_creator_updator_infos

def get_leave_list_service(
    db: Session, admin_id: Optional[str] = None, employee_id: Optional[str] = None
) -> List[dict]:
    try:
        query = select(EmployeeLeave).order_by(EmployeeLeave.id.desc())

        if admin_id:
            query = query.where(EmployeeLeave.admin_id == admin_id)
        if employee_id:
            query = query.where(EmployeeLeave.employee_id == employee_id)

        leaves = db.execute(query).scalars().all()
        leave_list = []

        for leave in leaves:

            created_updated_data = get_creator_updator_infos(
            admin_emp_id=leave.admin_emp_id,
            created_by_type=leave.created_by_type,
            updated_admin_emp_id=leave.updated_admin_emp_id,
            updated_by_type=leave.updated_by_type,

            rejacted_admin_emp_id=leave.rejacted_admin_emp_id,
            rejacted_by_type=leave.rejacted_by_type,
            approve_admin_emp_id=leave.approve_admin_emp_id,
            approve_by_type=leave.approve_by_type,
            db=db
        )

            update = leave.updated_at
            create = leave.created_at
            approve_updated_at = leave.approve_updated_at
            rejacted_updated_at = leave.rejacted_updated_at

            created_updated_data["creator_info"]["created_at"] = create
            created_updated_data["updater_info"]["updated_at"] = update
            created_updated_data["rejacted_info"]["rejacted_updated_at"] = rejacted_updated_at
            created_updated_data["approve_info"]["approve_updated_at"] = approve_updated_at


            emp = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == leave.employee_id).first()
            employe_name = emp.employe_name if emp and emp.employe_name else "Unknown"

            leave_data = leave.dict()
            leave_data["start_date"] = leave.start_date.strftime("%Y-%m-%d %I:%M %p")
            leave_data["end_date"] = leave.end_date.strftime("%Y-%m-%d %I:%M %p")
            leave_data["employe_name"] = employe_name

            leave_list.append({**leave_data, **created_updated_data})

        return leave_list

    except Exception as e:
        raise Exception(f"Error fetching leave list: {str(e)}")



from datetime import datetime
from datetime import datetime, timezone

def update_leave_status(
    db: Session, 
    leave_data: EmployeeLeaveStatusUpdate
):
   
    leave_record = db.query(EmployeeLeave).filter(
        EmployeeLeave.id == leave_data.leave_id,
        EmployeeLeave.admin_id == leave_data.admin_id,
        EmployeeLeave.employee_id == leave_data.employee_id
    ).first()
    
    
    if not leave_record:
        raise HTTPException(status_code=200, detail="Leave record not found")
    

    if leave_data.status == "Rejected" and leave_record.status == "Approved":
        date_t = get_current_datetime()
        approved_date = leave_record.approve_updated_at

        if not approved_date:
            raise HTTPException(status_code=400, detail="Approval date not found for this leave record.")

        # Ensure approve_updated_at is timezone aware, if not assume UTC
        if approved_date.tzinfo is None:
            approved_date = approved_date.replace(tzinfo=timezone.utc)

        diff_minutes = (date_t - approved_date).total_seconds() / 60

        if diff_minutes > 30:
            raise HTTPException(
                status_code=400,
                detail="Cannot change approval status after 30 minutes of approval."
            )

    if leave_data.status == "Approved":
        leave_record.approve_by_type = leave_data.approve_by_type
        leave_record.approve_admin_emp_id = leave_data.approve_admin_emp_id
        leave_record.approve_updated_at = get_current_datetime()

    if leave_data.status == "Rejected":
        leave_record.rejacted_by_type = leave_data.rejacted_by_type
        leave_record.rejacted_admin_emp_id = leave_data.rejacted_admin_emp_id
        leave_record.rejacted_updated_at = get_current_datetime()




    leave_record.status = leave_data.status
    leave_record.remark = leave_data.remark
    leave_record.updated_at = datetime.utcnow()

    db.add(leave_record)
    db.commit()
    db.refresh(leave_record)

    
    return leave_record



def update_leave_details(db: Session, leave_update: EmployeeLeaveUpdate):
   
    leave = db.query(EmployeeLeave).filter(
        EmployeeLeave.id == leave_update.leave_id,
        EmployeeLeave.admin_id == leave_update.admin_id,
        EmployeeLeave.employee_id == leave_update.employee_id
    ).first()

    if not leave:
        return JSONResponse(
            status_code=200,
            content={
                'status': 'false',
                'message': 'Leave record not found for the provided details.'
            }
        )

   
    update_fields = [
        "leave_type",
        "start_date",
        "end_date",
        "leave_priority",
        "pdf_file_or_image",
        "type",
        "leave_matter",
        "status",
        "remark",
        "half_or_full_day",
        "updated_by_type",
        "updated_admin_emp_id"
    ]
    for field in update_fields:
        new_value = getattr(leave_update, field)
        if new_value is not None:
            setattr(leave, field, new_value)

    leave.updated_at = get_current_datetime()

    db.commit()
    db.refresh(leave)

    response = {
        'status': 'true',
        'message': 'Leave details updated successfully',
        'data': {
            "id": leave.id,
            "admin_id": leave.admin_id,
            "employee_id": leave.employee_id,
            "leave_type": leave.leave_type,
            "start_date": leave.start_date.strftime("%Y-%m-%d") if leave.start_date else None,
            "end_date": leave.end_date.strftime("%Y-%m-%d") if leave.end_date else None,
            "leave_priority": leave.leave_priority,
            "pdf_file_or_image": leave.pdf_file_or_image,
            "type": leave.type,
            "leave_matter": leave.leave_matter,
            "status": leave.status,
            "remark": leave.remark,
            "half_or_full_day": leave.half_or_full_day,
        }
    }
    return response



def delete_leave_record(db: Session, leave_delete: EmployeeLeaveDelete):
    
    leave = db.query(EmployeeLeave).filter(
        EmployeeLeave.id == leave_delete.leave_id,
        EmployeeLeave.admin_id == leave_delete.admin_id,
        EmployeeLeave.employee_id == leave_delete.employee_id
    ).first()

   
    if not leave:
        return JSONResponse(
            status_code=200,
            content={
                "status": "false",
                "message": "Leave record not found for the provided details."
            }
        )

   
    db.delete(leave)
    db.commit()

    return {
        "status": "true",
        "message": "Leave record deleted successfully"
    }


from datetime import datetime, date
from sqlalchemy import cast, Date

def update_expired_EmployeeLeave(db: Session):
    current_date = datetime.now().date()  # Get only the date part

    expired_leaves = db.query(EmployeeLeave).filter(
        cast(EmployeeLeave.end_date, Date) <= current_date,
        EmployeeLeave.status != "Expired"
    ).all()

    for leave in expired_leaves:
        leave.status = "Expired"

    db.commit()
    
    
    
    
