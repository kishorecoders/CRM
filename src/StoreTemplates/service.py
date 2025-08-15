from sqlalchemy.orm import Session
from typing import Dict, List,Optional
from sqlalchemy import select
from sqlalchemy import desc
from fastapi import APIRouter, Depends, HTTPException, Header
from src.parameter import get_current_datetime
from src.ProductTemplates.models import TemplateInput ,ProductTemplate , TemplateRead , TemplateDelete
import json

def create(db: Session, templateInput: TemplateInput):
    created = []
    skipped = []

    for item in templateInput.template_name:
        data = item.dict() if hasattr(item, 'dict') else item
        key_name = data.get("temp_key_name")

        existing = db.query(ProductTemplate).filter(
            ProductTemplate.template_name.contains(f'"temp_key_name": "{key_name}"')
        ).first()

        if existing:
            skipped.append(key_name)
            continue 

        db_template = ProductTemplate(
            admin_id=templateInput.admin_id,
            emp_id=templateInput.emp_id,
            product_id=templateInput.product_id,
        )
        db_template.set_template_name([data])

        db.add(db_template)
        db.commit()
        db.refresh(db_template)

        created.append({
            "id": db_template.id,
            "admin_id": db_template.admin_id,
            "emp_id": db_template.emp_id,
            "product_id": db_template.product_id,
            "template_name": db_template.get_template_name()
        })

    return {
        "status": "true",
        "message": f"{len(created)} template(s) created, {len(skipped)} skipped (duplicates)",
        "created_templates": created,
        # "skipped_templates": skipped
    }




def get(db: Session, templateRead: TemplateRead):

    query = db.query(ProductTemplate) 

    if templateRead.product_id:
        query = query.filter(ProductTemplate.product_id == templateRead.product_id)

    results = query.all()

    response = []
    for r in results:
        response.append({
            "id": r.id,
            "admin_id": r.admin_id,
            "emp_id": r.emp_id,
            "product_id": r.product_id,
            "template_name": json.loads(r.template_name) if r.template_name else [] 
        })

    return {
        "status": "true",
        "message": f"{len(response)} templates found",
        "data": response
    }

def delete(db: Session, delete_data: TemplateDelete):
    query = db.query(ProductTemplate)

    if delete_data.id:
        query = query.filter(ProductTemplate.id == delete_data.id)

    records = query.all()

    if not records:
        return {"status": "false", "message": "No matching templates found"}

    deleted_ids = []
    for record in records:
        deleted_ids.append(record.id)
        db.delete(record)

    db.commit()

    return {
        "status": "true",
        "message": f"Deleted {len(deleted_ids)} template(s)",
    }



