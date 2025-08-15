from sqlmodel import SQLModel, Field, Relationship
from pydantic import UUID4
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime


class CreateDispatchBase(SQLModel):
    admin_id: str = Field(nullable=True, default=None)
    employee_id: str = Field(nullable=True, default=None)
    vendor_id: str = Field(nullable=True, default=None)
    product_id: str = Field(nullable=True, default=None)
    quantity: str = Field(nullable=True, default=None)
    material: str = Field(nullable=True, default=None)


class CreateDispatch(CreateDispatchBase, table=True):
    __tablename__ = "create_dispatch"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=True)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=True)


class CreateDispatchCreate(CreateDispatchBase):
    pass


class CreateDispatchRead(CreateDispatchBase):
    admin_id: int



class DispatchListRequest(BaseModel):
    admin_id: int
    employee_id: Optional[str] = None



class CreateDispatchDelete(BaseModel):
    admin_id: int
    dispatch_id: int
