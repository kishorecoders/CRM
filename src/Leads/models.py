from sqlmodel import SQLModel, Field, Relationship
from pydantic import UUID4
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime

class LeadsBase(SQLModel):
    lead_source: Optional[str] = Field(nullable=False, default=None)
    name: Optional[str] = Field(nullable=False, default=None)
    email: Optional[str] = Field(nullable=False, default=None)
    contact_details: Optional[str] = Field(nullable=False, default=None)
    address: Optional[str] = Field(nullable=False, default=None)
    discription: Optional[str] = Field(nullable=False, default=None)
    business_name: Optional[str] = Field(nullable=False, default=None)

class Leads(LeadsBase, table=True):
    __tablename__ = "leads"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: Optional[datetime] = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: Optional[datetime] = Field(default_factory=get_current_datetime, nullable=False)

class LeadsCreate(LeadsBase):
    pass

class LeadsRead(LeadsBase):
    id: int