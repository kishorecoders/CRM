from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime
import json

class ProductTemplateKeyBase(SQLModel):
    admin_id : Optional[str] = Field(nullable=True,default=None)
    emp_id: Optional[str] = Field(nullable=True ,default=None)
    template_id :Optional[str] = Field(nullable=True,default=None)
    temp_key_name :Optional[str] = Field(nullable=True,default=None)
    temp_value : Optional[str]= Field(nullable=True,default=None)


class ProductTemplateKey(ProductTemplateKeyBase,table = True):
    __tablename__ = "product_templates_key"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

 
class ProductTemplateKeyCreate(BaseModel):
    admin_id : Optional[str] = None
    emp_id: Optional[str]  = None
    template_id :Optional[str]= None
    temp_key_name :Optional[str] = None
    temp_value : Optional[str]= None
 
class ProductTemplateKeyUpdate(BaseModel):
    temp_key_id :Optional[str] = None
    temp_key_name :Optional[str] = None
    temp_value :Optional[str] = None
 
class ProductTemplateKeyDelete(BaseModel):
    temp_key_id :Optional[str] = None
 