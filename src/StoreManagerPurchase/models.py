from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime

class StoreManagerPurchaseBase(SQLModel):
    admin_id : str = Field(nullable=False,default=None)
    employe_id : Optional[str] = Field(nullable=False,default=None)
    request_date : Optional[date] = Field(nullable=False,default=date.today())
    product_id : Optional[str] = Field(nullable=False,default=None)
    request_purchase_quntity : Optional[str] = Field(nullable=False,default=None)
    request_id : Optional[str] = Field(nullable=False,default=None)
    request_status : Optional[str] = Field(nullable=False,default=None)

    created_by_type : Optional[str] = Field(nullable=True,default=None)
    admin_emp_id : Optional[str] = Field(nullable=True,default=None)

    updated_by_type : Optional[str] = Field(nullable=True,default=None)
    updated_admin_emp_id : Optional[str] = Field(nullable=True,default=None)

    procure_status : Optional[str] = Field(nullable=True,default="0")
    rfq_create : Optional[str] = Field(nullable=True,default="0")
    
    product_manager_id : Optional[str] = Field(nullable=True,default=None)
    
    request_type : Optional[str] = Field(nullable=True,default=None)


class StoreManagerPurchase(StoreManagerPurchaseBase,table = True):
    __tablename__ = "store_manager_purchase"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class StoreManagerPurchaseCreate(BaseModel):
    admin_id : str = None
    employe_id : Optional[str] = None
    request_date : Optional[date] = None
    product_id : Optional[str] = None
    request_purchase_quntity : Optional[str] = None
    request_id : Optional[str] = None
    request_status : Optional[str] = None
    procure_status : Optional[str] = None
    product_manager_id : Optional[str] = None
    request_type : Optional[str] = None
    product_manager_type : Optional[str] = None

class StoreManagerPurchaseUpdate(BaseModel):
    store_purchase_id: Optional[int] = None    
    request_purchase_quntity: Optional[str] = None    

# class StoreManagerPurchaseUpdate(BaseModel):
#     admin_id: Optional[int] = None    
#     employe_id: Optional[str] = None    
#     request_date: Optional[str] = date.today()    
#     product_id: Optional[str] = None    
#     store_purchase_id: Optional[int] = None    
#     request_purchase_quntity: Optional[str] = None    
#     request_id: Optional[str] = None   


class StoreManagerPurchaseRead(StoreManagerPurchaseBase):
    id : int
    
class RequestStatusUpdate(SQLModel):
    admin_id : str = None
    employe_id : Optional[str] = None
    request_status: Optional[str] = None    
    
class StoreManagerPurchaseDelete(BaseModel):
    store_manager_purchase_id: Optional[int] = None   