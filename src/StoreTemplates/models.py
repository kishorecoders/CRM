from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime
import json

class StoreTemplateBase(SQLModel):
    admin_id : Optional[str] = Field(nullable=True,default=None)
    emp_id: Optional[str] = Field(nullable=True ,default=None)
    product_id :Optional[str] = Field(nullable=True,default=None)
    template_name : Optional[str]= Field(nullable=True,default=None)
    production_id : Optional[str]= Field(nullable=True,default=None)

class StoreTemplate(StoreTemplateBase,table = True):
    __tablename__ = "store_templates"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

