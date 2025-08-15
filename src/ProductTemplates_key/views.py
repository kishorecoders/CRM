from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from src.database import get_db
from src.parameter import get_token
from typing import List
from src.ProductTemplates_key.models import ProductTemplateKey , ProductTemplateKeyCreate , ProductTemplateKeyUpdate , ProductTemplateKeyDelete
from src.ProductTemplates_key.service import create , update , delete


router = APIRouter()


@router.post("/create_product_template")
def create_product_templates_details(
    templates_input: List[ProductTemplateKeyCreate],
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    
    return create(db=db, templates_input=templates_input)


@router.post("/update_product_template")
def update_product_template_detail(
    template_input: ProductTemplateKeyUpdate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    return update(db=db, template_input=template_input)


@router.post("/delete_product_template_key")
def delete_product_template_key(
    template_input: ProductTemplateKeyDelete,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    return delete(db=db, template_input=template_input)
