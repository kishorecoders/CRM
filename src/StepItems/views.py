from typing import List,Optional
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from .models import StepItemsCreate,StepItemFilterRequest,StepItemUpdateRequest,StepItemDeleteRequest,StepItemsBulkCreateRequest
from .service import create,get_items_by_filter,update_step_item,delete_step_item,create_multiple
from src.parameter import get_token

router = APIRouter()

@router.post("/create_step_item")
def create_step_item_details(
    step_item: StepItemsCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    
    return create(db=db, step_item=step_item)
    
    
    

@router.post("/create_multiple_step_items", response_model=dict)
def create_multiple_step_items(
    request: StepItemsBulkCreateRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

   
    response = create_multiple(db=db, step_items=request.step_items)
    return response
    
    


        
@router.post("/get_step_items")
def get_step_items(
    filter_data: StepItemFilterRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
   
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

   
    admin_id = filter_data.admin_id
    step_id = filter_data.step_id
    employee_id = filter_data.employee_id
    product_ids = filter_data.product_ids
    stage_id = filter_data.stage_id

    
    return get_items_by_filter(
        db=db,
        admin_id=admin_id,
        step_id=step_id,
        employee_id=employee_id,
        stage_id=stage_id,
        product_ids=product_ids
    )



@router.post("/update_step_item")
def update_step_item_details(
    update_data: StepItemUpdateRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    step_item_id = update_data.step_item_id
    admin_id = update_data.admin_id
    employe_id = update_data.employe_id
    item_name = update_data.item_name
    step_id = update_data.step_id
    aval_quantity = update_data.aval_quantity
    discription = update_data.discription
    required_quantity = update_data.required_quantity

    return update_step_item(
        db=db,
        step_item_id=step_item_id,
        admin_id=admin_id,
        employe_id = employe_id,
        item_name=item_name,
        step_id=step_id,
        aval_quantity=aval_quantity,
        discription=discription,
        required_quantity=required_quantity
    )



@router.post("/delete_step_item")
def delete_step_item_details(
    request: StepItemDeleteRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
   
    if auth_token != get_token():
        return {
            "status": "false",
            "message": "Unauthorized Request"
        }

   
    return delete_step_item(db=db, request=request)