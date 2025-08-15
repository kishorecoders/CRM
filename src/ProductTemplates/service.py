from sqlalchemy.orm import Session
from typing import Dict, List,Optional
from sqlalchemy import select
from sqlalchemy import desc
from fastapi import APIRouter, Depends, HTTPException, Header
from src.parameter import get_current_datetime
from src.ProductTemplates.models import TemplateInput ,ProductTemplate , TemplateRead , TemplateDelete
import json

def create(db: Session, templateInput: TemplateInput):
  

    existing = db.query(ProductTemplate).filter(
        ProductTemplate.template_name == templateInput.template_name,
        ProductTemplate.product_id == templateInput.product_id,
    ).first()

    if existing:
        return {
            "status": "false",
            "message": "Templates Name Already Exist",

        }

    db_template = ProductTemplate(
        admin_id=templateInput.admin_id,
        emp_id=templateInput.emp_id,
        product_id=templateInput.product_id,
        template_name=templateInput.template_name,
    )

    db.add(db_template)
    db.commit()
    db.refresh(db_template)


    return {
        "status": "true",
        "message": f"template(s) created",
        "created_templates": {
        "id": db_template.id,
        "admin_id": db_template.admin_id,
        "emp_id": db_template.emp_id,
        "product_id": db_template.product_id,
        "template_name": db_template.template_name
    }
    }

# def create(db: Session, templateInput: TemplateInput):
#     created = []
#     skipped = []

#     for item in templateInput.template_name:
#         data = item.dict() if hasattr(item, 'dict') else item
#         key_name = data.get("temp_key_name")

#         existing = db.query(ProductTemplate).filter(
#             ProductTemplate.template_name.contains(f'"temp_key_name": "{key_name}"')
#         ).first()

#         if existing:
#             skipped.append(key_name)
#             continue 

#         db_template = ProductTemplate(
#             admin_id=templateInput.admin_id,
#             emp_id=templateInput.emp_id,
#             product_id=templateInput.product_id,
#         )
#         db_template.set_template_name([data])

#         db.add(db_template)
#         db.commit()
#         db.refresh(db_template)

#         created.append({
#             "id": db_template.id,
#             "admin_id": db_template.admin_id,
#             "emp_id": db_template.emp_id,
#             "product_id": db_template.product_id,
#             "template_name": db_template.get_template_name()
#         })

#     return {
#         "status": "true",
#         "message": f"{len(created)} template(s) created, {len(skipped)} skipped (duplicates)",
#         "created_templates": created,
#         # "skipped_templates": skipped
#     }


from src.ProductTemplates_key.models import ProductTemplateKey
from src.StoreManagerProduct.models import storeManagerProduct
from sqlalchemy.orm import Session
from typing import Dict
import json

def get(db: Session, templateRead: TemplateRead) -> Dict:
    product_id = None

    # Step 1: Get product_id from product_code or directly
    if templateRead.product_code:
        product = db.query(storeManagerProduct).filter(
            storeManagerProduct.item_code == templateRead.product_code
        ).first()
        if not product:
            return {
                "status": "false",
                "message": "No product found for the given product code"
            }
        product_id = str(product.id)
    elif templateRead.product_id:
        product_id = templateRead.product_id

    if not product_id:
        return {
            "status": "false",
            "message": "Product ID or Product Code must be provided"
        }

    # Step 2: Fetch all ProductTemplates related to the product_id
    templates = db.query(ProductTemplate).filter(
        ProductTemplate.product_id == product_id
    ).all()

    if not templates:
        return {
            "status": "false",
            "message": "No Templates found for the given product"
        }

    # Step 3: Format response with related keys
    response = []
    for template in templates:
        keys = db.query(ProductTemplateKey).filter(
            ProductTemplateKey.template_id == template.id
        ).all()

        key_data = [{
            "id": key.id,
            "temp_key_name": key.temp_key_name,
            "temp_value": key.temp_value
        } for key in keys]

        response.append({
            "id": template.id,
            "admin_id": template.admin_id,
            "emp_id": template.emp_id,
            "product_id": template.product_id,
            "template_name": template.template_name,
            "template_keys": key_data
        })

    return {
        "status": "true",
        "message": f"{len(response)} templates found",
        "data": response
    }



# from src.StoreManagerProduct.models import storeManagerProduct
# from sqlalchemy.orm import Session
# from typing import Dict
# import json

# def get(db: Session, templateRead: TemplateRead) -> Dict:
#     product_id = None

#     if templateRead.product_code:
#         product = db.query(storeManagerProduct).filter(
#             storeManagerProduct.item_code == templateRead.product_code
#         ).first()
#         if not product:
#             return {
#                 "status": "false",
#                 "message": "No product found for the given product code"
#             }
#         product_id = str(product.id)
#     elif templateRead.product_id:
#         product_id = templateRead.product_id

#     if not product_id:
#         return {
#             "status": "false",
#             "message": "Product ID or Product Code must be provided"
#         }

#     results = db.query(ProductTemplate).filter(
#         ProductTemplate.product_id == product_id
#     ).all()

#     if not results:
#         return {
#             "status": "false",
#             "message": "No Templates found for the given product"
#         }

#     response = []
#     for r in results:
#         response.append({
#             "id": r.id,
#             "admin_id": r.admin_id,
#             "emp_id": r.emp_id,
#             "product_id": r.product_id,
#             "template_name": r.template_name
#         })

#     return {
#         "status": "true",
#         "message": f"{len(response)} templates found",
#         "data": response
#     }

# from src.StoreManagerProduct.models import storeManagerProduct
# from sqlalchemy.orm import Session
# from typing import Dict
# import json

# def get(db: Session, templateRead: TemplateRead) -> Dict:
#     product_id = None

#     if templateRead.product_code:
#         product = db.query(storeManagerProduct).filter(
#             storeManagerProduct.item_code == templateRead.product_code
#         ).first()
#         if not product:
#             return {
#                 "status": "false",
#                 "message": "No product found for the given product code"
#             }
#         product_id = str(product.id)
#     elif templateRead.product_id:
#         product_id = templateRead.product_id

#     if not product_id:
#         return {
#             "status": "false",
#             "message": "Product ID or Product Code must be provided"
#         }

#     results = db.query(ProductTemplate).filter(
#         ProductTemplate.product_id == product_id
#     ).all()

#     if not results:
#         return {
#             "status": "false",
#             "message": "No Templates found for the given product"
#         }

#     response = []
#     for r in results:
#         response.append({
#             "id": r.id,
#             "admin_id": r.admin_id,
#             "emp_id": r.emp_id,
#             "product_id": r.product_id,
#             "template_name": json.loads(r.template_name) if r.template_name else []
#         })

#     return {
#         "status": "true",
#         "message": f"{len(response)} templates found",
#         "data": response
#     }

from src.ProductTemplates_key.models import ProductTemplateKey

def delete(db: Session, delete_data: TemplateDelete):
    # Fetch the ProductTemplate by ID
    template = db.query(ProductTemplate).filter(
        ProductTemplate.id == delete_data.id
    ).first()

    if not template:
        return {"status": "false", "message": "Template not found"}

    # Delete related ProductTemplateKey entries
    db.query(ProductTemplateKey).filter(
        ProductTemplateKey.template_id == template.id
    ).delete(synchronize_session=False)

    # Delete the template itself
    db.delete(template)
    db.commit()

    return {
        "status": "true",
        "message": f"Template ID {template.id} and related keys deleted"
    }

# def delete(db: Session, delete_data: TemplateDelete):
#     query = db.query(ProductTemplate)

#     if delete_data.id:
#         query = query.filter(ProductTemplate.id == delete_data.id)

#     records = query.all()

#     if not records:
#         return {"status": "false", "message": "No matching templates found"}

#     deleted_ids = []
#     for record in records:
#         deleted_ids.append(record.id)
#         db.delete(record)

#     db.commit()

#     return {
#         "status": "true",
#         "message": f"Deleted {len(deleted_ids)} template(s)",
#     }



