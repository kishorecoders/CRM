from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime

class CheckPointBase(SQLModel):
    admin_id : Optional[str] = Field(nullable=False,default=None)
    emp_id: Optional[str] = Field(nullable=False ,default=None)
    subproduct_id :Optional[str] = Field(nullable=False,default=None)
    stage_id : Optional[str]= Field(nullable=False,default=None)
    check_point_name : Optional[str]= Field(nullable=False,default=None)
    check_point_status : Optional[int]= Field(nullable=False,default=0)

class CheckPoint(CheckPointBase,table = True):
    __tablename__ = "CheckPoint"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)


class CheckPointItem(BaseModel):
    check_point_name: str
    check_point_status: int

class CheckPointCreate(BaseModel):
    admin_id: str
    emp_id: str
    subproduct_id: str
    stage_id: str
    CheckPoints: List[CheckPointItem]

class CheckPointRead(BaseModel):
    subproduct_id : str
    stage_id : str

class CheckPointDeletee(BaseModel):
    checkPoint_id: int


class CheckPointUpdate(BaseModel):
    admin_id: str
    emp_id: str
    checkPoint_id: int
    subproduct_id: str
    stage_id: str
    CheckPoints: List[CheckPointItem]