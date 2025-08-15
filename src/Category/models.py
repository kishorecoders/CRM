from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime

class CategoryBase(SQLModel):
    admin_id : str = Field(nullable=False,default=None)
    employe_id : Optional[str] = Field(nullable=False,default=None)
    category_name : Optional[str] = Field(nullable=False,default=None)
    type : Optional[str] = Field(nullable=False,default=None)

    created_by_type : Optional[str] = Field(nullable=True,default=None)
    admin_emp_id : Optional[str] = Field(nullable=True,default=None)

    updated_by_type : Optional[str] = Field(nullable=True,default=None)
    updated_admin_emp_id : Optional[str] = Field(nullable=True,default=None)


class Category(CategoryBase,table = True):
    __tablename__ = "category"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    ccreated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class CategoryCreate(BaseModel):
    admin_id : str = None
    employe_id : Optional[str] = None
    category_name : Optional[str] = None
    type : Optional[str] = None

class CategoryRead(CategoryBase):
    id : int