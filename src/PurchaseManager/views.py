from typing import List
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from .models import PurchaseMangerCreate,PurchaseManger
from .service import create,get_all_purcahse_manager,update,get_purcahse_manager_by_admin_id,delete_purcahse_manager_by_id,get_purcahse_manager_by_request,get_purchase_manager_by_request_ids
from src.parameter import get_token

router = APIRouter()

@router.get("/showallPurchaseManager")
def read_all_purcahse_manager_details(auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_all_purcahse_manager(db=db)
        
@router.post("/createPurchaseManager")
def create_purcahse_manager_details(purchase_manager_create: PurchaseMangerCreate,
                auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return create(db=db, purchase_manager_create=purchase_manager_create)    

@router.get("/showPurchaseManager/{admin_id}")
def read_purcahse_manager_byadmin__id(admin_id: str, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_purcahse_manager_by_admin_id(admin_id=admin_id, db=db)
        
@router.get("/showPurchaseManagerbyRequest/{admin_id}/{request_id}")
def read_purcahse_manager_by_request(admin_id: str, request_id: str,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_purcahse_manager_by_request(admin_id=admin_id, request_id=request_id, db=db)
        
@router.get("/showPurchaseManagerbyRequestIds/{admin_id}")
def read_purchase_manager_by_request_ids(admin_id: str, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_purchase_manager_by_request_ids(admin_id=admin_id, db=db)        
     
@router.put("/updatePurchaseManager/{purchase_manager_id}")
def update_purcahse_manager_details(purchase_manager_id:int,purchase_manager:PurchaseMangerCreate,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db:Session=Depends(get_db)):
       def inner_get_plan(auth_token: str):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return update(purchase_manager_id=purchase_manager_id,purchase_manager=purchase_manager,db=db)
    
       return inner_get_plan(auth_token)

@router.delete("/deletePurchaseManager/{purchase_manager_id}")
def delete_purcahse_manager_by_id(purchase_manager_id: int, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return delete_purcahse_manager_by_id(purchase_manager_id=purchase_manager_id, db=db)