from sqlmodel import select, Session
from datetime import datetime
from .models import TaskRequest, TaskRequestCreate,TaskRequestUpdate,TaskStatusUpdate, TaskRequestCreatelist 
from pytz import UTC
from typing import List
from typing import Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from src.parameter import get_current_datetime
from src.AdminAddEmployee.models import AdminAddEmployee
from apscheduler.schedulers.background import BackgroundScheduler
from src.database import get_db
import json
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew
from sqlalchemy import and_, or_
from sqlalchemy.dialects import mysql
from datetime import timezone
from src.cre_upd_name import get_creator_info , get_creator_updator_info
from src.EmployeeTasksCustomer.models import EmployeeTasksCustomer
from src.TasksStatusHistory.models import TaskStatusHistory
from src.Meetingplanned.service import update_expired_meetings
from src.EmployeeLeave.service import update_expired_EmployeeLeave
from datetime import datetime, timedelta
from src.TasksStatusHistory.models import TaskStatusHistory
from src.Account.service import save_base64_file
from src.ProjectTasks.models import ProjectTask
from src.Notifications.models import Notification


def create_task(db: Session, task_create: TaskRequestCreate):
    task_create_from_aware = task_create.from_date_time.replace(tzinfo=UTC)
    task_create_to_aware = task_create.to_date_time.replace(tzinfo=UTC)

    # Define valid creator types
    valid_creators = ["AdminSelf", "EmployeeSelf", "Admin", "Employee"]

    print("gggggg",TaskRequest.from_date_time)
    print("hhhhh",task_create_to_aware)
    print("jkkkkk",TaskRequest.to_date_time)
    print("mmmmmm",task_create_from_aware)


    # Only check if the create_by is in our role list
    if task_create.create_by in valid_creators:
        query = select(TaskRequest).where(
            TaskRequest.admin_id == task_create.admin_id,
            TaskRequest.emp_id_to == task_create.emp_id_to,
            TaskRequest.create_by == task_create.create_by,
            or_(
                and_(
                    TaskRequest.from_date_time <= task_create_to_aware,
                    TaskRequest.to_date_time >= task_create_from_aware
                )
            )
        )




        print("gggggg",query)
        print("hhhhh",task_create_to_aware)
        print("jkkkkk",TaskRequest.to_date_time)
        print("mmmmmm",task_create_from_aware)

        overlapping_task = db.execute(query).scalars().first()

        if overlapping_task:
            return {
                "status": "false",
                "message": (
                    f"A task already exists for this employee with the same creator "
                    f"type ({task_create.create_by}) during this time range "
                    f"({task_create.from_date_time} to {task_create.to_date_time})."
                )
            }

    # No conflict, continue task creation
    task_data = task_create.dict()
    task_data["task_file_image"] = json.dumps(task_data["task_file_image"])
    new_task = TaskRequest(**task_data)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "status": "true",
        "message": "Task created successfully",
        "data": new_task
    }


def create_multi_task(db: Session, paylode: TaskRequestCreatelist):
    result = []
    for task_create in paylode.tasks:

        task_data = task_create.dict()
        task_data["task_file_image"] = json.dumps(task_data.get("task_file_image", []))
        task_data["customer_id"] = paylode.customer_id
        task_data["admin_id"] = paylode.admin_id
        task_data["emp_id_from"] = paylode.emp_id_from
        task_data["emp_id_to"] = paylode.emp_id_to
        task_data["task_status"] = "Pending"
        new_task = TaskRequest(**task_data)

        db.add(new_task)
        db.flush() 
        result.append(new_task)

        if paylode.emp_id_from:
            admin_emp_id = paylode.emp_id_from
            created_by_type = "employee"
        else:
            admin_emp_id = paylode.admin_id
            created_by_type = "admin"

        status_history = TaskStatusHistory(
            task_id= new_task.id,
            admin_id= paylode.admin_id,
            emp_id_from= paylode.emp_id_from,
            task_status= "Created" if task_create.task_status == "Pending" else task_create.task_status,
            created_by_type= created_by_type,
            admin_emp_id= admin_emp_id
        )
        db.add(status_history)

    db.commit()  # ? One commit after loop
    for obj in result:
        db.refresh(obj)

    return {
        "status": "true",
        "message": "task(s) created successfully",
        "data":result
    }



def get_task_list(
    db: Session,
    admin_id: int,
    emp_id_from: Optional[str] = None,
    emp_id_to: Optional[str] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    task_priority: Optional[str] = None,
    task_status: Optional[str] = None,
    customer_id: Optional[str] = None,
    project_id: Optional[str] = None,
    task_id: Optional[str] = None 
) -> List[Dict]:


    query = select(TaskRequest).where(TaskRequest.admin_id == admin_id).order_by(TaskRequest.id.desc())

    if emp_id_from:
        query = query.where(TaskRequest.emp_id_from == emp_id_from)
    if emp_id_to:
        query = query.where(TaskRequest.emp_id_to == emp_id_to)
    if from_date:
        query = query.where(TaskRequest.created_at >= from_date)
    if to_date:
        query = query.where(TaskRequest.created_at <= to_date)
    if task_priority:
        query = query.where(TaskRequest.task_priority == task_priority)
    if task_status:
        query = query.where(TaskRequest.task_status == task_status)
    if customer_id:
        query = query.where(TaskRequest.customer_id == customer_id)
    if project_id:
        query = query.where(TaskRequest.project_id == project_id)
        
    if task_id:
        query = query.where(TaskRequest.id == int(task_id))
        
    tasks = db.execute(query).scalars().all()

    # Fetch employees and super admins
    employees = db.execute(select(AdminAddEmployee)).scalars().all()
    super_admins = db.execute(select(SuperAdminUserAddNew)).scalars().all()

    # Create lookup maps
    employee_map = {str(emp.id): (emp.employe_name or "Unknown", emp.employee_id or "") for emp in employees}
    super_admin_map = {str(admin.id): admin.full_name for admin in super_admins}

    result = []
    for task in tasks:
        if task.create_by == "AdminSelf":
            # Created by admin, assigned to self
            admin_full_name = super_admin_map.get(str(task.admin_id), "Admin") + " (Admin)"
            emp_name_from = admin_full_name
            emp_name_to = admin_full_name

        elif task.create_by == "AdminCustomerSelf":
            # Created by AdminCustomerSelf, assigned to self
            admin_full_name = super_admin_map.get(str(task.admin_id), "Admin") + " (Admin)"
            emp_name_from = admin_full_name
            emp_name_to = admin_full_name

        elif task.create_by == "AdminCustomerEmployee":
            # Created by AdminCustomerEmployee, assigned to employee
            emp_name_from = super_admin_map.get(str(task.admin_id), "Admin") + " (Admin)"
            name_to, emp_id_to_val = employee_map.get(str(task.emp_id_to), ("Unknown", ""))
            emp_name_to = f"{name_to} ({emp_id_to_val})" if emp_id_to_val else name_to

        elif task.create_by == "Admin":
            # Created by admin, assigned to employee
            emp_name_from = super_admin_map.get(str(task.admin_id), "Admin") + " (Admin)"
            name_to, emp_id_to_val = employee_map.get(str(task.emp_id_to), ("Unknown", ""))
            emp_name_to = f"{name_to} ({emp_id_to_val})" if emp_id_to_val else name_to

        else:
            # Created by employee, assigned to another employee
            name_from, emp_id_from_val = employee_map.get(str(task.emp_id_from), ("Unknown", ""))
            name_to, emp_id_to_val = employee_map.get(str(task.emp_id_to), ("Unknown", ""))
            emp_name_from = f"{name_from} ({emp_id_from_val})" if emp_id_from_val else name_from
            emp_name_to = f"{name_to} ({emp_id_to_val})" if emp_id_to_val else name_to

        admin_emp_cus_info_data={}

        customer_info=None
        customer_data=db.query(EmployeeTasksCustomer).filter(EmployeeTasksCustomer.id==int(task.customer_id)).first()
        if customer_data:
            customer_info={
                "customer_id":customer_data.id,
                "customer_name":customer_data.customer_name,
                "site_name":customer_data.site_name
            }

        project = None
        if task.project_id:
            project = db.query(ProjectTask).filter(ProjectTask.id == int(task.project_id)).first()



        history_records = db.query(TaskStatusHistory).filter(
            TaskStatusHistory.task_id == task.id
        ).all()
        
        history_result = []
        
        for hist in history_records:
            hi = hist.__dict__.copy()
            hi.pop('_sa_instance_state', None)  # remove SQLAlchemy internal key if present
        
            created__data_order = get_creator_info(hist.admin_emp_id, hist.created_by_type, db)
            created__data_order['created_at'] = hist.created_at
            hi['created_by_data'] = created__data_order
        
            history_result.append(hi)



        employee_info_to=None
        if task.create_by =="AdminCustomerEmployee" or task.create_by =="Admin" or task.create_by =="EmployeeCustomerEmployee" or task.create_by =="AdminNotAssign" or task.create_by =="EmployeeNotAssign" or task.create_by =="Employee":
            employee_info_to=get_creator_info(admin_emp_id=task.emp_id_to,created_by_type="employee",db=db)
        
        employee_info_from = None

        if task.create_by =="EmployeeCustomer" or task.create_by =="EmployeeCustomerSelf"or task.create_by =="EmployeeCustomerEmployee"or task.create_by =="EmployeeSelf"or task.create_by =="Employee":
            employee_info_from=get_creator_info(admin_emp_id=task.emp_id_from,created_by_type="employee",db=db)
        
        admin_info=get_creator_info(admin_emp_id=task.admin_id,created_by_type="admin",db=db)
        admin_emp_cus_info_data={
        "admin_info":admin_info,
        "employee_info_from":employee_info_from,
        "employee_info_to":employee_info_to,
        "customer_info":customer_info
        } 

        created_updated_data = get_creator_updator_info(
            admin_emp_id=task.admin_emp_id,
            created_by_type=task.created_by_type,
            updated_admin_emp_id=task.updated_admin_emp_id,
            updated_by_type=task.updated_by_type,
          db=db
        )


        task_data={
            "id": task.id,
            "admin_id": task.admin_id,
            "emp_id_from": task.emp_id_from,
            "emp_name_from": emp_name_from,
            "emp_id_to": task.emp_id_to,
            "emp_name_to": emp_name_to,
            "customer_id":task.customer_id,
            "project_id": task.project_id,
            "task_title": task.task_title,
            "task_details": task.task_details,
            "task_file_image": json.loads(task.task_file_image) if task.task_file_image else [],
            "task_priority": task.task_priority,
            "task_status": task.task_status,
            "from_date_time": task.from_date_time,
            "to_date_time": task.to_date_time,
            "created_by_type": task.created_by_type,
            "admin_emp_id": task.admin_emp_id,
            "updated_by_type": task.updated_by_type,
            "updated_admin_emp_id": task.updated_admin_emp_id,
            "task_type_status": task.task_type_status,
            "complete_file_path": task.complete_file_path,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
            "created_by": task.create_by,
            "task_routine": task.task_routine,
            "project": project if project else None,
            "status_updator_info":history_result
        }

        result.append({**task_data,**admin_emp_cus_info_data ,**created_updated_data})


    return result
    

def delete_task(
    db: Session,
    admin_id: int,
    emp_id: str,
    task_id: int
):
    


    task = db.execute(select(TaskRequest).where(
        TaskRequest.id == task_id,
        TaskRequest.admin_id == admin_id,
        TaskRequest.emp_id_from == emp_id,
       
    )).scalars().first()


   
    if not task:
        return {"status": "false", "message": "Task not found to delete"}

    
    db.delete(task)
    db.commit()

    # Delete associated task status history
    db.execute(
        TaskStatusHistory.__table__.delete().where(
            TaskStatusHistory.task_id == task_id
        )
    )
    db.commit()
    # Delete associated task file images if any


    return {"status": "true", "message": "Task deleted successfully"}


def update_task(db: Session, task_update: TaskRequestUpdate):
    task = db.get(TaskRequest, task_update.task_id)
    if not task:
        return {
            "status": "false",
            "message": "Task not found",
        }


    update_data = task_update.dict(exclude_unset=True, exclude={"task_id"})
    
    if (task.created_by_type == "admin" and task_update.from_date_time is None and 
        task_update.to_date_time is None and task_update.emp_id_to != task.admin_id) and(
            task.create_by == "AdminSelf" or task.create_by == "AdminCustomerSelf"
        ) :
            return {
            "status": "false",
            "message": "From date and too date is reqired ."
        }

    if (task.created_by_type == "employee" and task_update.from_date_time is None and 
        task_update.to_date_time is None and task_update.emp_id_to != task.emp_id_from) and(
            task.create_by == "EmployeeSelf" or task.create_by == "EmployeeCustomerSelf"
        ) :
            return {
            "status": "false",
            "message": "From date and too date is reqired ."
        }

    # Prevent clearing of already-set from_date_time
    if task.from_date_time is not None and task_update.from_date_time is None:
        return {
            "status": "false",
            "message": "from_date_time is already set and cannot be cleared."
        }
    
    # Prevent clearing of already-set to_date_time
    if task.to_date_time is not None and task_update.to_date_time is None:
        return {
            "status": "false",
            "message": "to_date_time is already set and cannot be cleared."
        }


    if "task_status" in update_data and update_data["task_status"] == "":
        update_data["task_status"] = task.task_status

    # Proceed to update the task if no overlap is found
    for key, value in update_data.items():
        if key == "task_status" and value == "":
            continue  # Skip updating task_status if empty string
        if key == "task_file_image" and value is not None:
            setattr(task, key, json.dumps(value))
        else:
            setattr(task, key, value)

    task.updated_at = get_current_datetime()
    
        
    db.add(task)
    db.commit()
    db.refresh(task)

    task_file_image = []
    if task.task_file_image:
        try:
            task_file_image = json.loads(task.task_file_image)
        except json.JSONDecodeError:
            task_file_image = []

    response_data = {
        "id": task.id,
        "admin_id": task.admin_id,
        "emp_id_from": task.emp_id_from,
        "emp_id_to": task.emp_id_to,
        "task_title": task.task_title,
        "task_details": task.task_details,
        "task_file_image": task_file_image,
        "task_priority": task.task_priority,
        "task_status": task.task_status,
        "from_date_time": task.from_date_time,
        "to_date_time": task.to_date_time,
        "task_routine": task.task_routine,
        "task_type_status": task.task_type_status,
        "created_at": task.created_at,
        "updated_at": task.updated_at,
        "create_by": task.create_by,
    }

    return {
        "status": "true",
        "message": "Task updated successfully",
        "data": response_data,
    }


def update_task_status(db: Session, task_data: TaskStatusUpdate):
    task = db.get(TaskRequest, task_data.task_id)
    if not task:
        return {
        "status": "false",
        "message": "Task not found"
        
    }
       

    if task.admin_id != task_data.admin_id:
        return {
        "status": "false",
        "message": "Task not found"
       
    }

    if task_data.to_date_time:
        task.to_date_time = task_data.to_date_time

    if task_data.emp_id_to:
        task.emp_id_to = task_data.emp_id_to
    if task_data.customer_id:
        task.customer_id = task_data.customer_id
        

    if task_data.task_status:
        task.task_status = "Pending" if task_data.task_status == "Re Assign" else task_data.task_status
        task.complete_file_path = None if task_data.task_status == "Re Assign" else task.complete_file_path

    if task_data.task_remark:
        task.task_remark = task_data.task_remark
      
    if task_data.create_by:
        task.create_by = task_data.create_by

    complete_file_path = None

    if task_data.complete_file_path:
        current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
        # file_extension = "pdf" if task_data.file_type == "pdf" else "jpg"
        file_extension = task_data.file_type
        filename = f"{current_datetime}_task_{task_data.admin_id}.{file_extension}"
        complete_file_path = save_base64_file(task_data.complete_file_path, filename)
    else:
        complete_file_path = "" 

    if task_data.complete_file_path:
        task.complete_file_path = complete_file_path  
        

    task.updated_at = get_current_datetime()
    if task_data.project_id != None and task_data.project_id != "":
        task.project_id = task_data.project_id
        
        
    db.add(task)
    db.commit()
    db.refresh(task)

    if task_data.emp_id_from:
        admin_emp_id = task_data.emp_id_from
        created_by_type = "employee"
    else:
        admin_emp_id = task_data.admin_id
        created_by_type = "admin"   
    
    if task_data.task_status:
        status_history = TaskStatusHistory(
            task_id= task.id,
            admin_id= task_data.admin_id,
            emp_id_from= task_data.emp_id_from,
            task_status= "Re Assign" if task_data.task_status == "Re Assign" else task_data.task_status,
            task_history_remark= task_data.task_remark,
            created_by_type= created_by_type,
            admin_emp_id= admin_emp_id
        )
        db.add(status_history)
        db.commit() 
        db.refresh(status_history)  


    # ? Create notification based on task status
    if task.task_status in ["Completed", "In-Progress"]:
        emp_name = None
        if task.emp_id_from:
            employee = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == int(task.emp_id_from)).first()
            if employee:
                emp_name = f"{employee.employe_name} ({employee.employee_id})"

        if task.task_status == "Completed":
            notif_title = "Task Completed"
            notif_description = f"Task '{task.task_title}' has been completed by {emp_name}."
            notif_type = "task_completed"

        elif task.task_status == "In-Progress":
            notif_title = "Task In Progress"
            notif_description = f"{emp_name} has started working on task '{task.task_title}'."
            notif_type = "task_in_progress"

        notification = Notification(
            admin_id=task.admin_id,
            title=notif_title,
            description=notif_description,
            type=notif_type,
            object_id=str(task.id),
            created_by_id=admin_emp_id,
            created_by_type=created_by_type,
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)


    return {
        "status": "true",
        "message": "Task status updated successfully",
        "data": task,
    }
    



# def update_expired_tasks(db: Session):

#     current_time = get_current_datetime()
#     print("current_time",current_time)

    
#     expired_tasks = db.query(TaskRequest).filter(
#         (TaskRequest.to_date_time).date()  <= (current_time + timedelta(days=1)).date(),
#         TaskRequest.task_status != "Completed"
#     ).all()

#     for task in expired_tasks:
#         task.task_status = "Expired"
#         task.updated_at = current_time
#         db.add(task)

#     db.commit()


def update_expired_tasks(db: Session):
    current_time = get_current_datetime()
    today_date = current_time.date()

    print("current_time:", current_time)
    print("today_date:", today_date)

    expired_tasks = db.query(TaskRequest).filter(
        TaskRequest.to_date_time < datetime.combine(today_date, datetime.min.time()),
        TaskRequest.task_status != "Completed"
    ).all()

    for task in expired_tasks:
        task.task_status = "Expired"
        task.updated_at = current_time
        db.add(task)

    db.commit()



def start_scheduler():
    
    scheduler = BackgroundScheduler()
    # scheduler.add_job(
    #     func=lambda: update_expired_tasks(next(get_db())),  
    #     trigger="interval",  
    #     seconds=60, 
    # )
    scheduler.add_job(
        func=lambda: update_expired_meetings(next(get_db())),
        trigger="interval",
        seconds=60,
    )
    scheduler.add_job(
        func=lambda: update_expired_EmployeeLeave(next(get_db())),
        trigger="interval",
        seconds=60,
    )

    scheduler.start()
    

from src.EmployeeTasksMessage.models import ChatMessageModel, ChatMessageModelCreate

def message_create_func(db: Session, message_create: ChatMessageModelCreate):


    message_data = message_create.dict()
    new_message = ChatMessageModel(**message_data)

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return {
        "status": "true",
        "message": "message created successfully",
    }




    
