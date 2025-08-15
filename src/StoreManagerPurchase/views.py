from typing import List,Optional
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from src.StoreManagerPurchase.models import StoreManagerPurchase,StoreManagerPurchaseCreate,RequestStatusUpdate ,StoreManagerPurchaseUpdate , StoreManagerPurchaseDelete
from .service import create,get_all_store_manger_purcahse,get_store_manger_purcahse_by_admin_id,update,delete_store_manger_purcahse_by_id,update_request_status,create_multiple
from src.parameter import get_token

router = APIRouter()

@router.get("/showallstorepurchase")
def read_all_store_manger_purcahse_details(auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_all_store_manger_purcahse(db=db)
        
@router.post("/createstorepurchase")
def create_purchase_order_issue_details(store_manger_purcahse_create: StoreManagerPurchaseCreate,
                auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return create(db=db, store_manger_purcahse_create=store_manger_purcahse_create)    

@router.post("/createmultiplestorepurchase")
def create_purchase_order_issue_details(
    store_manger_purcahse_create: list[StoreManagerPurchaseCreate],
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    else:
        return create_multiple(db=db, store_manger_purcahse_create_list=store_manger_purcahse_create)



@router.get("/showstorepurchase/{admin_id}")
def read_store_manger_purcahse_byadmin__id(admin_id: str, search: Optional[str] = None, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_store_manger_purcahse_by_admin_id(db=db, admin_id=admin_id, search=search)
     



@router.post("/updatestorepurchase/")
def update_store_manager_purchase_details(
    store_manager_purchase: StoreManagerPurchaseUpdate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    # Check token validity
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    
    # Validate presence of store_purchase_id
    if not store_manager_purchase.store_purchase_id:
        raise HTTPException(status_code=400, detail="store_purchase_id is required")
    
    # Prepare update data
    store_manager_purchase_update = store_manager_purchase.dict(exclude_unset=True)
    store_purchase_id = store_manager_purchase.store_purchase_id
    update_data = {k: v for k, v in store_manager_purchase_update.items() if k != "store_purchase_id"}

    query = db.query(StoreManagerPurchase).filter(StoreManagerPurchase.id == store_purchase_id)
    if query.first() is None:
        raise HTTPException(status_code=404, detail="Store Purchase ID not found")
    
    query.update(update_data)
    db.commit()

    return {
        "status": "true",
        "message": "Store Manager Purchase Details Updated Successfully",
        "data": update_data
    }

@router.post("/deletestorepurchase/")
def delete_store_manger_purcahse(
     request: StoreManagerPurchaseDelete, 
     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), 
     db: Session = Depends(get_db)
):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return delete_store_manger_purcahse_by_id(store_purchase_id=request.store_manager_purchase_id, db=db)
            
            
@router.put("/updateRequestStatus/{store_manager_purchase_id}")
def update_request_status_route(
    store_manager_purchase_id: int,
    request_data: RequestStatusUpdate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    else:
        return update_request_status(store_manager_purchase_id=store_manager_purchase_id, request_data=request_data, db=db)        