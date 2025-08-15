from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime

from sqlalchemy import Column, DateTime, Text , BigInteger
from sqlmodel import SQLModel, Field, Column, JSON

class ActivityCenterBase(SQLModel):
    admin_sales_id : int = Field(nullable=False,default=0)
    employe_id : str = Field(nullable=False,default=0)
    #activiity_message : str = Field(nullable=False,default=0)

    activiity_message: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )

    type : Optional[str] = Field(nullable=True,default=0)
    activity_docs : Optional[str] = Field(nullable=True,default=None)
    quot_send : Optional[str] = Field(nullable=True,default=None)
    latitude: Optional[float] = Field(nullable=True, default=None)
    longitude: Optional[float] = Field(nullable=True, default=None)
    created_by_type : Optional[str] = Field(nullable=True,default=None)
    admin_emp_id : Optional[str] = Field(nullable=True,default=None)
    meeting_link : Optional[str] = Field(nullable=True,default=None)

class ActivityCenter(ActivityCenterBase,table = True):
    __tablename__ = "activity_center"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class ActivityCenterCreate(ActivityCenterBase):
    pass

class ActivityCenterRead(ActivityCenterBase):
    id : int


class DashboardOverview(BaseModel):
    admin_id : int
    emp_id: Optional[str] = None
    from_date: Optional[str] = None 
    to_date: Optional[str] = None
    
class SalesDashboardOverview(BaseModel):
    admin_id : int
    allocated_emplyee_id: Optional[str]