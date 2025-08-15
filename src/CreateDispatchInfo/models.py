from sqlmodel import SQLModel, Field, Relationship
from pydantic import UUID4
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime

class DispatchInfoBase(SQLModel):
    admin_id: str = Field(nullable=False, default=None)
    employee_id: Optional[str] = Field(nullable=True, default=None)
    challan_id: Optional[str] = Field(nullable=True, default=None)
    challan_date: Optional[str] = Field(nullable=True, default=None)
    eway_bill_no: Optional[str] = Field(nullable=True,default=None)
    product_count: Optional[int] = Field(nullable=True,default=None)
    customer_po_no: Optional[str] = Field(nullable=True,default=None)
    so_number: Optional[str] = Field(nullable=True,default=None)
    driver_no: Optional[str] = Field(nullable=True,default=None)
    vehicle_no: Optional[str] = Field(nullable=True,default=None)
    authorized_image: Optional[str] = Field(nullable=True,default=None)
    dispatch_image: Optional[str] = Field(nullable=True,default=None) 
    inventryoutword_id: Optional[str] = Field(nullable=True,default=None) 
    product_id: Optional[str] = Field(nullable=True,default=None) 
    order_id :  Optional[str] = Field(nullable=True,default=None) 

class DispatchInfo(DispatchInfoBase, table=True):
    __tablename__ = "dispatch_info"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)


class DispatchInfoCreate(BaseModel):
    admin_id: str = None
    employee_id: Optional[str] = None
    challan_date: Optional[str] = None
    eway_bill_no: Optional[str] = None
    product_count: Optional[int] = None
    customer_po_no: Optional[str] = None
    so_number: Optional[str] = None
    driver_no: Optional[str] = None
    vehicle_no: Optional[str] = None
    authorized_image: Optional[str] = None
    dispatch_image: Optional[str] = None
    order_id: Optional[str] = None




class DispatchListRequest(BaseModel):
    admin_id: int
    employee_id: Optional[str] = None

