from typing import List,Optional
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from .models import  GrnOrderIssueCreate , GrnOrderIssueUpdate ,GrnOrderProductGet , GrnOrderProductDelete
from .service import create_order_with_products , update ,get_all_grn_order_issue ,get_grn_order_issue_by_admin , delete_grn_order_issue_by_admin
from src.parameter import get_token

router = APIRouter()



@router.post("/create_grn_order_issue")
def create_grn_order_issue_with_products(
    request: GrnOrderIssueCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    
    return create_order_with_products(db=db, request=request)



@router.post("/updateGrnOrderIssue")
def update_purchase_order(
    request: GrnOrderIssueUpdate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):

    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    return update(db=db, request=request)



@router.post("/showAllGrnOrderIssue")
def read_all_grn_order_issue_details(
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
    ):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    else:
        return get_all_grn_order_issue(db=db)



@router.post("/showGrnOrderIssueByAdmin")
def read_grn_order_issue_by_admin(
    request:GrnOrderProductGet,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
    ):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    else:
        return get_grn_order_issue_by_admin(db=db, request = request)



@router.post("/DeleteGrnOrderIssueByAdmin")
def grn_order_issue_by_admin(
    request:GrnOrderProductDelete,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
    ):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    else:
        return delete_grn_order_issue_by_admin(db=db, request = request)





