from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status,HTTPException
from sqlalchemy import func,cast,String,Integer
from .models import GrnOrderProductRead , GrnOrderProduct


def get(db: Session, order: GrnOrderProductRead):

    query = db.query(GrnOrderProduct).filter(
        GrnOrderProduct.admin_id == order.admin_id
    )

    if order.grn_order_id:
        query = query.filter(GrnOrderProduct.grn_order_id == order.grn_order_id)

    if order.employee_id:
        query = query.filter(GrnOrderProduct.employee_id == order.employee_id)

    data = query.all()

    if not data:
        return {
            "status": "false",
            "message": f"No products found for admin_id={order.admin_id} and grn_order_id={order.grn_order_id}"
        }

    return {
        "status": "true",
        "message": "Products retrieved successfully.",
        "data": data,
    }
