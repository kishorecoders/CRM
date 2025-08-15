from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime


class GrnOrderProductBase(SQLModel):
    admin_id : Optional[str] = Field(nullable=True,default=None)
    employee_id: Optional[str] = Field(nullable=True,default=None)
    grn_order_id : Optional[str] = Field(nullable=True,default=None)
    product_id : Optional[str] = Field(nullable=True,default=None)
    recived_quantity: Optional[str] = Field(nullable=True,default=None)
    accepted_quantity: Optional[str] = Field(nullable=True,default=None)
    reject_quantity: Optional[str] = Field(nullable=True,default=None)
    remark: Optional[str] = Field(nullable=True,default=None)
    
    
    accepted_qty_by_invoice: Optional[str] = Field(nullable=True,default=None)
    rate: Optional[str] = Field(nullable=True,default=None)
    amount: Optional[str] = Field(nullable=True,default=None)
    
    
    created_by_type : Optional[str] = Field(nullable=True,default=None)
    admin_emp_id : Optional[str] = Field(nullable=True,default=None)
    
    updated_by_type : Optional[str] = Field(nullable=True,default=None)
    updated_admin_emp_id : Optional[str] = Field(nullable=True,default=None)
    used_quantity : Optional[str] = Field(nullable=True,default=None)

class GrnOrderProduct(GrnOrderProductBase,table = True):
    __tablename__ = "grn_order_product"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

    
class GrnOrderProductRead(BaseModel):
    admin_id : Optional[str]  = None
    employee_id : Optional[str]  = None
    grn_order_id : Optional[str]  = None
    
    
    
    
    
class GrnOrderRemarkUpdateRequest(BaseModel):
    id: int
    admin_id: Optional[str]
    employee_id: Optional[str]
    remark: str
    
class GrnOrderProductusedQty(BaseModel):
    admin_id: Optional[str] = None
    product_id: Optional[str] = None

class UpdateGrnOrderProductusedQty(BaseModel):
    admin_id: Optional[str] = None
    grn_product_id: Optional[str] = None
    type: Optional[str] = None


    