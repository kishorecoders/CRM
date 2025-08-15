from .models import AdminSales, AdminSalesCreate , AdminSalesM,Leadcount
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status, HTTPException, Query
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew
from src.AdminAddEmployee.models import AdminAddEmployee
from src.RoleAssignByLevel.models import RoleAssignByLevel
from src.parameter import get_current_datetime
from sqlmodel import Session, select
from datetime import date
from sqlalchemy import and_, func
from datetime import date, timedelta, datetime
from sqlalchemy import cast, Date
from itertools import chain  # Useful for flattening lists
from src.ProjectManagerOrder.models import ProjectManagerOrder
from src.Quotation.models import Quotation
from src.Activity.models import ActivityCenter
from src.Meetingplanned.models import Meetingplanned
from src.ActivityComment.models import ActivityComment
from src.QuotationProductEmployee.models import QuotationProductEmployee

from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew
from src.AdminAddEmployee.models import AdminAddEmployee
import json
from src.Account.service import save_base64_file
import json
from src.Account.service import save_base64_file
from src.ProjectManagerResourseFile.models import ProjectManagerResourseFile
from src.EmployeeLeave.models import EmployeeLeave
from src.EmployeeTasks.models import TaskRequest
from src.Attendance.models import Attendance
from src.StoreManagerProduct.models import storeManagerProduct
from src.Notifications.models import Notification
from src.Notifications.models import Notification
from src.FCM import sendPush

def get_all_admin_sales(db: Session):
    data = db.query(AdminSales).order_by(AdminSales.id.desc()).all()
    response = {'status': 'true', 'message': "Data Received Successfully", 'data': data}
    return response


def create(db: Session, admin_sales: AdminSalesCreate):
    gst_number = admin_sales.gst_number
    
    if admin_sales.created_by_type and admin_sales.admin_emp_id:
        if admin_sales.created_by_type == "admin":
            query = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == admin_sales.admin_emp_id).first()
            name = query.full_name
            admin_sales.lead_source_name = name
        elif admin_sales.created_by_type == "employee":
            query = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == admin_sales.admin_emp_id).first()
            id = query.employee_id
            name = query.employe_name
            admin_sales.lead_source_name =f"{name}({id})"

    is_duplicate_mobile = False
    if admin_sales.contact_details:
        existing_mobile = db.query(AdminSales).filter(AdminSales.contact_details == admin_sales.contact_details).first()
        if existing_mobile:
            is_duplicate_mobile = True

    # Set the is_duplicate flag
    admin_sales_dict = admin_sales.dict()
    admin_sales_dict["is_duplicate"] = is_duplicate_mobile

    db_admin_sales = AdminSales(**admin_sales_dict)
    db.add(db_admin_sales)
    db.commit()
    db.refresh(db_admin_sales)
    
    # Create notification for the admin
    notification = Notification(
        admin_id=admin_sales.admin_id,
        title="New Lead Created",
        description=f"Lead {db_admin_sales.name} has been created by {db_admin_sales.lead_source_name}",
        type="lead_creation",
        object_id=str(db_admin_sales.id),
        created_by_id= db_admin_sales.admin_emp_id,
        created_by_type=db_admin_sales.created_by_type,
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    
    if admin_sales.created_by_type == "employee":
        token = None
        token = db.query(SuperAdminUserAddNew.device_token).filter(
            SuperAdminUserAddNew.id == admin_sales.admin_id
        ).first()
        if token:
            token = token.device_token
        sendPush(
            msg=f"Lead {db_admin_sales.name} has been created by {db_admin_sales.lead_source_name}",
            token=token,
            title="New Lead Created",
            data={
                "lead_id": str(db_admin_sales.id),
                "action": "lead_created"
            }
        )
    
    response = {'status': 'true', 'message': "Lead Added Successfully", 'data': db_admin_sales}
    return response




def create_multi(db: Session, admin_sales: AdminSalesM):

    # Step 1: Get all employees under the admin
    employees = db.query(AdminSales).filter(
        AdminSales.admin_id == admin_sales.admin_id
    ).all()

    employee_ids = list(set(emp.allocated_emplyee_id for emp in employees if emp.allocated_emplyee_id))

    if not employee_ids:
        return {"status": "false", "message": "No employees found for this admin."}

    # Step 2: Get the current lead count for each employee
    employee_lead_count = {
        emp_id: db.query(AdminSales).filter(
            AdminSales.admin_id == admin_sales.admin_id,
            AdminSales.allocated_emplyee_id == str(emp_id)
        ).count()
        for emp_id in employee_ids
    }

    # Step 3: Sort employees by lead count (ascending order)
    sorted_employees = sorted(employee_lead_count.items(), key=lambda x: x[1])
    employee_queue = [emp_id for emp_id, _ in sorted_employees]

    # Step 4: Distribute leads in round-robin across the sorted employee list
    total_leads = admin_sales.Leads
    allocated_leads = []
    index = 0

    for _ in range(len(total_leads)):
        allocated_leads.append(employee_queue[index])
        index = (index + 1) % len(employee_queue)

    # Step 5: Identify lead source name
    lead_source_name = ""
    if admin_sales.created_by_type and admin_sales.admin_emp_id:
        if admin_sales.created_by_type == "admin":
            query = db.query(SuperAdminUserAddNew).filter(
                SuperAdminUserAddNew.id == admin_sales.admin_emp_id
            ).first()
            lead_source_name = query.full_name if query else ""
        elif admin_sales.created_by_type == "employee":
            query = db.query(AdminAddEmployee).filter(
                AdminAddEmployee.id == admin_sales.admin_emp_id
            ).first()
            if query:
                lead_source_name = f"{query.employe_name}({query.employee_id})"

    created_leads = []
    skipped_leads = []

    for index, lead_data in enumerate(admin_sales.Leads):

        allocated_employee_id = allocated_leads[index]

        lead_dict = lead_data.dict()
        lead_dict.update({
            "admin_id": admin_sales.admin_id,
            "created_by_type": admin_sales.created_by_type,
            "admin_emp_id": admin_sales.admin_emp_id,
            "lead_source_name": lead_source_name,
            "allocated_emplyee_id": str(allocated_employee_id)
        })

        db_lead = AdminSales(**lead_dict)
        db.add(db_lead)
        db.commit()
        db.refresh(db_lead)
        # Create notification for the admin
        notification = Notification(
            admin_id=admin_sales.admin_id,
            title="New Lead Created",
            description=f"Lead {db_lead.name} has been created by {db_lead.lead_source_name}",
            type="lead_creation",
            object_id=str(db_lead.id),
            created_by_id= db_lead.admin_emp_id,
            created_by_type=db_lead.created_by_type,
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)

        # Send push notification to the allocated employee
        if admin_sales.created_by_type == "employee":
            token = None
            token = db.query(SuperAdminUserAddNew.device_token).filter(
                SuperAdminUserAddNew.id == admin_sales.admin_id
            ).first()
            if token:
                token = token.device_token
            sendPush(
                msg=f"Lead {db_lead.name} has been created by {db_lead.lead_source_name}",
                token=token,
                title="New Lead Created",
                data={
                    "lead_id": str(db_lead.id),
                    "action": "lead_created"
                }
            )


        created_leads.append(lead_dict)

    return {
        "status": "true" if created_leads else "false",
        "message": (
            f"{len(created_leads)} lead(s) added successfully."
            if created_leads else
            "No leads were added."
        ),
        "created": created_leads,
    }


import re
from src.cre_upd_name import get_creator_updator_info
from src.cre_upd_name import get_creator_info, get_creator_updator_info
from sqlalchemy import or_, func

def normalize_mobile(mobile: str) -> str:
    digits = re.sub(r'\D', '', mobile)  # Remove non-digit characters
    return digits[-10:]  # Get last 10 digits


def get_admin_sales_by_multi_id(
    db: Session,
    admin_id: int,
    employe_id: Optional[str] = None,
    status: Optional[str] = None,
    lead_source: Optional[str] = None,
    lead_name: Optional[str] = None,
    lead_from_date: Optional[datetime] = None,
    lead_to_date: Optional[datetime] = None,
    mobile_num: Optional[str] = None,
    lead_id_from: Optional[str] = None,
    lead_id_to: Optional[str] = None,
    time_frame: Optional[str] = None,
    page: Optional[int] = None,  # Allow None to fetch all records
    page_size: Optional[int] = None,  # Allow None to fetch all records
):
    admin_sales_query = db.query(AdminSales).filter(AdminSales.admin_id == admin_id)

    if employe_id:
        admin_sales_query = admin_sales_query.filter(AdminSales.allocated_emplyee_id.like(f'%{employe_id}%'))


    if status == "Not_Won":
        admin_sales_query = admin_sales_query.filter(
            or_(
                AdminSales.status.is_(None),
                AdminSales.status == "",
                func.lower(func.trim(AdminSales.status)) != "won"
            )
        )
    elif status:
        admin_sales_query = admin_sales_query.filter(
            func.lower(func.trim(AdminSales.status)) == status.lower()
        )


    if mobile_num:
        normalized_mobile = normalize_mobile(mobile_num)
        admin_sales_query = admin_sales_query.filter(
            AdminSales.contact_details.like(f"%{normalized_mobile}%")
        )


    if lead_source:
        admin_sales_query = admin_sales_query.filter(AdminSales.lead_source == lead_source)

    if lead_name:
        admin_sales_query = admin_sales_query.filter(AdminSales.name == lead_name)

    # Handle time frame filtering
    if time_frame:
        now = datetime.now()
        if time_frame == "Today":
            start_of_day = datetime(now.year, now.month, now.day)
            admin_sales_query = admin_sales_query.filter(
                func.date(AdminSales.created_at) == start_of_day.date()
            )
        elif time_frame == "Yesterday":
            start_of_yesterday = datetime(now.year, now.month, now.day) - timedelta(days=1)
            admin_sales_query = admin_sales_query.filter(
                func.date(AdminSales.created_at) == start_of_yesterday.date()
            )
        elif time_frame == "Last seven days":
            seven_days_ago = now - timedelta(days=7)
            admin_sales_query = admin_sales_query.filter(
                func.date(AdminSales.created_at) >= seven_days_ago.date()
            )
        elif time_frame == "This month":
            start_of_month = datetime(now.year, now.month, 1)
            admin_sales_query = admin_sales_query.filter(
                func.date(AdminSales.created_at) >= start_of_month.date()
            )

    # Handle date range filtering
    if lead_from_date and lead_to_date:
        admin_sales_query = admin_sales_query.filter(
            and_(
                func.date(AdminSales.created_at) >= lead_from_date.date(),
                func.date(AdminSales.created_at) <= lead_to_date.date()
            )
        )
    elif lead_from_date:
        admin_sales_query = admin_sales_query.filter(func.date(AdminSales.created_at) >= lead_from_date.date())
    elif lead_to_date:
        admin_sales_query = admin_sales_query.filter(func.date(AdminSales.created_at) <= lead_to_date.date())

    # Handle lead ID filtering
    if lead_id_from and lead_id_to:
        admin_sales_query = admin_sales_query.filter(
            and_(
                AdminSales.id >= lead_id_from,
                AdminSales.id <= lead_id_to
            )
        )
    elif lead_id_from:
        admin_sales_query = admin_sales_query.filter(AdminSales.id >= lead_id_from)
    elif lead_id_to:
        admin_sales_query = admin_sales_query.filter(AdminSales.id <= lead_id_to)

    # Get total count before pagination
    total_count = admin_sales_query.count()

    # **Pagination Logic**
    if page and page_size:  # Apply pagination only if page and page_size are provided
        start_index = (page - 1) * page_size
        admin_sales_query = admin_sales_query.order_by(AdminSales.id.desc()).offset(start_index).limit(page_size)
    else:  
        admin_sales_query = admin_sales_query.order_by(AdminSales.id.desc())  # No pagination, fetch all

    admin_sales = admin_sales_query.all()

    # Determine previous and next page existence
    has_previous = page > 1 if page else False
    has_next = (start_index + page_size) < total_count if page and page_size else False

    # Prepare response data
    data_array = []
    for admin_sale in admin_sales:

        created_updated_data = get_creator_updator_info(
            admin_emp_id=admin_sale.admin_emp_id,
            created_by_type=admin_sale.created_by_type,
            updated_admin_emp_id=admin_sale.updated_admin_emp_id,
            updated_by_type=admin_sale.updated_by_type,
          db=db
        )

        allocated_employee = None
        if admin_sale.allocated_emplyee_id and admin_sale.allocated_emplyee_id.isdigit():
            allocated_employee = get_creator_info(
                admin_emp_id=admin_sale.allocated_emplyee_id,
                created_by_type="employee",
                db=db
            )

        admin_details = db.query(SuperAdminUserAddNew).filter(
            SuperAdminUserAddNew.id == admin_sale.admin_id
        ).all()
        employee_details = db.query(AdminAddEmployee).filter(
            AdminAddEmployee.id == admin_sale.allocated_emplyee_id
        ).all()

        temp = {
            'Admin_sales_details': {**vars(admin_sale).copy(), "allocated_employee_details": allocated_employee if allocated_employee else None},

            'Admin_details': admin_details,
            'employee_details': employee_details
        }
        data_array.append({**temp,**created_updated_data})

    response = {
        'status': 'true',
        'message': "Data Received Successfully",
        'total_count': total_count,
        'page': page if page else "All",
        'page_size': page_size if page_size else "All",
        'total_pages': (total_count // page_size) + (1 if total_count % page_size > 0 else 0) if page_size else 1,
        'previous': has_previous,
        'next': has_next,
        'data': data_array
    }

    return response  


def get_admin_sales(admin_id: int, employe_id: Optional[str], name: Optional[str], db: Session):
    admin_sales_query = db.query(AdminSales).filter(AdminSales.admin_id == admin_id)

    if employe_id is not None:
        admin_sales_query = admin_sales_query.filter(AdminSales.allocated_emplyee_id.ilike(f"%{employe_id}%"))

    admin_sales = admin_sales_query.order_by(AdminSales.created_at.desc()).all()
    data_array = []

    for admin_sale in admin_sales:
        admin_details = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == admin_sale.admin_id).all()
        employee_details = db.query(AdminAddEmployee).filter(
            AdminAddEmployee.employee_id == admin_sale.allocated_emplyee_id).all()

        if admin_details and employee_details:
            admin_details = admin_details[0]

            matches = not name or any(
                str(name).lower() in str(value).lower() for value in [
                    admin_sale.status,
                    admin_sale.lead_source,
                    admin_sale.name
                ]
            )

            if name is None or matches:
                temp = {
                    'Admin_sales_details': admin_sale,
                    'Admin_details': admin_details,
                    'employee_details': employee_details
                }
                data_array.append(temp)

    response = {
        'status': 'true',
        'message': "Data Received Successfully",
        'data': data_array
    }

    return response


def get_admin_sales_search_two(admin_id: int, search_term: Optional[str], db: Session):
    admin_sales_query = db.query(AdminSales).filter(AdminSales.admin_id == admin_id)

    if search_term is not None:
        admin_sales_query = admin_sales_query.filter(
            (
                    (AdminSales.lead_source.ilike(f"%{search_term}%") | (
                        AdminSales.lead_status.ilike(f"%{search_term}%")))
                    & (AdminSales.admin_id == admin_id)
            )
            |(
                db.query(AdminAddEmployee)
                .filter(
                    (AdminAddEmployee.employe_name.ilike(f"%{search_term}%") & (AdminAddEmployee.admin_id == admin_id))
                    & (AdminAddEmployee.employee_id == AdminSales.allocated_emplyee_id)
                )
                .exists()
            )
        )

    admin_sales = admin_sales_query.all()
    data_array = []

    for admin_sale in admin_sales:
        admin_details = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == admin_sale.admin_id).all()
        employee_details = db.query(AdminAddEmployee).filter(
            AdminAddEmployee.employee_id == admin_sale.allocated_emplyee_id).all()

        if admin_details and employee_details:
            admin_details = admin_details[0]

            temp = {
                'Admin_sales_details': admin_sale,
                'Admin_details': admin_details,
                'employee_details': employee_details
            }
            data_array.append(temp)

    response = {
        'status': 'true',
        'message': "Data Received Successfully",
        'data': data_array
    }

    return response




def get_lead_count(admin_id: int, employee_id: str, db: Session):
    
    employee_leads_query = db.query(AdminSales).filter(AdminSales.admin_id == admin_id)
    if employee_id:
        employee_leads_query = employee_leads_query.filter(
            AdminSales.allocated_emplyee_id.ilike(f"%{employee_id}%")
        )

   
    hot_leads_count = employee_leads_query.filter(AdminSales.status == "Hot").count()

    won_leads_count = employee_leads_query.filter(AdminSales.status == "Won").count()

    
    # meeting_done_count = employee_leads_query.filter(AdminSales.lead_status == "Meeting Done").count()

    if employee_id:
        meeting_done_count = db.query(Meetingplanned).filter(
            Meetingplanned.admin_id == admin_id,
            Meetingplanned.employe_id == employee_id,
            Meetingplanned.meeting_status == "Meeting Done"
        ).count()
    else:
        meeting_done_count = db.query(Meetingplanned).filter(
            Meetingplanned.admin_id == admin_id,
            Meetingplanned.meeting_status == "Meeting Done"
        ).count()

    # quotation_sent_count = employee_leads_query.filter(Quotation.quotation_status == 1).count()

    if employee_id:
        quotation_sent_count = db.query(Quotation).filter(
            Quotation.admin_id == admin_id,
            Quotation.employe_id == employee_id,
            Quotation.quotation_status == 1
        ).count()
    else:
        quotation_sent_count = db.query(Quotation).filter(
            Quotation.admin_id == admin_id,
            Quotation.quotation_status == 1
        ).count()
    
    employee_leads = employee_leads_query.all()
    employee_id_count = sum(
        1 for lead in employee_leads if employee_id in (lead.allocated_emplyee_id or "").split(',')
    )

    
    role_assignments = db.query(RoleAssignByLevel.employe_id_to).filter(
        RoleAssignByLevel.employe_id_from == employee_id
    ).all()

    
    all_assigned_employees = set(
        chain.from_iterable(role.employe_id_to or [] for role in role_assignments)
    )
    assigned_employee_count = len(all_assigned_employees)


    task = db.query(TaskRequest).filter(TaskRequest.admin_id == admin_id)
    if employee_id:
        task = task.filter(TaskRequest.emp_id_from == employee_id)  # add filter instead of new query

    task_count = task.count()

    attendance = db.query(Attendance).filter(Attendance.admin_id == admin_id)
    if employee_id:
        attendance = attendance.filter(Attendance.employee_id == employee_id)

    attendance_count = attendance.count()

    leave = db.query(EmployeeLeave).filter(EmployeeLeave.admin_id == admin_id)
    if employee_id:
        leave = leave.filter(EmployeeLeave.employee_id == employee_id)

    leave_count = leave.count()

    inventry = db.query(storeManagerProduct).filter(storeManagerProduct.admin_id == admin_id)
    if employee_id:
        inventry = inventry.filter(storeManagerProduct.emplpoyee_id == employee_id)

    inventry_count = inventry.count()

    # Response
    response = {
        'status': 'true',
        'message': "Data Received Successfully",
        'data': {
            'employee_id': employee_id,
            'lead_count': employee_id_count,
            'hot_leads_count': hot_leads_count,
            'won_leads_count': won_leads_count,
            'meeting_done_count': meeting_done_count,
            'quotation_sent_count': quotation_sent_count,
            'assigned_employee_count': assigned_employee_count,
            
            'inventry_count': inventry_count,
            'leave_count': leave_count,
            'task_count': task_count,
            'attendence_count': attendance_count
        }
    }

    return response




def delete_admin_sales(id: int, db: Session):
    
    admin_sales = db.query(AdminSales).filter(AdminSales.id == id).first()

    if not admin_sales:
        return {'status': 'false', 'message': "Admin Sales Details Not Found"}

    if admin_sales.status == "Won":
        return {'status': 'false', 'message': "Cannot delete a lead with status 'Won'."}
    
    if db.query(Quotation).filter(Quotation.lead_id == str(id)).first():
        return {'status': 'false', 'message': "Cannot delete lead because a quotation exists for this lead."}

    
    db.query(Quotation).filter(Quotation.lead_id == id).delete()

    
    activity_entries = db.query(ActivityCenter).filter(ActivityCenter.admin_sales_id == id).all()

    
    for activity in activity_entries:
        db.query(ActivityComment).filter(ActivityComment.activity_id == str(activity.id)).delete()

    db.query(ActivityCenter).filter(ActivityCenter.admin_sales_id == id).delete()

    
    db.query(Meetingplanned).filter(Meetingplanned.admin_sales_id == id).delete()

    
    # db.query(QuotationProductEmployee).filter(QuotationProductEmployee.lead_id == id).delete()

   
    db.delete(admin_sales)
    db.commit()

    response = {
        'status': 'true',
        'message': "Admin Sales Details and related records deleted successfully"
    }
    return response


    


def show_all_count(admin_id: int, db: Session):
    total_data_count = db.query(AdminSales).filter(AdminSales.admin_id == admin_id).count()

    hot_leads_count = db.query(AdminSales).filter(AdminSales.admin_id == admin_id,
                                                  AdminSales.status == "Hot").count()

    meeting_done_count = db.query(AdminSales).filter(AdminSales.admin_id == admin_id,
                                                     AdminSales.lead_status == "Meeting_Done").count()

    response = {
        'status': 'true',
        'message': "Data Received Successfully",
        'total_lead': total_data_count,
        'hot_leads_count': hot_leads_count,
        'meeting_done_count': meeting_done_count
    }

    return response


def check_quotation_exists(lead_id: int, db: Session) -> bool:
    return db.query(Quotation).filter(Quotation.lead_id == str(lead_id)).first() is not None
    
    
    

def generate_order_id(db: Session, admin_id: str):
    admin_company_name = db.query(SuperAdminUserAddNew.company_name).filter(SuperAdminUserAddNew.id == admin_id).scalar()
    short_name = admin_company_name[:4].upper()
    current_year = datetime.now().year % 100
    next_year = current_year + 1
    
    prefix = f"{short_name}/{current_year:02d}-{next_year:02d}/"
    latest_order = (
        db.query(func.max(ProjectManagerOrder.order_id))
        .filter(ProjectManagerOrder.order_id.like(f"{prefix}%"))
        .scalar()
    )

    existing_order_number = int(latest_order.split('/')[-1]) if latest_order else 0
    new_order_number = existing_order_number + 1
    return f"{prefix}{new_order_number:03d}"
    


def update_admin_sales(admin_sales_id: int, admin_sales_data: AdminSalesCreate, db: Session):
    # updated_data = admin_sales_data.dict(exclude_unset=True)

    updated_data = admin_sales_data.dict(exclude_unset=True, exclude={"files"})
    uploaded_files = []  # collect file info for the response

    if admin_sales_data.created_by_type == "employee":
        updated_by_type = "employee"
        updated_admin_emp_id = admin_sales_data.admin_emp_id
    else:
        updated_by_type = "admin"
        updated_admin_emp_id = admin_sales_data.admin_id  



    if admin_sales_data.files:
        file_data = []
        for f in admin_sales_data.files:
            current_datetime = datetime.now().strftime("%Y%m%d%H%M%S%f")
            # file_extension = "pdf" if f.file_type == "pdf" else "jpg"
            file_extension = "pdf"
            filename = f"{current_datetime}_{f.file_name}.{file_extension}"
            path = save_base64_file(f.file_path, filename)
            # Create file data dict
            file_info = {
                "file_name": f.file_name,
                "file_path": path
            }
            uploaded_files.append(file_info)
            file_data.append(file_info)

            # Store file info in ProjectManagerResourseFile
            res_file = ProjectManagerResourseFile(
                admin_id=admin_sales_data.admin_id,
                emp_id=admin_sales_data.allocated_emplyee_id,
                lead_id=str(admin_sales_id),
                file_path=json.dumps(file_info)
            )
            db.add(res_file)
        #updated_data["file_path"] = json.dumps(file_data)

        
    if updated_data.get('mark_status') == 'Mark Complete':
        admin_sales_record = db.query(AdminSales).filter(AdminSales.id == admin_sales_id).first()
        
        if not admin_sales_record:
            return {'status': 'false', 'message': 'Admin sales record not found'}


        # if not check_quotation_exists(admin_sales_record.id, db):
        #     return {'status': 'false', 'message': 'Please add a quotation before marking complete'}
        

        updated_data['status'] = 'Won'
        updated_data['updated_by_type'] = updated_by_type
        updated_data['updated_admin_emp_id'] = updated_admin_emp_id
        
    db.query(AdminSales).filter(AdminSales.id == admin_sales_id).update(updated_data)
    db.commit()

    admin_sales_dt = db.query(AdminSales).filter(AdminSales.id == admin_sales_id).first()
    # Create notification

    # Notification creation based on mark_status
    if updated_data.get('mark_status') == 'Mark Complete':
        notification = Notification(
            admin_id=admin_sales_data.admin_id,
            title="Lead Marked as Complete",
            description=f"Lead {admin_sales_dt.name} has been marked as complete.",
            type="lead_mark_complete",
            object_id=str(admin_sales_dt.id),
            created_by_id=updated_admin_emp_id,
            created_by_type=updated_by_type,
        )
    else:
        notification = Notification(
            admin_id=admin_sales_data.admin_id,
            title="Lead Status Changed",
            description=f"Lead {admin_sales_dt.name} Status has been changed to {updated_data.get('status')}",
            type="lead_Status_changed",
            object_id=str(admin_sales_dt.id),
            created_by_id=updated_admin_emp_id,
            created_by_type=updated_by_type,
        )
    db.add(notification)
    db.commit()
    db.refresh(notification)

        
    if "file_path" in updated_data and isinstance(updated_data["file_path"], str):
        try:
            updated_data["file_path"] = json.loads(updated_data["file_path"])
        except Exception:
            updated_data["file_path"] = []

    return {'status': 'true', 
            'message': "Data Updated Successfully", 
            'data': updated_data,
            "uploaded_files": uploaded_files 
            }










def get_admin_sales_name(db: Session, admin_id: str):
    data = db.query(AdminSales).filter(AdminSales.admin_id == admin_id).order_by(AdminSales.id.desc()).all()
    
    response_data = [{'id': admin_sale.id, 'name': admin_sale.name, 'email': admin_sale.email, 'company_name': admin_sale.business_name, 'contact_number': admin_sale.contact_details} for admin_sale in data]
    
    response = {'status': 'true', 'message': "Data Received Successfully", 'data': response_data}
    return response




def lead_assign_employee(
    db: Session, lead_ids: list[int], employee_id: str, admin_id: int
):
    admin_sales = (
        db.query(AdminSales)
        .filter(AdminSales.id.in_(lead_ids), AdminSales.admin_id == admin_id)
        .all()
    )

    if not admin_sales:
        raise HTTPException(
            status_code=404, detail="Lead not available in the database."
        )

    already_assigned = []
    not_assigned = []

    for sale in admin_sales:
        if sale.allocated_emplyee_id:
            already_assigned.append(sale.id)  
        else:
            sale.allocated_emplyee_id = employee_id
            sale.lead_status = "Assigned"  # Update the lead_status to "Assigned"
            sale.updated_at = get_current_datetime()
            not_assigned.append(sale.id)

    if already_assigned:
        return {
            "status": "false",
            "message": f"The following lead IDs are already assigned",
        }

    db.commit()

    return {
        "status": "true",
        "message": "Leads successfully assigned to the employee.",
    }




def get_allocated_leads(db: Session, admin_id: int, employee_id: str):
    
    allocated_leads = (
        db.query(AdminSales)
        .filter(AdminSales.admin_id == admin_id, AdminSales.allocated_emplyee_id == employee_id)
        .all()
    )

    if not allocated_leads:
        return {"status": "false", "message": "No leads found for this employee."}

    
    return allocated_leads




def get_today_allocated_leads(db: Session, admin_id: int, employee_id: str):
    today = date.today()

   
    today_leads = (
        db.query(AdminSales)
        .filter(
            and_(
                AdminSales.admin_id == admin_id,
                AdminSales.allocated_emplyee_id == employee_id,
                func.date(AdminSales.created_at) == today
            )
        )
        .all()
    )

    if not today_leads:
        return {"status": "false", "message": "No leads found for this employee today."}

    return today_leads






# def reassign_leads(
#     db: Session, lead_ids: list[int], from_employee_id: str, to_employee_id: str, admin_id: int
# ):
#     admin_sales = db.query(AdminSales).filter(
#                 AdminSales.id.in_(lead_ids),
#                 AdminSales.admin_id == admin_id,
#             ).all()
#     if from_employee_id :
#         admin_sales = db.query(AdminSales).filter(
#                 AdminSales.id.in_(lead_ids),
#                 AdminSales.allocated_emplyee_id == from_employee_id,
#                 AdminSales.admin_id == admin_id,
#             ).all()
        
        
#     if not admin_sales:
#         return {
#         "status": "false",
#         "message": f"No leads found assigned to the current employee.",
#     }
        
#     for sale in admin_sales:
#         sale.allocated_emplyee_id = to_employee_id
#         sale.updated_at = get_current_datetime()

#     db.commit()

#     return {
#         "status": "true",
#         "message": f"Leads successfully reassigned from employee {from_employee_id} to {to_employee_id}.",
#     }    

 
    
    

def reassign_leads(
    db: Session, lead_ids: list[int], from_employee_id: str, to_employee_id: str, admin_id: int
):
    # Fetch target employee details using employee_id
    target_employee = db.query(AdminAddEmployee).filter(
        AdminAddEmployee.id == to_employee_id,
        AdminAddEmployee.admin_id == admin_id
    ).first()

    if not target_employee:
        return {
            "status": "false",
            "message": f"Employee with ID {to_employee_id} not found."
        }

    employee_display_name = f"{target_employee.employe_name} ({target_employee.employee_id})"

    # Prepare sales query
    admin_sales_query = db.query(AdminSales).filter(
        AdminSales.id.in_(lead_ids),
        AdminSales.admin_id == admin_id,
    )

    if from_employee_id:
        admin_sales_query = admin_sales_query.filter(
            AdminSales.allocated_emplyee_id == from_employee_id
        )

    admin_sales = admin_sales_query.all()

    if not admin_sales:
        return {
            "status": "false",
            "message": "No leads found assigned to the current employee.",
        }

    # Check if all leads are already assigned
    if all(sale.allocated_emplyee_id == to_employee_id for sale in admin_sales):
        return {
            "status": "false",
            "message": f"Already assigned the lead to {employee_display_name}.",
        }

    updated_count = 0
    for sale in admin_sales:
        if sale.allocated_emplyee_id != to_employee_id:
            sale.allocated_emplyee_id = to_employee_id
            sale.updated_at = get_current_datetime()
            updated_count += 1

    db.commit()

    return {
        "status": "true",
        "message": f"Lead reassign to {employee_display_name}.",
    }

    
    
    

def remove_admin_sales(lead_id: int, admin_id: Optional[int], employee_id: Optional[str], db: Session):
    
    admin_sales = db.query(AdminSales).filter(AdminSales.id == lead_id).first()

    if not admin_sales:
        return {'status': 'false', 'message': "Admin Sales Details Not Found"}

   
    if admin_id and admin_sales.admin_id != admin_id:
        return {'status': 'false', 'message': "Admin ID does not match. You cannot delete this lead."}
    
    if employee_id and admin_sales.allocated_emplyee_id != employee_id:
        return {'status': 'false', 'message': "Employee ID does not match. You cannot delete this lead."}

    if db.query(Quotation).filter(Quotation.lead_id == str(lead_id)).first():
        return {'status': 'false', 'message': "Cannot delete lead because a quotation exists for this lead."}

        

    db.query(Quotation).filter(Quotation.lead_id == lead_id).delete()
    activity_entries = db.query(ActivityCenter).filter(ActivityCenter.admin_sales_id == lead_id).all()

    for activity in activity_entries:
        db.query(ActivityComment).filter(ActivityComment.activity_id == str(activity.id)).delete()

    db.query(ActivityCenter).filter(ActivityCenter.admin_sales_id == lead_id).delete()
    db.query(Meetingplanned).filter(Meetingplanned.admin_sales_id == lead_id).delete()

    
    db.delete(admin_sales)
    db.commit()

    return {'status': 'true', 'message': "Admin Sales Details and related records deleted successfully"}




def get_lead_count_main(request: Leadcount, db: Session):
    
    employee_leads_query = db.query(AdminSales).filter(AdminSales.admin_id == request.admin_id)
    if request.employee_id:
        employee_leads_query = employee_leads_query.filter(
            AdminSales.allocated_emplyee_id.ilike(f"%{request.employee_id}%")
        )

   
    hot_leads_count = employee_leads_query.filter(AdminSales.status == "Hot").count()

    won_leads_count = employee_leads_query.filter(AdminSales.status == "Won").count()

    
    # meeting_done_count = employee_leads_query.filter(AdminSales.lead_status == "Meeting Done").count()

    if request.employee_id:
        meeting_done_count = db.query(Meetingplanned).filter(
            Meetingplanned.admin_id == request.admin_id,
            Meetingplanned.employe_id == request.employee_id,
            Meetingplanned.meeting_status == "Meeting Done"
        ).count()
    else:
        meeting_done_count = db.query(Meetingplanned).filter(
            Meetingplanned.admin_id == request.admin_id,
            Meetingplanned.meeting_status == "Meeting Done"
        ).count()

    # quotation_sent_count = employee_leads_query.filter(Quotation.quotation_status == 1).count()

    if request.employee_id:
        quotation_sent_count = db.query(Quotation).filter(
            Quotation.admin_id == request.admin_id,
            Quotation.employe_id == request.employee_id,
            Quotation.quotation_status == 1
        ).count()
    else:
        quotation_sent_count = db.query(Quotation).filter(
            Quotation.admin_id == request.admin_id,
            Quotation.quotation_status == 1
        ).count()
    
    employee_leads = employee_leads_query.all()
    employee_id_count = sum(
        1 for lead in employee_leads if request.employee_id in (lead.allocated_emplyee_id or "").split(',')
    )

    
    role_assignments = db.query(RoleAssignByLevel.employe_id_to).filter(
        RoleAssignByLevel.employe_id_from == request.employee_id
    ).all()

    
    all_assigned_employees = set(
        chain.from_iterable(role.employe_id_to or [] for role in role_assignments)
    )
    assigned_employee_count = len(all_assigned_employees)


    task = db.query(TaskRequest).filter(TaskRequest.admin_id == request.admin_id)
    if request.employee_id:
        task = task.filter(TaskRequest.emp_id_from == request.employee_id)  # add filter instead of new query

    task_count = task.count()

    attendance = db.query(Attendance).filter(Attendance.admin_id == request.admin_id)
    if request.employee_id:
        attendance = attendance.filter(Attendance.employee_id == request.employee_id)

    attendance_count = attendance.count()

    leave = db.query(EmployeeLeave).filter(EmployeeLeave.admin_id == request.admin_id)
    if request.employee_id:
        leave = leave.filter(EmployeeLeave.employee_id == request.employee_id)

    leave_count = leave.count()

    inventry = db.query(storeManagerProduct).filter(storeManagerProduct.admin_id == request.admin_id)
    if request.employee_id:
        inventry = inventry.filter(storeManagerProduct.emplpoyee_id == request.employee_id)

    inventry_count = inventry.count()

    # Response
    response = {
        'status': 'true',
        'message': "Data Received Successfully",
        'data': {
            'employee_id': request.employee_id,
            'lead_count': employee_id_count,
            'hot_leads_count': hot_leads_count,
            'won_leads_count': won_leads_count,
            'meeting_done_count': meeting_done_count,
            'quotation_sent_count': quotation_sent_count,
            'assigned_employee_count': assigned_employee_count,
            
            'inventry_count': inventry_count,
            'leave_count': leave_count,
            'task_count': task_count,
            'attendence_count': attendance_count
        }
    }

    return response






