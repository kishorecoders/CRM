from typing import List
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from .models import ProductStepsCreate,GetStepsRequest,ProductStepsRead,ProductSteps,UpdateStepRequest,DeleteStepRequest,DeleteStepfile
from .service import create,update_step,delete_step , delete_step_file
from src.parameter import get_token
from src.StepItems.models import StepItems,StepItemsRead
from src.StoreManagerProduct.models import storeManagerProduct
from src.AdminAddEmployee.models import AdminAddEmployee
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew
from src.cre_upd_name import get_creator_updator_info


router = APIRouter()


@router.post("/create_product_step")
def create_Step_details(
    productstep: ProductStepsCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
  
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    
    return create(db=db, productstep=productstep)



@router.post("/get_steps_list")
def get_steps_list(
    request: GetStepsRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    query = select(ProductSteps).where(ProductSteps.admin_id == request.admin_id)
    if request.employe_id:
        query = query.where(ProductSteps.employe_id == request.employe_id)

    steps_result = db.execute(query)
    steps = steps_result.scalars().all()

    if not steps:
        return {
            "status": "false",
            "message": "No steps found for the provided criteria."
        }

    steps_with_items = []
    for step in steps:

        if request.is_visible is not None:
            items_query = (
                select(StepItems)
                .join(storeManagerProduct, StepItems.product_id == storeManagerProduct.id)
                .where(StepItems.step_id == step.id)
                .where(storeManagerProduct.is_visible == request.is_visible)
            )
        else:
            items_query = select(StepItems).where(StepItems.step_id == step.id)    

        #items_query = select(StepItems).where(StepItems.step_id == step.id)
        step_items_result = db.execute(items_query)
        step_items = step_items_result.scalars().all()

        assign = bool(step_items)

        # Build item list with creator/updator data
        item_data_list = []
        for item in step_items:
            created_updated_item_data = get_creator_updator_info(
                admin_emp_id=item.admin_emp_id,
                created_by_type=item.created_by_type,
                updated_admin_emp_id=item.updated_admin_emp_id,
                updated_by_type=item.updated_by_type,
                db=db
            )
            item_dict = {
                "admin_id": item.admin_id,
                "employe_id": item.employe_id,
                "step_id": item.step_id,
                "item_name": item.item_name,
                "id": item.id,
                "aval_quantity": item.aval_quantity,
                "discription": item.discription,
                "stage_id": item.stage_id,
                "product_id": item.product_id,
                "required_quantity": item.required_quantity,
                "created_at": item.created_at,
                "updated_at": item.updated_at,
            }
            item_data_list.append({**item_dict,**created_updated_item_data})


        created_updated_data = get_creator_updator_info(
            admin_emp_id=step.admin_emp_id,
            created_by_type=step.created_by_type,
            updated_admin_emp_id=step.updated_admin_emp_id,
            updated_by_type=step.updated_by_type,
            db=db
        )

        step_data = {
            "admin_id": step.admin_id,
            "employe_id": step.employe_id,
            "step_name": step.step_name,
            "position": step.position,
            "id": step.id,
            "assign": assign,
            "items": item_data_list,
            "file_path":step.file_path,
            "type":step.type,
            "created_at": step.created_at,
            "updated_at": step.updated_at,
        }

        steps_with_items.append({**step_data,**created_updated_data})


    return {
        "status": "true",
        "message": "Steps retrieved successfully.",
        "data": steps_with_items
    }



@router.post("/update_product_step")
def update_step_details(
    request: UpdateStepRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
   
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    
    
    step_data = ProductStepsCreate(
        step_id = request.step_id,
        admin_id=request.admin_id,
        employe_id=request.employe_id,
        step_name=request.step_name,
        position=request.position,
        file_path = request.file_path
    )
    return update_step(db=db,step_data=request)



@router.post("/delete_product_step")
def delete_step_details(
    request: DeleteStepRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    
    return delete_step(
        db=db,
        admin_id=request.admin_id,
        step_id=request.step_id
    )


@router.post("/delete_product_file")
def delete_step_details(
    request: DeleteStepfile,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    
    return delete_step_file(
        db=db,
        step_id=request.step_id
    )






