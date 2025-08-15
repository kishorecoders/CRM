from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime
from sqlalchemy import Column, DateTime, Text , BigInteger

class SuperAdminPlanAndPriceBase(SQLModel):
    name_of_the_subscription : str = Field(nullable=False,default=0)

    discription: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=False)  
    )    

    one_month_normal_price : float = Field(nullable=False,default=0)
    one_month_gst_amount : float = Field(nullable=False,default=0)
    one_month_price : float = Field(nullable=False,default=0)
    three_month_normal_price : float = Field(nullable=False,default=0) 
    three_month_gst_amount : float = Field(nullable=False,default=0)
    three_month_price : float = Field(nullable=False,default=0)
    twelve_month_normal_price : float = Field(nullable=False,default=0)
    twelve_month_gst_amount : float = Field(nullable=False,default=0) 
    twelve_month_price : float = Field(nullable=False,default=0)
    admin : bool = Field(nullable=False,default=0)
    sales : bool = Field(nullable=False,default=0)
    project_manager : bool = Field(nullable=False,default=0) 
    store_engineer : bool = Field(nullable=False,default=0)
    purchase : bool = Field(nullable=False,default=0)
    dispatch : bool = Field(nullable=False,default=0)
    account : bool = Field(nullable=False,default=0) 
    customer : bool = Field(nullable=False,default=0)
    status : Optional[str] = Field(nullable=True,default='Activate')
    total_access : int = Field(nullable=False,default=0)
    status_update : bool = Field(nullable=False,default=0)
    employee_sales : bool = Field(nullable=True,default=0) 
    employee_attendance :  bool = Field(nullable=True,default=0) 
    employee_leave :  bool = Field(nullable=True,default=0) 
    employee_task :  bool = Field(nullable=True,default=0) 
    plan_type : Optional[str] = Field(nullable=True,default=None)


class SuperAdminPlanAndPrice(SuperAdminPlanAndPriceBase,table = True):
    __tablename__ = "super_admin_subscription_plan_price"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class SuperAdminPlanAndPriceCreate(SuperAdminPlanAndPriceBase):
    pass

class SuperAdminPlanAndPriceRead(SuperAdminPlanAndPriceBase):
    id : int