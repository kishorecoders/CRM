from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status,HTTPException
from sqlalchemy import func,cast,String,Integer
from .models import PurchaseOrderProductRead , PurchaseOrderProduct


def get(db: Session, order: PurchaseOrderProductRead):
    query = db.query(PurchaseOrderProduct).filter(
        PurchaseOrderProduct.admin_id == order.admin_id
    )

    if order.purchase_order_id:
        query = query.filter(PurchaseOrderProduct.purchase_order_id == order.purchase_order_id)

    data = query.all()

    if not data:
        return {
            "status": "false",
            "message": f"No products found for admin_id={order.admin_id} and purchase_order_id={order.purchase_order_id}"
        }

    return {
        "status": "true",
        "message": "Products retrieved successfully.",
        "data": data,
    }
