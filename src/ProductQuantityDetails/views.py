from typing import List,Optional
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from src.ProductQuantityDetails.models import ProductQuantityRead
from src.ProductQuantityDetails.service import get_filtered_products_details
from src.parameter import get_token
from datetime import datetime

router = APIRouter()

@router.post("/get_ProductQuantity")
def get_products_list(
    qtydetails: ProductQuantityRead,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db) 
):
    if auth_token != get_token():
        raise HTTPException(
            status_code=401, 
            detail="Unauthorized Request"
        )
    
    return get_filtered_products_details(db = db ,qtydetails = qtydetails)
