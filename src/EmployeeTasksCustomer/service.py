from sqlmodel import select, Session
from datetime import datetime
from .models import CustomerCreate,EmployeeTasksCustomer ,CustomerGet , Customerupdate , CustomerDelete
from fastapi import HTTPException
from src.EmployeeTasks.models import TaskRequest

from src.ProjectTasks.models import ProjectTask

def create_task_customer(db: Session, task_create: CustomerCreate):
    
    task_data = task_create.dict()
    new_task = EmployeeTasksCustomer(**task_data)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "status": "true",
        "message": "Customer created successfully",
        "data": new_task
    }

def get_task_customer(db: Session, customer_get: CustomerGet):
    query = db.query(EmployeeTasksCustomer).filter(
        EmployeeTasksCustomer.admin_id == customer_get.admin_id
    )

    if not customer_get.emp_id:
        query = query.filter(EmployeeTasksCustomer.emp_id == "")

    if customer_get.emp_id:
        query = query.filter(EmployeeTasksCustomer.emp_id == customer_get.emp_id)

    if customer_get.customer_id:
        query = query.filter(EmployeeTasksCustomer.id == int(customer_get.customer_id))


    data = query.all()
    all_data = []
    
    for cust in data:
        pro_dict = cust.__dict__.copy()
    
        project_list = db.query(ProjectTask).filter(
            ProjectTask.customer_id == int(cust.id)
        ).all()
    
        pro_dict["projects"] = [
            {"id": proj.id, "project_name": proj.project_name}
            for proj in project_list
        ]
    
        pro_dict.pop("_sa_instance_state", None)
        all_data.append(pro_dict)
    
    return {
        "status": "true",
        "message": "Customer fetched successfully",
        "data": all_data
    }



def update_task_customer(db: Session, customer_update: Customerupdate):
    query = db.query(EmployeeTasksCustomer).filter(
        EmployeeTasksCustomer.admin_id == customer_update.admin_id,
        EmployeeTasksCustomer.id == int(customer_update.customer_id)
    )

    if customer_update.emp_id:
        query = query.filter(EmployeeTasksCustomer.emp_id == customer_update.emp_id)

    customer = query.first()  # Get the actual model instance

    if not customer:
        return {
            "status": "false",
            "message": "Customer not found",
        }

    data = customer_update.dict(exclude={"customer_id"})  # Remove ID from update
    for key, value in data.items():
        setattr(customer, key, value)

    db.commit()
    db.refresh(customer)

    return {
        "status": "true",
        "message": "Customer updated successfully",
        "data": data
    }


def delete_task_customer(db: Session, customer_delete: CustomerDelete):
    query = db.query(EmployeeTasksCustomer).filter(
        EmployeeTasksCustomer.admin_id == customer_delete.admin_id,
        EmployeeTasksCustomer.id == int(customer_delete.customer_id)
    )

    if customer_delete.emp_id:
        query = query.filter(EmployeeTasksCustomer.emp_id == customer_delete.emp_id)

    customer = query.first()  # Get the actual instance

    if not customer:
        return {
            "status": "false",
            "message": "Customer not found",
        }

    # Check if the customer has any tasks associated with it
    task_query = db.query(TaskRequest).filter(
        TaskRequest.customer_id == customer.id
    )

    if not task_query.first():
        db.delete(customer)  
        db.commit()

        return {
            "status": "true",
            "message": "Customer deleted successfully",
        }

    return {
        "status": "false",
        "message": "Customer cannot be deleted as it has associated tasks",
    }
