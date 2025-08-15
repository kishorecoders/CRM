from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from src.database import get_db
from src.QuotationProductEmployee.models import QuotationProductEmployeeCreateList,ProductEmployeeQuery,ReleaseRequest,ProductFilterQuery,StageUpdateRequest , ProductDispatchStatusUpdate , QuotationProductEmployee,UpdateBookedStatus,bookRequest,ProductmultipleDispatchStatusUpdate
from src.QuotationProductEmployee.service import create_multiple_products,get_products_by_admin_and_employee,create_release_request,get_filtered_products,update_product_service,create_booked_request
from src.parameter import get_token
from typing import List
from src.Quotation.models import Quotation
from src.Inventoryoutward.models import InventoryOutward
from src.InventoryOutwardRemark.models import InventoryOutwardRemark

router = APIRouter()




@router.post("/create_quotation_products")
def create_multiple_quotation_products(
    product_list: QuotationProductEmployeeCreateList,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    
    return create_multiple_products(db=db, products=product_list.products)




@router.post("/get_products_by_admin")
def get_products(
    product_query: ProductEmployeeQuery,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    
    result = get_products_by_admin_and_employee(
        db=db,
        admin_id=product_query.admin_id,
        employee_id=product_query.employee_id
    )

    
    return result


@router.post("/release-request", response_model=dict)
def release_request(
    outward_data: ReleaseRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    return create_release_request(outward_data, db=db)




@router.post("/update-booked-status", response_model=dict)
def release_request(
    outward_data: bookRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    return create_booked_request(outward_data, db=db)



@router.post("/get_products_list")
def get_products_list(
    query_params: ProductFilterQuery,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db) 
):
   
    if not query_params.admin_id or query_params.admin_id.strip() == "":
        return {"status": "false", "message": "admin id is required"}
    
   
    if auth_token != get_token():
        raise HTTPException(
            status_code=401, 
            detail="Unauthorized Request"
        )
    
    
    products = get_filtered_products(
        db,
        admin_id=query_params.admin_id,
        employee_id=query_params.employee_id,
        product_name=query_params.product_name
    )
    
    return {"status": "true","message": "Products retrived successfully", "products": products}




# @router.post("/update_product_stage")
# def update_stage(
#     request: StageUpdateRequest,
#     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#     db: Session = Depends(get_db)
# ):
    
#     if auth_token != get_token():
#         raise HTTPException(status_code=401, detail="Unauthorized Request")
    

#     return update_product_service(request, db)


@router.post("/update_product_stage")
def update_stage(
    request: List[StageUpdateRequest],
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    return update_product_service(request, db)


@router.post("/approve_product_status")
def approve_quotation(
    request: ProductDispatchStatusUpdate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {
            "status": "false",
            "message": "Unauthorized Request",
        }

    product = db.query(QuotationProductEmployee).filter(
        QuotationProductEmployee.id == request.product_id,
        QuotationProductEmployee.quote_id == request.quote_id
    ).first()
    if not product:
        return {
            "status": "false",
            "message": "Product not found in this quotation",
        }

    if request.dispatch_status == "Disapproved":
        invent = db.query(InventoryOutward).filter(InventoryOutward.product_id == request.product_id).first()
        if invent:
            invent.status = "Requested"
            db.commit()
            remark = InventoryOutwardRemark(
                admin_id = request.admin_id,
                employee_id = request.employee_id,
                type = "Account Disapproved",
                InventoryOutward_id = invent.id,
                add_remark = "Approval denied by the Accounts Department.",
            )
            db.add(remark)
            db.commit()
            db.refresh(remark)


    product.dispatch_status = request.dispatch_status
    product.give_credit = request.give_credit
    product.remark = request.remark

    db.commit()

    return {
        "status": "true",
        "message": "Quotation product status updated successfully",
    }

@router.post("/approve_multiple_product_status")
def approve_quotation(
    request: ProductmultipleDispatchStatusUpdate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {
            "status": "false",
            "message": "Unauthorized Request",
        }

    for pro in request.product:
        product = db.query(QuotationProductEmployee).filter(
            QuotationProductEmployee.id == pro.product_id,
            QuotationProductEmployee.quote_id == request.quote_id
        ).first()

        if not product:
            return {
                "status": "false",
                "message": f"Product with ID {pro.product_id} not found in this quotation",
            }

        if pro.dispatch_status == "Disapproved":
            invent = db.query(InventoryOutward).filter(
                InventoryOutward.product_id == pro.product_id
            ).first()
            if invent:
                invent.status = "Requested"
                db.commit()

                remark = InventoryOutwardRemark(
                    admin_id=request.admin_id,
                    employee_id=request.employee_id,
                    type="Account Disapproved",
                    InventoryOutward_id=invent.id,
                    add_remark="Approval denied by the Accounts Department.",
                )
                db.add(remark)
                db.commit()
                db.refresh(remark)

        product.dispatch_status = pro.dispatch_status
        product.give_credit = pro.give_credit
        product.remark = pro.remark
        db.commit()

    return {
        "status": "true",
        "message": "All quotation product statuses updated successfully",
    }
