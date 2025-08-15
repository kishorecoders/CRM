from src.parameter import get_current_datetime
from .models import StepItemsCreate,StepItems,StepItemDeleteRequest
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status,HTTPException
from src.ProductSteps.models import ProductSteps


def create(db: Session, step_item: StepItemsCreate):
    admin_id = step_item.admin_id
    name = step_item.item_name
    step_id = step_item.step_id

    
    if not admin_id or admin_id.strip() == "":
        return {'status': 'false', 'message': 'Admin ID is required.'}

    
    main_step = db.query(ProductSteps).filter(ProductSteps.id == step_id).first()
    if not main_step:
        return {'status': 'false', 'message': f'Step with ID {step_id} does not exist.'}

    
    step_name = main_step.step_name
    if step_name == name:
        return {
            'status': 'false',
            'message': f'The step item name "{name}" already exists under the Step "{step_name}". '
                       'Please choose a different step item name.'
        }

    if step_item.employe_id:
        created_by_type = "employee"
        admin_emp_id = step_item.employe_id
    else:
        created_by_type = "admin"
        admin_emp_id = step_item.admin_id  
    
    data = step_item.dict()
    data["created_by_type"]= created_by_type
    data["admin_emp_id"]= admin_emp_id

    db_step_item = StepItems(**data)
    db.add(db_step_item)
    db.commit()
    db.refresh(db_step_item)

   
    response = {
        'status': 'true',
        'message': "Step item Details Added Successfully",
        'data': db_step_item
    }
    return response
    
    
    
    

def create_multiple(db: Session, step_items: List[StepItemsCreate]) -> dict:
   
    for step_item in step_items:
        step_id = step_item.step_id

       
        main_step = db.query(ProductSteps).filter(ProductSteps.id == step_id).first()
        if not main_step:
            return {
                "status": "false",
                "message": f"Step with ID {step_id} does not exist. No records were added."
            }
        main_step.type = "Product"
        main_step.file_path = None
        db.add(main_step)
        db.commit()

    skip = []
    added = []
    for step_item in step_items:
    
        if step_item.employe_id:
            created_by_type = "employee"
            admin_emp_id = step_item.employe_id
        else:
            created_by_type = "admin"
            admin_emp_id = step_item.admin_id  
        
        existing_item = db.query(StepItems).filter(StepItems.product_id == step_item.product_id,
                                                    StepItems.step_id == step_item.step_id).first()
        if existing_item:
            skip.append(step_item)
            continue

        data = step_item.dict()
        data["created_by_type"] = created_by_type
        data["admin_emp_id"] = admin_emp_id

        db_step_item = StepItems(**data)
        db.add(db_step_item)
        added.append(db_step_item)

    db.commit()

    
    return {
        "status": "true",
        "message": f"{len(added)} step item(s) added successfully. {len(skip)} step item(s) skipped due to existing records."
    }




from src.StoreManagerProduct.models import storeManagerProduct

def get_items_by_filter(
    db: Session,
    admin_id: str,
    step_id: Optional[int] = None,
    employee_id: Optional[str] = None,
    product_ids: Optional[list[int]] = None,
    stage_id: Optional[str] = None
):
    if not admin_id or admin_id.strip() == "":
        return {'status': 'false', 'message': 'Admin ID is required.'}

    base_query = db.query(StepItems).filter(StepItems.admin_id == admin_id)

    if step_id and step_id != 0:
        base_query = base_query.filter(StepItems.step_id == step_id)

    if employee_id and employee_id.strip() != "":
        base_query = base_query.filter(StepItems.employe_id == employee_id)

    results = []
    

    # Ensure both stage_id and product_ids are given
    if not stage_id or not product_ids:
        return {
            'status': 'true',
            'message': 'Stage ID and product IDs are required to fetch step items.',
            'data': []
        }



    if stage_id and product_ids:
        for pid in product_ids:
            query = base_query.filter(StepItems.product_id == str(pid), StepItems.stage_id == stage_id)
            items = query.all()
            for item in items:
                data = item.dict()
                product_detail = db.query(storeManagerProduct).filter(storeManagerProduct.id == item.product_id).first()
                if product_detail:
                    data['item_name'] = product_detail.product_tital
                    data['aval_quantity'] = product_detail.opening_stock
                    data['discription'] = product_detail.item_code
                    results.extend([data])
    else:
        items = base_query.all()
        for item in items:
            data = item.dict()
            product_detail = db.query(storeManagerProduct).filter(storeManagerProduct.id == item.product_id).first()
            if product_detail:
                data['item_name'] = product_detail.product_tital
                data['aval_quantity'] = product_detail.opening_stock
                data['discription'] = product_detail.item_code
                results.extend([data])

    if not results:
        return {
            'status': 'false',
            'message': 'No step items found matching the given criteria.'
        }

    return {
        'status': 'true',
        'message': 'Step items fetched successfully.',
        'data': results
    }




def update_step_item(
    db: Session,
    step_item_id: int,
    admin_id: str,
    employe_id: Optional[str] = None,
    item_name: Optional[str] = None,
    step_id: Optional[int] = None,
    aval_quantity: Optional[str] = None,
    discription: Optional[str] = None,
    required_quantity: Optional[str] = None
):
    if not admin_id or admin_id.strip() == "":
        return {'status': 'false', 'message': 'Admin ID is required.'}

    step_item = db.query(StepItems).filter(
        StepItems.id == step_item_id,
        StepItems.admin_id == admin_id
    ).first()

    if not step_item:
        return {
            'status': 'false',
            'message': f'Step item with ID {step_item_id} does not exist.'
        }

   
   

    
    if item_name:
        step_item.item_name = item_name
    if step_id:
        step_item.step_id = step_id
    if aval_quantity:
        step_item.aval_quantity = aval_quantity
    if discription:
        step_item.discription = discription
    if required_quantity:
        step_item.required_quantity = required_quantity


    if employe_id:
        updated_by_type = "employee"
        updated_admin_emp_id = employe_id
    else:
        updated_by_type = "admin"
        updated_admin_emp_id = admin_id  


    step_item.updated_at = get_current_datetime()
    step_item.updated_by_type = updated_by_type
    step_item.updated_admin_emp_id = updated_admin_emp_id

    db.commit()
    db.refresh(step_item)

    return {
        'status': 'true',
        'message': 'Step item updated successfully.',
        'data': step_item
    }
    
    


def delete_step_item(db: Session, request: StepItemDeleteRequest):
    
    step_item = db.query(StepItems).filter(
        StepItems.id == request.step_item_id, 
        StepItems.admin_id == request.admin_id
    ).first()

    if not step_item:
        return {
            "status": "false",
            "message": f"Step item with ID {request.step_item_id} does not exist."
        }

    db.delete(step_item)
    db.commit()

    return {
        "status": "true",
        "message": f"Step item with ID {request.step_item_id} deleted successfully."
    }



