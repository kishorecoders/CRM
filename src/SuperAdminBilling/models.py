from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime

class SuperAdminBillingBase(SQLModel):
    user_add_new_id : int = Field(nullable=False,default=0)
    transection_id : str = Field(nullable=False,default=0)
    reffral_code_id : Optional[int] = Field(nullable=True,default=0)
    gst_number : Optional[str] = Field(nullable=True,default=0)
    address : Optional[str] = Field(nullable=True,default=0)
    city : Optional[str] = Field(nullable=True,default=0)
    state : Optional[str] = Field(nullable=True,default=0)
    pin_code : Optional[int] = Field(nullable=True,default=0)
    country : Optional[str] = Field(nullable=True,default=0)
    amount_of_transection : Optional[str] = Field(nullable=True,default=0)
    

class SuperAdminBilling(SuperAdminBillingBase,table = True):
    __tablename__ = "super_admin_billing"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class SuperAdminBillingCreate(SuperAdminBillingBase):
    pass

class SuperAdminBillingRead(SuperAdminBillingBase):
    id : int