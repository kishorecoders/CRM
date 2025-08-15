from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime

class StoreCheckPointBase(SQLModel):
    admin_id : Optional[str] = Field(nullable=True,default=None)
    emp_id: Optional[str] = Field(nullable=True ,default=None)
    subproduct_id :Optional[str] = Field(nullable=True,default=None)
    stage_id : Optional[str]= Field(nullable=True,default=None)
    check_point_name : Optional[str]= Field(nullable=True,default=None)
    check_point_status : Optional[int]= Field(nullable=True,default=0)
    production_id : Optional[str]= Field(nullable=True,default=None)
    production_id : Optional[str]= Field(nullable=True,default=None)


    check_remark: Optional[str] = Field(nullable=True,default=None)
    check_remark_date: Optional[datetime] = Field(nullable=True,default=None)
    check_emp_id: Optional[str] = Field(nullable=True,default=None)
    check_admin_id: Optional[str] = Field(nullable=True,default=None)
    check_status: Optional[int] = Field(nullable=True,default=0)



class StoreCheckPoint(StoreCheckPointBase,table = True):
    __tablename__ = "StoreCheckPoint"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

    
    created_by_type : Optional[str] = Field(nullable=True,default=None)
    admin_emp_id : Optional[str] = Field(nullable=True,default=None)
    created_by_date: Optional[datetime] = Field(nullable=True,default=None)

    updated_by_type : Optional[str] = Field(nullable=True,default=None)
    updated_admin_emp_id : Optional[str] = Field(nullable=True,default=None)
    updated_by_date: Optional[datetime] = Field(nullable=True,default=None)






class CheckPointUpdate(BaseModel):
    checkPoint_id: int
    admin_id: str
    check_point_name: str
    check_point_status: str

