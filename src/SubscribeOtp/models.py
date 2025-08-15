from sqlmodel import SQLModel, Field, Relationship
from pydantic import UUID4
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime,LargeBinary
from src.parameter import get_current_datetime
from sqlmodel import Field, SQLModel, Column
from sqlalchemy import Text

class OTPStoreBase(SQLModel):
    phone_number: Optional[str] = Field(nullable=False, default=None)
    otp: Optional[str] = Field(nullable=False, default=None)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class OTPStore(OTPStoreBase, table=True):
    __tablename__ = "otp_store"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

