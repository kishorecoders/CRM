from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime
from sqlalchemy import Column, DateTime, Text , BigInteger

class NotificationBase(SQLModel):
    admin_id : Optional[str] = Field(nullable=True,default=None)
    title: Optional[str] = Field(default=None, nullable=True)
    description: Optional[str] = Field(default=None, nullable=True)
    type : Optional[str] = Field(nullable=True,default=None)
    object_id : Optional[str] = Field(nullable=True,default=None)
    created_by_id: Optional[str] = Field(default=None,nullable=True)  # either admin or employee
    created_by_type: Optional[str] = Field(default=None,nullable=True)  # "admin" or "employee"

class Notification(NotificationBase,table = True):
    __tablename__ = "notification"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class NotificationRead(BaseModel):
    admin_id: Optional[str] = None
    user_type: Optional[str] = None  # "admin" or "employee"
    user_id: Optional[str] = None  # ID of the user who read the notification