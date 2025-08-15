from fastapi import APIRouter, Depends, HTTPException, Header
from sqlmodel import Session
from .models import TaskRequestCreate,TaskListRequest,DeleteTask,TaskRequestUpdate,TaskStatusUpdate,TaskRequestCreatelist
from .service import create_task,get_task_list,delete_task,update_task,update_task_status, create_multi_task , message_create_func
from src.database import get_db
from src.parameter import get_token
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.post("/createTask")
def create_task_route(
    task_create: TaskRequestCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    
    return create_task(db=db, task_create=task_create)

@router.post("/createmultipleTask")
def create_task_route(
    paylode: TaskRequestCreatelist,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    
    return create_multi_task(db=db, paylode=paylode)


@router.post("/getTaskList")
def get_task_list_route(
    task_list_request: TaskListRequest, 
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    
    tasks = get_task_list(
        db=db,
        admin_id=task_list_request.admin_id,
        emp_id_from=task_list_request.emp_id_from,
        emp_id_to=task_list_request.emp_id_to,
        from_date=task_list_request.from_date,
        to_date=task_list_request.to_date,
        task_priority=task_list_request.task_priority,
        task_status=task_list_request.task_status,
        customer_id=task_list_request.customer_id,
        project_id=task_list_request.project_id,
        task_id = task_list_request.task_id
        
    )

    if tasks:
        return {
            "status": "true",
            "message": "Tasks fetched successfully",
            "data": tasks
        }
    else:
        return {
            "status": "false",
            "message": "No tasks found",
            "data": []
        }


@router.post("/deleteTask")
def delete_task_route(
    task_list_request: DeleteTask,  
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
  
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    
    return delete_task(
        db=db,
        admin_id=task_list_request.admin_id,
        emp_id=task_list_request.emp_id,
        task_id=task_list_request.task_id 
    )


@router.post("/updateTask")
def update_task_route(
    task_data: TaskRequestUpdate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db),
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    
    return update_task(db=db, task_update=task_data)
    

@router.post("/update_task_status")
def update_task_status_route(
    task_data: TaskStatusUpdate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db),
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    return update_task_status(db=db, task_data=task_data)




from src.EmployeeTasksMessage.models import ChatMessageModelGet, ChatMessageModelCreate ,ChatMessageModel
from src.cre_upd_name import *

@router.post("/messages")
def create_message(
    message_create: ChatMessageModelCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    
    return message_create_func(db=db, message_create=message_create)

@router.post("/messages_get")
def get_message(
    message_get: ChatMessageModelGet,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    
    # Filter messages based on input
    query = db.query(ChatMessageModel).filter(ChatMessageModel.admin_id == message_get.admin_id)

    if message_get.employee_id:
        query = query.filter(ChatMessageModel.employee_id == message_get.employee_id)
    
    if message_get.task_id:
        query = query.filter(ChatMessageModel.task_id == message_get.task_id)
    
    messages = query.all()

    result = []

    for msg in messages:
        admin_emp_id = msg.employee_id if msg.employee_id else msg.admin_id
        created_by_type = "employee" if msg.employee_id else "admin"

        creator_info = get_creator_info(
            admin_emp_id=admin_emp_id,
            created_by_type=created_by_type,
            db=db
        )

        # Avoid exposing internal SQLAlchemy state
        msg_data = {
            key: value
            for key, value in msg.__dict__.items()
            if not key.startswith("_sa_")
        }
        msg_data["creator_info"] = creator_info

        result.append(msg_data)

    return {
        "status": "true",
        "message": "Messages retrieved successfully",
        "data": result
    }
    


from src.ProjectTasks.models import ProjectTask
from src.EmployeeTasks.models import TaskRequest , TaskRequestCount , EmpRequestCount, AttendenceRequestCount
from src.EmployeeTasksCustomer.models import EmployeeTasksCustomer
from datetime import datetime , date
from datetime import date, datetime, time

@router.post("/Task_overview")
def dashboard_overview(
    request: TaskRequestCount,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {
            'status': 'false',
            'message': "Unauthorized request",
        }

    # Base TaskRequest query
    task_query = db.query(TaskRequest).filter(TaskRequest.admin_id == request.admin_id)
    if request.employee_id:
        task_query = task_query.filter(TaskRequest.emp_id_from == request.employee_id)

    task_count = task_query.count()

    # Assigned: emp_id_to not null and not empty
    assigned_task_count = task_query.filter(
        TaskRequest.emp_id_to.isnot(None),
        TaskRequest.emp_id_to != ""
    ).count()

    # Overdue tasks: to_date_time is not null and < today
    today = datetime.today()
    overdue_task_count = task_query.filter(
        TaskRequest.to_date_time != None,
        TaskRequest.to_date_time < today
    ).count()

    new_task_count = task_query.filter(
        TaskRequest.created_at >= datetime.combine(today, datetime.min.time()),
        TaskRequest.created_at <= datetime.combine(today, datetime.max.time())
    ).count()

    
    today_start = datetime.combine(date.today(), time.min)
    
    task_list = task_query.filter(
        TaskRequest.to_date_time != None,
        TaskRequest.to_date_time >= today_start
    ).all()

    result = []
    for task in task_list:
        task = get_task_list(admin_id=task.admin_id , task_id=task.id , db=db)
        if task:
          result.append(task[0])

    # ProjectTask
    project_query = db.query(ProjectTask).filter(ProjectTask.admin_id == request.admin_id)
    if request.employee_id:
        project_query = project_query.filter(ProjectTask.emp_id == request.employee_id)
    project_task_count = project_query.count()

    # EmployeeTasksCustomer
    emp_task_query = db.query(EmployeeTasksCustomer).filter(EmployeeTasksCustomer.admin_id == request.admin_id)
    if request.employee_id:
        emp_task_query = emp_task_query.filter(EmployeeTasksCustomer.emp_id == request.employee_id)
    employee_task_count = emp_task_query.count()

    return {
        'status': 'true',
        'message': "Data Received Successfully",
        'data': {
            'task_request_count': task_count,
            'project_task_count': project_task_count,
            'employee_tasks_customer_count': employee_task_count,
            'report_count': 0,
            'new_task_count': new_task_count,
            'assigned_task_count': assigned_task_count,
            'overdue_task_count': overdue_task_count,
            'tasks': result if result else []
        }
    }


from src.AdminAddEmployee.models import AdminAddEmployee
from src.DailyTaskReport.models  import DailyReport

@router.post("/emdetailwithreports")
def emp_overview(
    request: EmpRequestCount,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    # Authentication check
    if auth_token != get_token():
        return {
            'status': 'false',
            'message': "Unauthorized request",
        }

    # Safely cast admin_id
    try:
        admin_id = int(request.admin_id)
    except (ValueError, TypeError):
        return {
            'status': 'false',
            'message': "Invalid admin ID",
        }

    # Fetch employees under this admin
    employees = db.query(AdminAddEmployee).filter(AdminAddEmployee.admin_id == admin_id).all()

    result = []
    for emp in employees:
        data = emp.__dict__.copy()

        # Count reports where employee_id matches (assume both are int)
        report_count = db.query(DailyReport).filter(DailyReport.employee_id == emp.id).count()
        data1 = {}

        data1['report_count'] = report_count
        data1["employee"] = data
        result.append(data1)

    return {
        'status': 'true',
        'message': 'Success',
        'data': result
    }





from src.Attendance.models import Attendance
from src.AdminSales.models import AdminSales
from sqlalchemy import not_, or_
from src.parameter import get_current_datetime
from sqlalchemy import and_
from datetime import datetime, timedelta
from sqlalchemy import func

@router.post("/Attendence_overview")
def attendence_overview(
    request: AttendenceRequestCount,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {'status': 'false', 'message': "Unauthorized request"}

    from_datetime = datetime.combine(request.from_date, time.min) if request.from_date else None
    to_datetime = datetime.combine(request.to_date, time.max) if request.to_date else None

    # ==============================
    # Task Query (for stats & report match)
    # ==============================
    task_query = db.query(TaskRequest).filter(TaskRequest.admin_id == request.admin_id)
    if request.employee_id:
        task_query = task_query.filter(TaskRequest.emp_id_to == request.employee_id)
    if from_datetime and to_datetime:
        task_query = task_query.filter(
            TaskRequest.created_at >= from_datetime,
            TaskRequest.created_at <= to_datetime
        )
    tasks = task_query.all()

    pending_task = task_query.filter(TaskRequest.task_status == "Pending").count()
    completed_task = task_query.filter(TaskRequest.task_status == "Completed").count()

    today_date = get_current_datetime().date()
    expired_tasks = task_query.filter(
        TaskRequest.to_date_time < datetime.combine(today_date, time.min),
        TaskRequest.task_status != "Completed"
    ).count()

    self_assigned_tasks = task_query.filter(
        TaskRequest.emp_id_from == TaskRequest.emp_id_to
    ).count()


    assigned_tasks = task_query.filter(
        TaskRequest.emp_id_to == request.employee_id,
        TaskRequest.emp_id_from != request.employee_id
    ).all()

    # Dictionary to count how many times each assigner assigned tasks
    # assigner_count = defaultdict(int)

    assigner_counter = {}

    for assigned in assigned_tasks:
        assigni_name = None

        if assigned.emp_id_from not in ["", None]:
            employee = db.query(AdminAddEmployee).filter(
                AdminAddEmployee.id == int(assigned.emp_id_from)
            ).first()
            if employee:
                assigni_name = f"{employee.employe_name}({employee.employee_id})"
        else:
            admin = db.query(SuperAdminUserAddNew).filter(
                SuperAdminUserAddNew.id == int(assigned.admin_id)
            ).first()
            if admin:
                assigni_name = f"{admin.full_name}(admin)"

        # if assigni_name:
        #     assigner_count[assigni_name] += 1

        if assigni_name:
            if assigni_name in assigner_counter:
                assigner_counter[assigni_name] += 1
            else:
                assigner_counter[assigni_name] = 1


    task_stats = {
        "total_tasks_count": len(tasks),
        "total_pending_count": pending_task,
        "total_expired_count": expired_tasks,
        "total_complited_count": completed_task,
        "total_self_count": self_assigned_tasks,
        "task_assigned_by": [{"name": name, "count": count} for name, count in assigner_counter.items()]
    }

    # ==============================
    # Attendance
    # ==============================
    attendance_query = db.query(Attendance).filter(Attendance.admin_id == request.admin_id)
    if request.employee_id:
        attendance_query = attendance_query.filter(Attendance.employee_id == request.employee_id)
    if from_datetime and to_datetime:
        attendance_query = attendance_query.filter(
            Attendance.created_at >= from_datetime,
            Attendance.created_at <= to_datetime
        )

    total_attendance = attendance_query.count()

    check_in = attendance_query.filter(Attendance.status == "sign-in").count()

    check_out = attendance_query.filter(Attendance.status == "sign-out").count()

    employee = db.query(AdminAddEmployee).filter(
        AdminAddEmployee.id == int(request.employee_id)
    ).first()

    if employee:
        created_date = employee.created_at.date()
        today_date = datetime.now().date()

    # Get unique sign-in dates
    sign_in_dates = attendance_query.filter(
        Attendance.status == "sign-in"
    ).with_entities(func.date(Attendance.created_at)).distinct().all()

    sign_in_day_set = {row[0] for row in sign_in_dates}

    # Total days since employee joined
    total_days = (today_date - created_date).days + 1

    # Calculate absents
    total_absent = total_days - len(sign_in_day_set)

    attendance = {
        "total_days_count": total_attendance,
        "total_on_time_count": 0,
        "total_latemark_count": 0,
        "total_absent_count": total_absent,
        "total_check_in_count": check_in,
        "total_check_out_count": check_out,
    }

    # ==============================
    # Leads (AdminSales)
    # ==============================
    lead_query = db.query(AdminSales).filter(AdminSales.admin_id == request.admin_id)
    if request.employee_id:
        lead_query = lead_query.filter(
            AdminSales.created_by_type == "employee",
            AdminSales.admin_emp_id == request.employee_id
        )
    if from_datetime and to_datetime:
        lead_query = lead_query.filter(
            AdminSales.created_at >= from_datetime,
            AdminSales.created_at <= to_datetime
        )

    total_leads = lead_query.count()
    won = lead_query.filter(AdminSales.status == "Won").count()
    hot = lead_query.filter(AdminSales.status == "Hot").count()
    cold = lead_query.filter(AdminSales.status == "Cold").count()
    warm = lead_query.filter(AdminSales.status == "Warm").count()
    open_leads = lead_query.filter(not_(AdminSales.status.in_(["Won", "", None]))).count()
    pending = lead_query.filter(
        or_(
            AdminSales.status == "",
            AdminSales.status == None
        )
    ).count()

    lead = {
        "total_lead_count": total_leads,
        "total_closed_count": won,
        "total_open_count": open_leads,
        "total_pending_count": pending,
        "total_hot_count": hot,
        "total_warm_count": warm,
        "total_cold_count": cold,
        "total_won_count": won,
    }

    # ==============================
    # Daily Reports
    # ==============================
    daily_report_query = db.query(DailyReport).filter(DailyReport.admin_id == request.admin_id)
    if request.employee_id:
        daily_report_query = daily_report_query.filter(DailyReport.employee_id == request.employee_id)
    if from_datetime and to_datetime:
        daily_report_query = daily_report_query.filter(
            DailyReport.created_at >= from_datetime,
            DailyReport.created_at <= to_datetime
        )

    daily_reports = daily_report_query.all()
    daily_report_count = len(daily_reports)

    with_task = sum(1 for report in daily_reports if report.task_id not in [None, "", "0"])
    without_task = sum(1 for report in daily_reports if report.task_id in [None, "", "0"])
    # without_task = daily_report_count - with_task

    reported_task_ids = set(str(report.task_id) for report in daily_reports if report.task_id not in [None, "", "0"])
    not_submitted = sum(1 for task in tasks if str(task.id) not in reported_task_ids)

    daily_report = {
        "total_daily_count": daily_report_count,
        "total_with_task_count": with_task,
        "total_without_task_count": without_task,
        "total_not_submited_count": not_submitted,
    }

    return {
        'status': 'true',
        'message': "Data Received Successfully",
        'data': {
            'attendence': attendance,
            'lead': lead,
            'dailyReport': daily_report,
            'task': task_stats,
        }
    }


