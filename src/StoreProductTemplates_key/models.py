from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime
import json

class StoreProductTemplateKeyBase(SQLModel):
    admin_id : Optional[str] = Field(nullable=True,default=None)
    emp_id: Optional[str] = Field(nullable=True ,default=None)
    template_id :Optional[str] = Field(nullable=True,default=None)
    temp_key_name :Optional[str] = Field(nullable=True,default=None)
    temp_value : Optional[str]= Field(nullable=True,default=None)


class StoreProductTemplateKey(StoreProductTemplateKeyBase,table = True):
    __tablename__ = "store_product_templates_key"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

