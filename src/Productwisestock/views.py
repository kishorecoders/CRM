from typing import List
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from .models import  ProductWiseStockCreate,ProductWiseStock
from .service import create,delete_product_wise_stock_by_id,get_all_product_wise_stock,get_product_wise_stock_by_admin,update
from src.parameter import get_token

router = APIRouter()

@router.get("/showAllProductWiseStock")
def read_all_product_wise_stock_details(auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_all_product_wise_stock(db=db)
        
@router.get("/showProductWiseStockByAdmin/{admin_id}")
def read_product_wise_stock_by_admin(admin_id:str,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_product_wise_stock_by_admin(db=db, admin_id=admin_id)

@router.post("/createProductWiseStock")
def create_product_wise_stock_details(product_wise_stock_create: ProductWiseStockCreate,
                auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return create(db=db, product_wise_stock_create=product_wise_stock_create)
     
@router.put("/updateProductWiseStock/{product_wise_stock_id}")
def update_product_wise_stock_details(product_wise_stock_id:int,product_wise_stock:ProductWiseStockCreate,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db:Session=Depends(get_db)):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return update(product_wise_stock_id=product_wise_stock_id,product_wise_stock=product_wise_stock,db=db)

@router.delete("/deleteProductWiseStock/{product_wise_stock_id}")
def delete_product_wise_stock_by_id(product_wise_stock_id: int, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
            if auth_token != get_token():
                return {"status": "false", "message": "Unauthorized Request"}
            else:
                return delete_product_wise_stock_by_id(product_wise_stock_id=product_wise_stock_id, db=db)