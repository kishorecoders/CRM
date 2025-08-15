from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .service import create_quotation_template,get_quotation_templates_by_admin ,delete_quotation_templates
from src.QuotationTemplate.models import QuotationTemplateCreate,AdminIDRequest,QuotationTemplatesDelete
from src.database import get_db
from fastapi import APIRouter, Depends, Header, HTTPException, Body
from typing import List 
from src.parameter import get_token

router = APIRouter()

@router.post("/quotation-template")
def add_quotation_template(
    template: QuotationTemplateCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
   
    if not template.admin_id or not template.template_name:
        return {
        "status": "false",
        "message": "Admin ID and Template Name are required",
        
    }
    new_template = create_quotation_template(db, template)
    return {
        "status": "true",
        "message": "Quotation template created successfully.",
        "data": {
            "id": new_template.id,
            "admin_id": new_template.admin_id,
            "template_name": new_template.template_name,
            "created_at": new_template.created_at,
            "updated_at": new_template.updated_at,
        }
    }



@router.post("/get-quotation-templates")
def get_quotation_templates(
    admin_data: AdminIDRequest,  
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    
    
    if not admin_data.admin_id:
        raise HTTPException(status_code=400, detail="Admin ID is required.")
    
    emp_id = admin_data.employee_id

    templates = get_quotation_templates_by_admin(db, admin_data.admin_id , emp_id)
    
    
    if not templates:
        return {
            "status":"false",
            "message":"No templates found for this admin.",
            "data":[]
        }

    
    return {
        "status":"true",
        "message":"Quotation templates retrieved successfully.",
        "data":templates
    }

@router.post("/quotation-templates-delete")
def quotation_templates_delete(
    response: QuotationTemplatesDelete,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    return delete_quotation_templates(db, response.template_id)
