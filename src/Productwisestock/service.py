from .models import ProductWiseStock,ProductWiseStockCreate
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status,HTTPException

def get_all_product_wise_stock(db: Session):
    data = db.query(ProductWiseStock).order_by(ProductWiseStock.id.desc()).all()
    response = {'status': 'true', 'message': "Data Received Successfully", 'data': data}
    return response

def get_product_wise_stock_by_admin(db: Session, admin_id: str):
    data = db.query(ProductWiseStock).filter(ProductWiseStock.admin_id == admin_id).all()
    response = {'status': 'true', 'message': "Data Received Successfully", 'data': data}
    return response

# def create(db: Session, product_wise_stock_create: ProductWiseStockCreate):
#     db_product_wise_stock_create = ProductWiseStock(**product_wise_stock_create.dict())
#     db.add(db_product_wise_stock_create)
#     db.commit()
#     db.refresh(db_product_wise_stock_create)
#     response = {'status': 'true','message':"Product Wise Stock Details Added Successfully",'data':db_product_wise_stock_create}
#     return response

def create(db: Session, product_wise_stock_create: ProductWiseStockCreate):
    
    existing_entry = db.query(ProductWiseStock).filter(
        ProductWiseStock.admin_id == product_wise_stock_create.admin_id,
        ProductWiseStock.product_id == product_wise_stock_create.product_id
    ).first()

    if existing_entry:
        
        existing_entry.total_quantity += product_wise_stock_create.total_quantity
        db.commit()
        db.refresh(existing_entry)
        response = {'status': 'true', 'message': "Product Wise Stock Details Updated Successfully", 'data': existing_entry}
    else:
        
        db_product_wise_stock_create = ProductWiseStock(**product_wise_stock_create.dict())
        db.add(db_product_wise_stock_create)
        db.commit()
        db.refresh(db_product_wise_stock_create)
        response = {'status': 'true', 'message': "Product Wise Stock Details Added Successfully", 'data': db_product_wise_stock_create}

    return response
   
def update(purchase_order_issue_id:int, product_wise_stock:ProductWiseStock,db:Session):
    product_wise_stock_update = product_wise_stock.dict(exclude_unset=True)
    db.query(ProductWiseStock).filter(ProductWiseStock.id == purchase_order_issue_id).update(product_wise_stock_update)
    db.commit()
    response = {'status': 'true','message':"Product Wise Stock Details Updated Successfully",'data':product_wise_stock_update}
    return response

def delete_product_wise_stock_by_id(product_wise_stock_id: int, db: Session):
    product_wise_stock_details = db.query(ProductWiseStock).filter(ProductWiseStock.id == product_wise_stock_id).first()
    if product_wise_stock_details:
        db.delete(product_wise_stock_details)
        db.commit()
        return {'status':'true', 'message':"Product Wise Stock Details deleted successfully", 'data':product_wise_stock_details}
    return {"status":'false',  'message':"Product Wise Stock not found"}