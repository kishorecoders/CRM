from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from src.database import get_db
from src.parameter import get_token
from typing import List
from src.ProductTemplates.models import TemplateInput , TemplateRead , TemplateDelete
from src.ProductTemplates.service import create ,get , delete


router = APIRouter()


@router.post("/create_product_template")
def create_product_templates_details(
    templateInput: TemplateInput,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    
    return create(db=db, templateInput=templateInput)

@router.post("/get_product_template")
def get_product_templates_details(
    templateRead: TemplateRead,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    
    return get(db=db, templateRead=templateRead)



@router.post("/delete_product_template")
def delete_product_templates_details(
    delete_data: TemplateDelete,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    return delete(db=db, delete_data=delete_data)


# from src.ProductTemplates.models import TemplateItem
# from src.ProductTemplates.models import TemplateInput ,ProductTemplate , TemplateRead , TemplateDelete
# from datetime import datetime
# import json

# @router.put("/template/{template_id}/update", tags=["Template"])
# def update_template(
#     template_id: int,
#     updated_items: List[TemplateItem],
#     db: Session = Depends(get_db)
# ):
#     template = db.query(ProductTemplate).filter(ProductTemplate.id == template_id).first()

#     if not template:
#         raise HTTPException(status_code=404, detail="Template not found")

#     try:
#         existing_data_raw = template.get_template_name()
#         if isinstance(existing_data_raw, str):
#             existing_data = json.loads(existing_data_raw)
#         else:
#             existing_data = existing_data_raw or []
#     except json.JSONDecodeError:
#         raise HTTPException(status_code=400, detail="Invalid JSON in template_name field")

#     # Ensure we are working with a list of dicts
#     if not isinstance(existing_data, list):
#         existing_data = []

#     existing_map = {item["temp_key_name"]: item["temp_value"] for item in existing_data if isinstance(item, dict)}

#     updated_keys = []
#     for item in updated_items:
#         existing_map[item.temp_key_name] = item.temp_value
#         updated_keys.append(item.temp_key_name)

#     updated_list = [{"temp_key_name": k, "temp_value": v} for k, v in existing_map.items()]

#     template.set_template_name(updated_list)
#     template.updated_at = datetime.now()
#     db.commit()

#     return {
#         "status": "true",
#         "message": "Template updated successfully",
#         "updated_keys": updated_keys
#     }



from src.ProductTemplates.models import ProductTemplate , TemplateUpdate
from datetime import datetime

@router.post("/Product_template_update/")
def update_template(
    template_id: TemplateUpdate,
    # updated_items: List[TemplateItem],
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    
    template = db.query(ProductTemplate).filter(ProductTemplate.id == template_id.template_id).first()

    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    # Convert updated_items to list of dicts
    updated_list = [
        {"temp_key_name": item.temp_key_name, "temp_value": item.temp_value}
        for item in template_id.updated_items
    ]

    template.set_template_name(updated_list)
    template.updated_at = datetime.now()
    db.commit()

    return {
        "status": "true",
        "message": "Template updated successfully",
        "updated_keys": [item.temp_key_name for item in template_id.updated_items]
    }

