from sqlmodel import SQLModel, Field, Relationship
from pydantic import UUID4
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime






class ProductDispatchBase(SQLModel):
    account_id: int = Field(nullable=True, default=None)
    admin_id: int = Field(nullable=False)
    emp_id: Optional[int] = Field(default=None,nullable=True)
    dc_no: str = Field(nullable=False)
    dc_qty: str = Field(nullable=False)
    dispatch_qty: str = Field(nullable=False)
    balance_qty: str = Field(nullable=False)
    product_id: str = Field(nullable=False)
    


class ProductDispatch(ProductDispatchBase, table=True):
    __tablename__ = "product_dispatch"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)





# ? Request Model
class EditDispatchRequest(BaseModel):
    dispatch_id: int
    account_id: str
    admin_id: str
    emp_id: str
    dc_no: str
    dc_qty: str
    dispatch_qty: str
    balance_qty: str
    product_id: str

# ? Request Model
class DeleteDispatch(BaseModel):
    dispatch_id: int
