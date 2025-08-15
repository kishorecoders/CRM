from sqlmodel import SQLModel, Field, Relationship
from pydantic import UUID4
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime

class IntegrationBase(SQLModel):
    admin_id: Optional[str] = Field(nullable=False, default=None)
    name: Optional[str] = Field(nullable=False, default=None)
    configure: Optional[str] = Field(nullable=False, default=None)
    status: Optional[str] = Field(nullable=False, default=None)
    configure_url: Optional[str] = Field(nullable=False, default=None)

class Integration(IntegrationBase, table=True):
    __tablename__ = "integration"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: Optional[datetime] = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: Optional[datetime] = Field(default_factory=get_current_datetime, nullable=False)

class IntegrationCreate(IntegrationBase):
    pass

class IntegrationRead(IntegrationBase):
    id: int