from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime

class LateMarkBase(SQLModel):
    admin_id : Optional[str] = Field(nullable=True,default=None)
    select_type : Optional[str] = Field(nullable=True,default=None) # 1 Day, 2 Day ....6 Day
    content : Optional[str] = Field(nullable=True,default=None)
    config_id : Optional[str] = Field(nullable=True,default=None)
    type : Optional[str] = Field(nullable=True,default=None) # Shift1, Shift2, Shift3, General Shift
    amount_type : Optional[str] = Field(nullable=True,default=None) 
    amount : Optional[str] = Field(nullable=True,default=None)

class LateMark(LateMarkBase,table = True):
    __tablename__ = "late_mark"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)


class LateMarkCreate(LateMarkBase):
    pass

class LateMarkRead(BaseModel):
    admin_id : Optional[str] = None
    type : Optional[str] = None

class LateMarkDelete(BaseModel):
    admin_id : Optional[str] = None
    id : Optional[str] = None

class LetmarkUpdate(BaseModel):
    id : Optional[str] = None
    admin_id : Optional[str] = None
    select_type : Optional[str] = None # 1 Day, 2 Day ....6 Day
    content : Optional[str] = None
    config_id : Optional[str] = None
    type : Optional[str] = None # Shift1, Shift2, Shift3, General Shift
    amount_type : Optional[str] = None
    amount : Optional[str] = None

