from sqlmodel import SQLModel, Field, Relationship
from pydantic import UUID4
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime


class SettingBase(SQLModel):
    admin_id: str = Field(nullable=False, default=None)
    employe_id: Optional[str] = Field(nullable=False, default=None)
    company_title: Optional[str] = Field(nullable=False, default=None)
    logo: Optional[str] = Field(nullable=False, default=None)
    address: Optional[str] = Field(nullable=False, default=None)
    gst_number: Optional[str] = Field(nullable=False, default=None)
    account_holder_name: Optional[str] = Field(nullable=False, default=None)
    account_number: Optional[str] = Field(nullable=False, default=None)
    ifsc_code: Optional[str] = Field(nullable=True, default=None)
    trems_condition: Optional[str] = Field(nullable=True, default=None)
    custom_series: Optional[str] = Field(nullable=True, default=None)
    state: Optional[str] = Field(nullable=False, default=None)
    bank_name: Optional[str] = Field(nullable=True, default=None)
    branch: Optional[str] = Field(nullable=True, default=None)
    city: Optional[str] = Field(nullable=True, default=None)

    contact_number: Optional[str] = Field(nullable=True, default=None)
    email: Optional[str] = Field(nullable=True, default=None)


class Setting(SettingBase, table=True):
    __tablename__ = "settings"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)


class SettingCreate(SettingBase):
    pass


class SettingRead(SettingBase):
    id: int
