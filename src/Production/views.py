import json
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from src.database import get_db
from src.Production.models import Production,ProductionCreateList,ProductionRead,ProductionStatusUpdate ,AddRemark , ProductionStatusUpdateFromStageid,Add_Check_Remark
from src.Production.service import create_multiple_products,fetch_products_by_admin,update_production_status
from src.parameter import get_token
from datetime import datetime
from src.ProductStages.models import ProductStages
from src.ProductionRequest.models import ProductionRequest
from src.StoreCheckPoint.models import StoreCheckPoint


router = APIRouter()




@router.post("/add_production_products")
def create_multiple_production_products(
    product_list: ProductionCreateList,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    
    return create_multiple_products(db=db, products=product_list.products)





@router.post("/get_products_by_admin")
def get_products_by_admin(
    products_data: ProductionRead,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
   
    if auth_token != get_token():
        return {
            "status": "false",
            "message": "Unauthorized Request"
        }

    
    result = fetch_products_by_admin(
        db=db,
        admin_id=products_data.admin_id,
        employee_id=products_data.employee_id,
        stage_id=products_data.stage_id,
    )

    
    return result



from src.StoreSubProductEmployee.models import StoreSubProductEmployee
from src.StoreCheckPoint.models  import StoreCheckPoint     
from src.parameter import get_current_datetime

@router.post("/update_production_status")
def update_production_status_api(
    status_update: ProductionStatusUpdate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    
    production = db.query(Production).filter(
        Production.admin_id == status_update.admin_id,
        Production.id == status_update.production_id
    ).first()

    if not production:
        return {
            "status": "false",
            "message": "Production record not found for the provided admin_id and production_id."
        }


    
    if status_update.employee_id and production.assign_employee != status_update.employee_id:
        return {
            "status": "false",
            "message": "Employee ID does not match the assigned employee for this production."
        }

    
    if status_update.status == "complete":
        related_request = db.query(ProductionRequest).filter(
            ProductionRequest.production_id == production.id,
            ProductionRequest.admin_id == production.admin_id,
            ProductionRequest.status != "completed"
        ).first()
  
        if related_request:
            return {
                "status": "false",
                "message": "Production cannot be marked as 'Completed' until all related production requests are completed."
            }
  
        subproducts = db.query(StoreSubProductEmployee).filter(StoreSubProductEmployee.production_id == str(production.id)).all()
  
        if subproducts:
            for subproduct in subproducts:
                stcheck = db.query(StoreCheckPoint).filter(
                    StoreCheckPoint.subproduct_id == subproduct.id,
                    StoreCheckPoint.production_id == str(production.id),
                    StoreCheckPoint.check_point_status == 0
                ).first()
                if stcheck:
                    return {
                        "status": "false",
                        "message": f"Please Checked {stcheck.check_point_name}",
                    }
        else:
            if status_update.status == "complete":
                product_stage = db.query(ProductStages).filter(
                    ProductStages.id == production.stage_id
                ).first()

                if product_stage:
                    product_stage.status = "Completed"
                    product_stage.updated_at = get_current_datetime()
                    db.add(product_stage)
        

    if status_update.status == "in-progress":
        production.started_at = get_current_datetime()
    
    if status_update.status:
        production.status = status_update.status

    if status_update.assign_employee:
        production.assign_employee = status_update.assign_employee

    if status_update.comment_mark:
        production.comment_mark = status_update.comment_mark


    if status_update.subproduct_list_ids:
        existing_ids = []
        if production.subproduct_list_ids:
            try:
                existing_ids = json.loads(production.subproduct_list_ids)
            except Exception:
                existing_ids = []

        # Convert all to strings before merging
        existing_ids = list(map(str, existing_ids))
        new_ids = list(map(str, status_update.subproduct_list_ids))

        merged_ids = list(set(existing_ids + new_ids))  # Merge and deduplicate
        merged_ids.sort()  # Optional: sort for consistent output

        production.subproduct_list_ids = json.dumps(merged_ids) if status_update.subproduct_list_ids is not None else production.subproduct_list_ids

    production.updated_at = get_current_datetime()
    db.add(production)

    # Commit changes once (reduces redundant writes)
    db.commit()
    db.refresh(production)

    return {
        "status": "true",
        "message": "Production record updated successfully.",
        "data": {
            "production_id": production.id,
            "status": production.status,
            "comment_mark": production.comment_mark,
            "updated_at": production.updated_at
        }
    }




@router.post("/add_remark")
def addremark(
    request:  AddRemark,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    
    production = db.query(Production).filter(Production.id == request.Production_id).first()
    if not production:
            return {
                "status": "false",
                "message": "Account not found",
            }
    production.add_remark = request.remark

    db.add(production)
    db.commit()
    db.refresh(production)
    
    
    return {
        "status": "true",
        "message": f"Remark added successfully",
    }



@router.post("/update_production_status_stage_id")
def update_production_status_api(
    status_update: ProductionStatusUpdateFromStageid,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    # Check for the auth token
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    # Query the production record
    production = db.query(Production).filter(
        Production.admin_id == status_update.admin_id,
        Production.stage_id == status_update.stage_id
    ).first()

    # If production not found, return an error
    if not production:
        return {
            "status": "false",
            "message": "No production requests found for the given criteria",
        }

    # If a valid production is found, set status to an empty string
    production.status = ""  # Set status to empty string


    production. production_engeneer_remark = ""
    production.production_engeneer_status = ""
    production.status = ""

    try:
        db.add(production)
        db.commit()
        db.refresh(production)
        return {
            "status": "true",
            "message": "Production record updated successfully.",
        }
    except Exception as e:
        db.rollback()  # Rollback in case of an error
        return {"status": "false", "message": f"Error updating record: {str(e)}"}



from src.StoreCheckPoint.models import StoreCheckPoint

@router.post("/add_check_remark")
def add_check(
    request:  Add_Check_Remark,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    
    production = db.query(Production).filter(Production.id == int(request.production_id)).first()
    if not production:
        return {
            "status": "false",
            "message": "Production not found",
        }
   
    if request.production_engeneer_status == "Approved" or request.production_engeneer_status == "Approve":
        product_stage = db.query(ProductStages).filter(
            ProductStages.id == production.stage_id
        ).first()

        if product_stage:
            product_stage.status = "Completed"
            product_stage.updated_at = get_current_datetime()
            db.add(product_stage)
                

    production.production_engeneer_status = request.production_engeneer_status
    if request.production_engeneer_status == "Approved" or request.production_engeneer_status == "Approve":
        production.status = "complete"

    elif request.point and all(check.check_status == 1 for check in request.point):
        production.status = "complete"

    else:
        production.status = "in-progress" if request.production_engeneer_status == "Update" and production.status == "complete" else production.status
    
    
    
    #production.status = "in-progress" if request.production_engeneer_status == "Update" and production.status == "complete" else production.status
    production.production_engeneer_remark = request.check_remark

    if request.employee_id:
        updated_by_type = "employee"
        updated_admin_emp_id = request.employee_id
    else:
        updated_by_type = "admin"
        updated_admin_emp_id = request.admin_id  

    
    if request.point:
        for check in request.point:
            check_point = db.query(StoreCheckPoint).filter(StoreCheckPoint.id == check.checkpoint_id).first()
            if not check_point:
                continue  # Or handle not found case if needed

            # check_point.check_remark = request.check_remark
            check_point.check_remark_date = get_current_datetime()
            check_point.check_emp_id = request.employee_id or None
            check_point.check_admin_id = request.admin_id or None

            check_point.check_status = check.check_status
            check_point.check_remark = check.checkpoint_remark
            check_point.check_point_status = 0 if check.check_status == 2 else check.check_status

            check_point.updated_by_type = updated_by_type
            check_point.updated_admin_emp_id = updated_admin_emp_id
            check_point.updated_by_date = get_current_datetime()
            

            db.add(check_point)
            #db.refresh(check_point)

    db.commit()
    db.refresh(production)
                
                
    return {
        "status": "true",
        "message": f"Remark added successfully",
    }



from src.ProductTemplates.models import ProductTemplate
from src.QuotationSubProductEmployee.models import QuotationSubProductEmployee
from src.QuotationProductEmployee.models import QuotationProductEmployee
from src.StoreManagerProduct.models import storeManagerProduct



@router.post("/get_gobcard_details")
def get_gobcard_details(
    admin:str,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    # ? Authorization
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    # ? Get non-visible products
    products = db.query(storeManagerProduct).filter(
        storeManagerProduct.admin_id == admin,
        storeManagerProduct.is_visible == True
        ).all()
    result = []

    for product_obj in products:
        product = product_obj.__dict__.copy()

        # ? Sub-products
        sub_products = db.query(QuotationSubProductEmployee).filter(
            QuotationSubProductEmployee.product_id == str(product["id"])
        ).all()

        # ? Template info
        templates = db.query(ProductTemplate).filter(
            ProductTemplate.product_id == str(product["id"])
        ).all()

        # ? Structure the response
        result.append({
            "product": product,
            "sub_products": [sub.__dict__.copy() for sub in sub_products],
            "templates": [tpl.__dict__.copy() for tpl in templates],
        })

    return {
        "status": "true",
        "message": "GoB card details fetched successfully",
        "data": result
    }













