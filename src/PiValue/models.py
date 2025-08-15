from sqlmodel import SQLModel, Field, Relationship
from pydantic import UUID4
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime

class PiValueBase(SQLModel):
    id: int = Field(nullable=False, default=None)
    rate: str = Field(nullable=False, default=None)
    taxable_value: str = Field(nullable=False, default=None)
    billing_percent: str = Field(nullable=False, default=None)
    cash_percent: str = Field(nullable=False, default=None)
    billing_amount: str = Field(nullable=False, default=None)
    cash_amount: str = Field(nullable=False, default=None)
    gst: str = Field(nullable=False, default=None)


class PiValue(PiValueBase, table=True):
    __tablename__ = "pi_value"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class PiValueCreate(PiValueBase):
    pass


