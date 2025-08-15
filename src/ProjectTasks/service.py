from sqlmodel import select, Session
from datetime import datetime
from .models import ProjectCreate,ProjectTask ,ProjectGet , ProjectUpdate , ProjectDelete
from fastapi import HTTPException
from src.EmployeeTasks.models import TaskRequest
from src.EmployeeTasksCustomer.models import EmployeeTasksCustomer

def create_task_customer(db: Session, project_create: ProjectCreate):

    task_data = project_create.dict()
    new_task = ProjectTask(**task_data)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "status": "true",
        "message": "Customer created successfully",
        "data": new_task
    }

def get_task_customer(db: Session, project_get: ProjectGet):
    query = db.query(ProjectTask).filter(
        ProjectTask.admin_id == project_get.admin_id
    )

    if not project_get.emp_id:
        query = query.filter(ProjectTask.emp_id == "")

    if project_get.emp_id:
        query = query.filter(ProjectTask.emp_id == project_get.emp_id)

    if project_get.customer_id:
        query = query.filter(ProjectTask.customer_id == int(project_get.customer_id))

    data = query.all()
    all_data = []

    for pro in data:
        pro_dict = pro.__dict__

        cust = db.query(EmployeeTasksCustomer).filter(
            EmployeeTasksCustomer.id == int(pro.customer_id)
        ).first()

        if cust:
            pro_dict["customer"] = {
                "customer_name": cust.customer_name,
                "site_name": cust.site_name
            }

        pro_dict.pop("_sa_instance_state", None)

        all_data.append(pro_dict)

    return {
        "status": "true",
        "message": "Project fetched successfully",
        "data": all_data
    }



def update_task_customer(db: Session, project_update: ProjectUpdate):
    query = db.query(ProjectTask).filter(
        ProjectTask.id == int(project_update.project_id)
    )

    project = query.first()  # Get the actual model instance

    if not project:
        return {
            "status": "false",
            "message": "Project not found",
        }

    data = project_update.dict(exclude={"project_id"})  # Remove ID from update
    for key, value in data.items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)

    return {
        "status": "true",
        "message": "Project updated successfully",
        "data": data
    }


from src.EmployeeTasks.models import TaskRequest

def delete_task_customer(db: Session, project_delete: ProjectDelete):
    query = db.query(ProjectTask).filter(
        ProjectTask.id == int(project_delete.project_id)
    )

    project = query.first()  # Get the actual instance

    if project:
        # Check if the project is in use
        exist = db.query(TaskRequest).filter(TaskRequest.project_id == project.id).first()
        if exist:
            return {
                "status": "false",
                "message": "Project is currently in use and cannot be deleted",
            }

        # Safe to delete
        db.delete(project)
        db.commit()
        return {
            "status": "true",
            "message": "Project deleted successfully",
        }

    return {
        "status": "false",
        "message": "Project not found",
    }
