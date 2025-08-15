from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime
from sqlalchemy import Column, DateTime, Text , BigInteger


class NotificationReadStatusBase(SQLModel):
    notification_id: Optional[str] = Field(default=None, nullable=True)
    employee_id: Optional[str] = Field(default=None , nullable=True)  # Employee who read it
    admin_id: Optional[str] = Field(default=None, nullable=True)  # Admin who read it
    is_read: Optional[bool] = Field(default=True, nullable=True)

class NotificationReadStatus(NotificationReadStatusBase,table = True):
    __tablename__ = "notification_read_status"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)


