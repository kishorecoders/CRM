from fastapi import APIRouter, Depends, Header
from sqlmodel import Session
from src.database import get_db
from .models import AssignStageRequest,StageDeleteRequest,GetStageListRequest
from .service import assign_or_update_stage,delete_stage
from src.parameter import get_token


from src.ProductStages.models import ProductStages
from src.ProductSteps.models import ProductSteps




router = APIRouter()


# @router.post("/assign_update_stage")
# def assign_or_update_stage_api(
#     request: AssignStageRequest,
#     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#     db: Session = Depends(get_db)
# ):
#     if auth_token != get_token():
#         return {"status": "false", "message": "Unauthorized Request"}

#     return assign_or_update_stage(request, db)

@router.post("/assign_update_stage")
def assign_or_update_stage_api(
    request: AssignStageRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    return assign_or_update_stage(request, db)



@router.post("/stage_delete")
def delete_stage_api(
    request: StageDeleteRequest,
    auth_token: str = Header(None, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        return {
            "status": "false",
            "message": "Unauthorized Request"
        }

   
    return delete_stage(request, db)
    
    
    
    
    

@router.post("/get_stage_list")
def get_stage_list(
    request: GetStageListRequest, 
    auth_token: str = Header(None, alias="AuthToken"),
    db: Session = Depends(get_db)):

    if auth_token != get_token():
        return {
            "status": "false",
            "message": "Unauthorized Request"
        }
    
    product_stages_query = db.query(ProductStages).filter(
        ProductStages.product_id == request.product_id,
        ProductStages.type == request.type
    ).all()

    if not product_stages_query:
        return {"status": "false", "message": "No stages found for this product."}

    
    #step_ids = [int(stage.step_id) for stage in product_stages_query if stage.step_id is not None]
    step_ids = [int(stage.step_id) for stage in product_stages_query if stage.step_id not in [None, ''] and str(stage.step_id).isdigit()]
    
    step_positions = (
        db.query(ProductSteps.id, ProductSteps.position)
        .filter(ProductSteps.id.in_(step_ids))
        .all()
    )

    
    step_positions_dict = {int(step_id): position for step_id, position in step_positions}

    
    print("Step Positions:", step_positions_dict)

   
    #sorted_stages = sorted(product_stages_query, key=lambda stage: step_positions_dict.get(int(stage.step_id), float('inf')))



    sorted_stages = sorted(
        product_stages_query,
        key=lambda stage: step_positions_dict.get(
            int(stage.step_id) if stage.step_id not in [None, ''] and str(stage.step_id).isdigit() else float('inf'),
            float('inf')
        )
    )


    
    response = []
    for stage in sorted_stages:
        response.append({
            "stage_id": stage.id,
            "product_id": stage.product_id,
            "assign_employee": stage.assign_employee,
            "steps": stage.steps,
            "time_required_for_this_process": stage.time_riquired_for_this_process,
            "day": stage.day,
            "type": stage.type,
            "step_id": stage.step_id,
            "step_item": stage.step_item,
            "remark": stage.remark,
            "file_path": stage.file_path,
            "serial_number": stage.serial_number,
            "parent_stage_id": stage.parent_stage_id,
            #"position": step_positions_dict.get(int(stage.step_id), None) 
            "position": step_positions_dict.get(
              int(stage.step_id) if stage.step_id not in [None, ''] and str(stage.step_id).isdigit() else None,
              None
          )
        })

    return {
        "status": "true",
        "message": "Stages retrieved successfully",
        "data": response
    }

