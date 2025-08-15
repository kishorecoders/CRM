from typing import List,Optional
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from .models import PurchaseOrderProduct , PurchaseOrderProductRead
from .service import get
from src.parameter import get_token

router = APIRouter()

@router.post("/showPurchaseOrderProduct")
def read_all_purchase_order_issue_details(
     order : PurchaseOrderProductRead,
     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get(db=db , order = order)
        




        