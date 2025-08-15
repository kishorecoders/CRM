from sqlalchemy.orm import Session
from typing import Dict, List,Optional
from sqlalchemy import select
from sqlalchemy import desc
from src.ProductTemplates_key.models import ProductTemplateKey , ProductTemplateKeyCreate , ProductTemplateKeyUpdate , ProductTemplateKeyDelete


def create(db: Session, templates_input: List[ProductTemplateKeyCreate]):
    created = []
    failed = []

    for template in templates_input:
        existing = db.query(ProductTemplateKey).filter(
            ProductTemplateKey.template_id == template.template_id,
            ProductTemplateKey.temp_key_name == template.temp_key_name
        ).first()

        if existing:
            failed.append({
                "template_id": template.template_id,
                "temp_key_name": template.temp_key_name,
                "message": "Template key already exists"
            })
            continue

        db_template = ProductTemplateKey(
            admin_id=template.admin_id,
            emp_id=template.emp_id,
            template_id=template.template_id,
            temp_key_name=template.temp_key_name,
            temp_value=template.temp_value,
        )

        db.add(db_template)
        db.commit()
        db.refresh(db_template)

        created.append({
            "id": db_template.id,
            "admin_id": db_template.admin_id,
            "emp_id": db_template.emp_id,
            "template_id": db_template.template_id,
            "temp_key_name": db_template.temp_key_name,
            "temp_value": db_template.temp_value
        })

    return {
        "status": "true" if created else "false",
        "message": f"{len(created)} created, {len(failed)} failed",
        "created_templates": created,
        "failed_templates": failed,
    }



def update(db: Session, template_input: ProductTemplateKeyUpdate):
    existing = db.query(ProductTemplateKey).filter(
        ProductTemplateKey.template_id == template_input.temp_key_id,
    ).first()

    if not existing:
        return {
            "status": "false",
            "message": "Template key not found"
        }

    existing.temp_key_name = template_input.temp_key_name
    existing.temp_value = template_input.temp_value

    db.commit()
    db.refresh(existing)

    return {
        "status": "true",
        "message": "Template key updated successfully",
        "updated_template": {
            "id": existing.id,
            "admin_id": existing.admin_id,
            "emp_id": existing.emp_id,
            "template_id": existing.template_id,
            "temp_key_name": existing.temp_key_name,
            "temp_value": existing.temp_value
        }
    }



def delete(db: Session, template_input: ProductTemplateKeyDelete):
    existing = db.query(ProductTemplateKey).filter(
        ProductTemplateKey.id == template_input.temp_key_id
    ).first()

    if not existing:
        return {
            "status": "false",
            "message": "Template key not found"
        }

    db.delete(existing)
    db.commit()

    return {
        "status": "true",
        "message": "Template key deleted successfully",
    }
