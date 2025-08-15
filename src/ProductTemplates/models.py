from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime
import json

class TemplateItem(BaseModel):
    temp_key_name: str
    temp_value: str

# class TemplateInput(BaseModel):
#     product_id: str
#     admin_id: str
#     emp_id: str
#     template_name: List[TemplateItem]


class TemplateInput(BaseModel):
    product_id: str 
    admin_id: str 
    emp_id: str
    template_name: str 
    # temp_name_value: List[TemplateItem] 


class ProductTemplateBase(SQLModel):
    admin_id : Optional[str] = Field(nullable=False,default=None)
    emp_id: Optional[str] = Field(nullable=True ,default=None)
    product_id :Optional[str] = Field(nullable=False,default=None)
    template_name : Optional[str]= Field(nullable=True,default=None)

    # def set_template_name(self, templates: list):
    #     # Convert each TemplateItem to dict
    #     self.template_name = json.dumps(
    #         [t.dict() if hasattr(t, 'dict') else t for t in templates]
    #     )

    # def get_template_name(self) -> Optional[list]:
    #     if self.template_name:
    #         return json.loads(self.template_name)
    #     return None
    
class ProductTemplate(ProductTemplateBase,table = True):
    __tablename__ = "product_templates"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class TemplateRead(BaseModel):
    product_id: str
    product_code: str


class TemplateDelete(BaseModel):
    id: Optional[int] = None

class TemplateUpdate(BaseModel):
    template_id: Optional[int] = None
    updated_items: List[TemplateItem]
