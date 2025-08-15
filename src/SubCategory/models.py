from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime

class SubCategoryBase(SQLModel):
    admin_id : str = Field(nullable=False,default=None)
    employe_id : Optional[str] = Field(nullable=False,default=None)
    category_id : Optional[int] = Field(nullable=False,default=None)
    sub_category_name : Optional[str] = Field(nullable=False,default=None)

class SubCategory(SubCategoryBase,table = True):
    __tablename__ = "subcategory"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class SubCategoryCreate(SubCategoryBase):
    pass

class SubCategoryRead(SubCategoryBase):
    id : int