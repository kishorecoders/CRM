from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime
from sqlalchemy import Column, DateTime, Text , BigInteger



class PurchaseOrderProductBase(SQLModel):
    admin_id : str = Field(nullable=False,default=None)
    employee_id: Optional[str] = Field(nullable=False)
    order_id : str = Field(nullable=False,default=None)
    purchase_order_id : Optional[str] = Field(nullable=True,default=None)
    product_name: Optional[str] = Field(nullable=False)
    product_code: Optional[str] = Field(nullable=False)
    hsn_code: Optional[str] = Field(nullable=False)
    rate_per_unit: Optional[float] = Field(nullable=False)
    quantity: Optional[int] = Field(nullable=False)
    total: Optional[float] = Field(nullable=False)
    gst_percentage: Optional[float] = Field(nullable=False)
    gross_total: Optional[float] = Field(nullable=False)
    availability: Optional[str] = Field(nullable=False)
    status: str = Field(nullable=True,default=None)
    discount_type: Optional[str] = Field(nullable=True,default=None)
    discount_amount: Optional[str] = Field(nullable=True,default=None)
    discount_percent: Optional[str] = Field(nullable=True,default=None)
    unit : Optional[str] = Field(nullable=True,default=None)
    prev_accept : Optional[str] = Field(nullable=True,default=0)
    prev_received : Optional[str] = Field(nullable=True,default=0)

    discription: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )    

    cgst : Optional[str] = Field(nullable=True,default=None)
    sgst : Optional[str] = Field(nullable=True,default=None)
    type : Optional[str] =  Field(nullable=True,default=None)
    




    
class PurchaseOrderProduct(PurchaseOrderProductBase,table = True):
    __tablename__ = "purchase_order_product"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

    
class PurchaseOrderProductRead(BaseModel):
    admin_id : Optional[str]  = None
    purchase_order_id : Optional[str]  = None
    