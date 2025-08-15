from sqlmodel import SQLModel, Field, Relationship
from pydantic import UUID4
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime


class DesignHandoverBase(SQLModel):
    admin_id: str = Field(nullable=True, default=None)
    employee_id: str = Field(nullable=True, default=None)
    product_id: str = Field(nullable=True, default=None)
    order_id: str = Field(nullable=True, default=None)
    date_time: str = Field(nullable=True, default=None)
    file: str = Field(nullable=False, default=None)
    type: str = Field(nullable=False, default=None)
   



class DesignHandover(DesignHandoverBase, table=True):
    __tablename__ = "design_handover"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=True)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=True)


class DesignHandoverCreate(DesignHandoverBase):
    pass


class DesignHandoverRead(DesignHandoverBase):
    admin_id: int
    employee_id: Optional[str] = None



class DeleteDesignHandoverRequest(BaseModel):
    admin_id: int
    design_handover_id: int
    employee_id: Optional[int] = None



