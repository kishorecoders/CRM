from fastapi import APIRouter, Depends, HTTPException, Header
from sqlmodel import Session
from src.database import get_db
from .models import ProductionRequestCreate,ProductionRequestRead,ProductionRequestUpdate,ProductionRequest , ProductionRequestDelete
from .service import add_production_request,get_production_requests_by_admin_id,update_production_request
from src.parameter import get_token

router = APIRouter()

@router.post("/add_production_requests")
def add_production_requests_api(
    production_requests: list[ProductionRequestCreate],  
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    if not production_requests:
        return {
            "status": "false",
            "message": "At least one production request is required."
        }

    added_requests = []
    
    
    db_objects = []
    for request in production_requests:
        if not request.production_id:
            return {
                "status": "false",
                "message": "Production ID is required in all requests."
            }
        
        if request.employe_id:
            created_by_type = "employee"
            admin_emp_id = request.employe_id
        else:
            created_by_type = "admin"
            admin_emp_id = request.admin_id
        data = request.dict()
        data["created_by_type"] = created_by_type
        data["admin_emp_id"] = admin_emp_id        

        db_object = ProductionRequest(**data)
        db_objects.append(db_object)

    
    db.add_all(db_objects)
    db.commit()

    
    for obj in db_objects:
        db.refresh(obj)
        added_requests.append(obj.dict())

    return {
        "status": "true",
        "message": "Production requests added successfully.",
        "data": added_requests
    }






# @router.post("/get_production_requests")
# def get_production_requests_api(
#     request_data: ProductionRequestRead,
#     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#     db: Session = Depends(get_db),
# ):
#     if auth_token != get_token():
#         return {
#             "status": "false",
#             "message": "Unauthorized Request",
#         }

#     return get_production_requests_by_admin_id(
#         db=db, admin_id=request_data.admin_id, employee_id=request_data.employee_id
#     )
@router.post("/get_production_requests")
def get_production_requests_api(
    request_data: ProductionRequestRead,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db),
):
    if auth_token != get_token():
        return {
            "status": "false",
            "message": "Unauthorized Request",
        }

    return get_production_requests_by_admin_id(
        db=db, admin_id=request_data.admin_id, employee_id=request_data.employee_id
    )
    
    
    

@router.post("/update_production_requests", response_model=dict)
def update_production_request_api(
    request: ProductionRequestUpdate, 
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)):


    if auth_token != get_token():
        return {
            "status": "false",
            "message": "Unauthorized Request",
        }
    
    try:
        updated_request = update_production_request(
            db, 
            request.production_request_id, 
            request.admin_id, 
            request.status,
            request.employe_id

        )
        return {
            "status": "true",
            "message": "Production request updated successfully",
            "data": updated_request
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        

@router.post("/delete_production_requests", response_model=dict)
def update_production_request_api(
    request: ProductionRequestDelete, 
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    try:
        if auth_token != get_token():
            return {
                "status": "false",
                "message": "Unauthorized Request",
            }

        pdr = db.query(ProductionRequest).filter(
            ProductionRequest.admin_id == request.admin_id,
            ProductionRequest.stage_id == request.stage_id
        ).all()

        if not pdr:
            return {
                "status": "false",
                "message": "No production requests found for the given criteria",
            }

        for pr in pdr:
            db.delete(pr)
        
        db.commit()  # Remember to commit after delete
        
        return {
            "status": "true",
            "message": "Production requests deleted successfully",
            "data": {"deleted_count": len(pdr)}
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
