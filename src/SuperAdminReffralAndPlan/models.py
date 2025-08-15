from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime

class SuperAdminReffralAndPlanBase(SQLModel):
    name_of_reffral_plan : str = Field(nullable=False,default=0)
    cupon_code : str = Field(nullable=False,default=0)
    coupon_use_limite : int = Field(nullable=False,default=0)
    email_coupon_code_use : Optional[str] = Field(nullable=True,default=0)
    mobile_number : Optional[int] = Field(nullable=True,default=0)
    discount : str = Field(nullable=False,default=0)
    validity_of_code : str = Field(nullable=False,default=date.today())


class SuperAdminReffralAndPlan(SuperAdminReffralAndPlanBase,table = True):
    __tablename__ = "super_admin_reffral_plan"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class SuperAdminReffralAndPlanCreate(SuperAdminReffralAndPlanBase):
    pass

class SuperAdminReffralAndPlanRead(SuperAdminReffralAndPlanBase):
    id : int