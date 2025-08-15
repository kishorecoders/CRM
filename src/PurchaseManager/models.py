from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime

class PurchaseMangerBase(SQLModel):
    admin_id : str = Field(nullable=False,default=None)
    employe_id : Optional[str] = Field(nullable=False,default=None)
    store_manager_order_id : Optional[str] = Field(nullable=False,default=None)
    request_id : Optional[str] = Field(nullable=False,default=None)
    product_id : Optional[str] = Field(nullable=False,default=None)
    request_purchase_quntity : Optional[str] = Field(nullable=False,default=None)
    take_action : Optional[str] = Field(nullable=False,default=None)

class PurchaseManger(PurchaseMangerBase,table = True):
    __tablename__ = "purchase_manager"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class PurchaseMangerCreate(PurchaseMangerBase):
    pass

class PurchaseMangerRead(PurchaseMangerBase):
    id : int