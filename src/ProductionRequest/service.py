from typing import List,Optional
from sqlalchemy import select, outerjoin
from sqlmodel import Session
from datetime import datetime
from fastapi import status, HTTPException
from .models import ProductionRequestCreate, ProductionRequest
from sqlalchemy import desc
from src.ProductStages.models import ProductStages
from src.ProjectManagerOrder.models import ProjectManagerOrder
from src.parameter import get_current_datetime


def add_production_request(db: Session, production_request: ProductionRequestCreate):
    db_production_request = ProductionRequest(**production_request.dict())
    db.add(db_production_request)
    db.commit()
    db.refresh(db_production_request)  
    
    return {
        'status': 'true',
        'message': "Production request added successfully.",
        'data': db_production_request  
    }





from src.cre_upd_name import get_creator_updator_info
from src.Production.models import Production 
from src.Quotation.models import Quotation


def get_production_requests_by_admin_id(db: Session, admin_id: int, employee_id: Optional[str] = None) -> dict:
    stmt = (
        select(
            ProductionRequest,
            ProductStages.steps.label('stage_name') 
        )
        .outerjoin(ProductStages, ProductionRequest.stage_id == ProductStages.id)  
        .filter(ProductionRequest.admin_id == str(admin_id))  
        .order_by(desc(ProductionRequest.id))  
    )

    if employee_id:
        stmt = stmt.filter(ProductionRequest.employe_id == str(employee_id))

    results = db.execute(stmt).all()  

    if not results:
        return {
            "status": "false",
            "message": "No production requests found for the provided admin_id.",
        }

    data = []
    for request, stage_name in results:
    
        # Fetch the full ProjectManagerOrder record
        order_record = db.query(ProjectManagerOrder).filter(
            ProjectManagerOrder.id == request.order_id
        ).first()

        quotation = None
        sale_order_id = None
        order_code = None
        sales_order = None

        if order_record:
            order_code = order_record.order_id
            if order_record.quotation_id:
                quotation = db.query(Quotation).filter(
                    Quotation.id == order_record.quotation_id
                ).first()
                sale_order_id = quotation.pi_number if quotation else None


        if order_record.status == "Manual" :
            sales_order = order_record.manual_sale_order_id if order_record.status == "Manual" else None

        if order_record.status == "Won":
            quot = db.query(Quotation).filter(Quotation.id == order_record.quotation_id).first()
            sales_order = quot.pi_number if quot else None



        # Fetch the product code
        product_code = None
        prodc = db.query(Production).filter(
            Production.id == request.production_id
        ).first()
        if prodc:
            product_code = prodc.product_code

        created_updated_data = get_creator_updator_info(
            admin_emp_id=request.admin_emp_id,
            created_by_type=request.created_by_type,
            updated_admin_emp_id=request.updated_admin_emp_id,
            updated_by_type=request.updated_by_type,
          db=db
        )
       
        request_data = {
            "id": request.id,
            "admin_id": request.admin_id,
            "employe_id": request.employe_id,
            "production_id": request.production_id,
            "material_name": request.material_name,
            "quantity": request.quantity,
            "order_id": request.order_id,
            "order_code": sales_order if sales_order else None,

            "pruduct_name": request.pruduct_name,
            "product_code": product_code if prodc else None,
            "sale_order_id": sale_order_id if sale_order_id else None,
            "stage_id": request.stage_id,
            "status": request.status,
            "created_at": request.created_at,
            "updated_at": request.updated_at,
            "stage_name": stage_name,  
        }
        data.append({**request_data,**created_updated_data})


    return {
        "status": "true",
        "message": "Production requests retrieved successfully.",
        "data": data,
    }
    
    
    

def update_production_request(db: Session, production_request_id: int, admin_id: str, status: str ,employe_id:Optional[str] = None):
    production_request = db.query(ProductionRequest).filter(
        ProductionRequest.id == production_request_id,
        ProductionRequest.admin_id == admin_id
    ).first()

    if not production_request:
        raise HTTPException(status_code=404, detail="Production request not found")

    if employe_id:
        updated_by_type = "employee"
        updated_admin_emp_id = employe_id
    else:
        updated_by_type = "admin"
        updated_admin_emp_id = admin_id


    production_request.updated_by_type = updated_by_type
    production_request.updated_admin_emp_id = updated_admin_emp_id
    production_request.status = status
    production_request.updated_at = get_current_datetime()

    db.add(production_request)
    db.commit()
    db.refresh(production_request)
    return production_request

