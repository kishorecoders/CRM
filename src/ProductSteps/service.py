from .models import ProductSteps,ProductStepsCreate,ProductStepsRead , UpdateStepRequest
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status,HTTPException
from src.SubCategory.models import SubCategory
from sqlalchemy import func,cast, Integer
from src.StepItems.models import StepItems


def create(db: Session, productstep: ProductStepsCreate):
    admin_id = productstep.admin_id
    name = productstep.step_name
    position = productstep.position

    
    if not admin_id or admin_id.strip() == "":
        return {'status': 'false', 'message': 'Admin ID is required.'}

    
    if not name or name.strip() == "":
        return {'status': 'false', 'message': 'Step Name is required.'}

    # if position is None:
    #     return {'status': 'false', 'message': 'Position is required.'}

    
    #positions_in_use = db.query(ProductSteps.position).filter(ProductSteps.admin_id == admin_id).order_by(ProductSteps.position).all()
    #used_positions = [p[0] for p in positions_in_use]

   
   # missing_positions = [i for i in range(1, position) if i not in used_positions]

   # if missing_positions:
    #    return {'status': 'false', 'message': f'Positions {", ".join(map(str, missing_positions))} are missing. Please create them first before creating# position {position}.'}

    

    
    existing_step_name = db.query(ProductSteps).filter(
        ProductSteps.admin_id == admin_id, ProductSteps.step_name == name
    ).first()
    if existing_step_name:
        return {'status': 'false', 'message': 'This step name is already available.'}

    if productstep.employe_id:
        created_by_type = "employee"
        admin_emp_id = productstep.employe_id
    else:
        created_by_type = "admin"
        admin_emp_id = productstep.admin_id
    data = productstep.dict()
    data["created_by_type"] = created_by_type
    data["admin_emp_id"] = admin_emp_id
    
    db_step = ProductSteps(**data)
    db.add(db_step)
    db.commit()
    db.refresh(db_step)

    
    response = {
        'status': 'true',
        'message': "Step Created.",
        'data': db_step
    }
    return response





def update_step(db: Session, step_data: UpdateStepRequest):
    
    #step = db.query(ProductSteps).filter(ProductSteps.id == step_id).first()
    step = db.query(ProductSteps).filter(ProductSteps.id == step_data.step_id).first()

    if not step:
        return {
        "status": "false",
        "message": f"Step with id {step_id} does not exist.",
        
    }
     

    # Check if step_name is changed
    step_name_changed = step.step_name != step_data.step_name

    if step_name_changed:
        # Check if step is already used
        already_used = db.query(StepItems).filter(StepItems.step_id == step_data.step_id).first()
        if already_used:
            return {
                "status": "false",
                "message": "Step is already used in StepItems and cannot be updated."
            }
        # Update name and file_path
        step.step_name = step_data.step_name
        if step_data.file_path:
            step.file_path = step_data.file_path
    else:
        # Name is same; update file_path only if provided
        if step_data.file_path:
            step.file_path = step_data.file_path  
    
    updated_by_type = None 
    updated_admin_emp_id = None
    

    if step_data.employe_id:
        updated_by_type = "employee"
        updated_admin_emp_id = step_data.employe_id
    else:
        updated_by_type = "admin"
        updated_admin_emp_id = step_data.admin_id
    
    if step_data.admin_id:
        step.admin_id = step_data.admin_id
    if step_data.employe_id:
        step.employe_id = step_data.employe_id
    if step_data.step_name:
        step.step_name = step_data.step_name
    if step_data.position:
        step.position = step_data.position
        
    if step_data.type:
        step.type = step_data.type
        
        
    step.updated_at = datetime.utcnow()
    step.updated_by_type = updated_by_type
    step.updated_admin_emp_id = updated_admin_emp_id
    
    db.add(step)
    db.commit()
    db.refresh(step)

    if step.type == "File":
        items = db.query(StepItems).filter(StepItems.step_id == step_data.step_id).all()
        for item in items:
            db.delete(item)
        db.commit()


    
    response = {
        "status": "true",
        "message": "Step updated successfully.",
        "data": ProductStepsRead.from_orm(step)
    }
    return response




def delete_step(db: Session, admin_id: str, step_id: int):
    
    step = db.query(ProductSteps).filter(
        ProductSteps.id == step_id,
        ProductSteps.admin_id == admin_id
    ).first()

    if not step:
        return {
            "status": "false",
            "message": f"Step with id {step_id} does not exist."
        }

    
    db.query(StepItems).filter(
        StepItems.step_id == step_id,
        StepItems.admin_id == admin_id
    ).delete()

   
    db.delete(step)
    db.commit()

    return {
        "status": "true",
        "message": f"Step with id {step_id} and related items deleted successfully."
    }



def delete_step_file(db: Session, step_id: int):
    
    step = db.query(ProductSteps).filter(
        ProductSteps.id == step_id,
    ).first()

    if not step:
        return {
            "status": "false",
            "message": f"Step with id {step_id} does not exist."
        }
    step.type = "product"
    step.file_path = None
    db.commit()

    return {
        "status": "true",
        "message": f"File Removed successfully."
    }



