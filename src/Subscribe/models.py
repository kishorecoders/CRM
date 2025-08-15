from sqlmodel import SQLModel, Field, Relationship
from pydantic import UUID4
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime,LargeBinary
from src.parameter import get_current_datetime
from sqlmodel import Field, SQLModel, Column
from sqlalchemy import Text

class SubscribeBase(SQLModel):
    admin_id: Optional[str] = Field(nullable=True, default=None)
    employee_id: Optional[str] = Field(nullable=True, default=None)
    first_name: Optional[str] = Field(nullable=True, default=None)
    last_name: Optional[str] = Field(nullable=True, default=None)
    email: Optional[str] = Field(nullable=True, default=None)
    phone: Optional[str] = Field(nullable=True, default=None)
    plan_type: Optional[str] = Field(nullable=True, default=None)
    privacy: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)
    )



class Subscribe(SubscribeBase, table=True):
    __tablename__ = "subscribe"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)


class SubscribeCreate(BaseModel):
    employee_id: Optional[str] = None
    admin_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    plan_type: Optional[str] = None
    privacy: Optional[str] = None

class FetchSubscribeRequest(BaseModel):
    admin_id: Optional[str] = None
    employee_id: Optional[str] = None



class SendOtpRequest(BaseModel):
    phone_number: Optional[str] = None

class VerifyOtpRequest(BaseModel):
    employee_id: Optional[str] = None
    admin_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    plan_type: Optional[str] = None
    privacy: Optional[str] = None
    otp: Optional[str] = None