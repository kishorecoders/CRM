from typing import List,Optional
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from .models import  PurchaseOrderIssueCreate,PurchaseOrderIssue,PurchaseOrderIssueLastStatusUpdate,PurchaseOrderIssueRequest
from .service import delete_purchase_order_issue_by_id,create_order_with_products,get_all_purchase_order_issue,get_purchase_order_issue_by_admin,update,show_all_count,get_purchase_order_issue_history_by_admin,update_status
from src.parameter import get_token

router = APIRouter()

@router.get("/showAllPurchaseOrderIssue")
def read_all_purchase_order_issue_details(auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_all_purchase_order_issue(db=db)
        
@router.get("/showPurchaseOrderIssueByAdmin/{admin_id}")
def read_purchase_order_issue_by_admin(admin_id:str,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_purchase_order_issue_by_admin(db=db, admin_id=admin_id)
        
@router.get("/showPurchaseOrderIssueHistoryByAdmin/{admin_id}")
def read_purchase_order_issue_history_by_admin(admin_id:str,order_id: Optional[str] = None, search: Optional[str] = None, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_purchase_order_issue_history_by_admin(db=db, admin_id=admin_id, search=search , order_id = order_id)  






# @router.post("/createPurchaseOrderIssue")
# def create_purchase_order_issue_details(purchase_oreder_issue_create: PurchaseOrderIssueCreate,
#                 auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#                 db: Session = Depends(get_db)):
#         if auth_token != get_token():
#             return {"status": "false", "message": "Unauthorized Request"}
#         else:
#             return create(db=db, purchase_oreder_issue_create=purchase_oreder_issue_create)
     
@router.post("/create_purchase_order_issue")
def create_purchase_order_issue_with_products(
    request: PurchaseOrderIssueRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    
    return create_order_with_products(db=db, request=request)



@router.put("/updatePurchaseOrderIssue/{purchase_order_issue_id}")
def update_purchase_order(
    purchase_order_issue_id: int,
    request: PurchaseOrderIssueRequest,
    db: Session = Depends(get_db)
):
    return update(purchase_order_issue_id, db, request)




# @router.delete("/deletePurchaseOrderIssue/{id}")
# def delete_purchase_order_issue_by_id(id: int, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
#             if auth_token != get_token():
#                 return {"status": "false", "message": "Unauthorized Request"}
#             else:
#                 return delete_purchase_order_issue_by_id(id=id, db=db)

   
            
@router.get("/PurchaseManagerDeshbordCount/{admin_id}")
def read_all_deshbord_count_details(admin_id: str, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db: Session = Depends(get_db)):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return show_all_count(db=db, admin_id=admin_id)
            
@router.put("/updateLastStatus/{purchase_order_issue_id}")
def update_status_route(
    purchase_order_issue_id: int,
    request_data: PurchaseOrderIssueLastStatusUpdate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    else:
        return update_status(purchase_order_issue_id=purchase_order_issue_id, request_data=request_data, db=db)            
            
@router.delete("/deletePurchaseOrderIssue/{id}")
def delete_purchase_order_issue(id: int, db: Session = Depends(get_db)):
    return delete_purchase_order_issue_by_id(id=id, db=db)           