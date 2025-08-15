from .models import LateMark , LateMarkRead ,LateMarkCreate ,LetmarkUpdate,LateMarkDelete
from typing import List, Optional
from sqlmodel import Session
from sqlalchemy import desc


def get_all_latemark(db: Session , data :LateMarkRead):
    query = db.query(LateMark).filter(LateMark.admin_id == data.admin_id)
    
    if data.type:
        query = db.query(LateMark).filter(LateMark.type == data.type)
    

    query = query.order_by(desc(LateMark.id))
    
    products = db.execute(query).scalars().all()

    response_data = []

    for product in products:
        product_data = product.dict()
        # Append to response list
        response_data.append(product_data)

    return {
        "status": "true",
        "message": "Data fetched successfully",
        "data": response_data
    }



def create(db: Session, latemark_create: LateMarkCreate):
    # Check if this config_id + admin_id + select_type combination already exists
    exist = db.query(LateMark).filter(
        LateMark.admin_id == latemark_create.admin_id,
        LateMark.config_id == latemark_create.config_id,
        LateMark.select_type == latemark_create.select_type,
        LateMark.type == latemark_create.type

    ).first()

    if exist:
        return {
            "status": "false",
            "message": f"LateMark for '{latemark_create.select_type}' already exists for this config."
        }

    latemark = LateMark(**latemark_create.dict())
    db.add(latemark)
    db.commit()
    db.refresh(latemark)

    return {
        "status": "true",
        "message": "LateMark added successfully",
        "data": latemark
    }



def delete(db: Session, latemark_delete: LateMarkDelete):
    # Check if this config_id + admin_id + select_type combination already exists
    data = db.query(LateMark).filter(
        LateMark.admin_id == latemark_delete.admin_id,
        LateMark.id == latemark_delete.id
    ).first()

    if not data:
        return {
            "status": "false",
            "message": f"LateMark not Found."
        }

    db.delete(data)
    db.commit()

    return {
        "status": "true",
        "message": "LateMark Deleted successfully",
    }


def update(db: Session, latemark_update: LetmarkUpdate):
    data = db.query(LateMark).filter(
        LateMark.admin_id == latemark_update.admin_id,
        LateMark.config_id == latemark_update.config_id,
        LateMark.id == int(latemark_update.id)
    ).first()

    if not data:
        return {
            "status": "false",
            "message": "LateMark not found."
        }

    # Update fields
    if latemark_update.select_type is not None:
        data.select_type = latemark_update.select_type

    if latemark_update.content is not None:
        data.content = latemark_update.content

    if latemark_update.type is not None:
        data.type = latemark_update.type

    if latemark_update.amount_type is not None:
        data.amount_type = latemark_update.amount_type

    if latemark_update.amount is not None:
        data.amount = latemark_update.amount
    
    db.commit()
    db.refresh(data)

    return {
        "status": "true",
        "message": "LateMark updated successfully.",
        "data": data
    }



