from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime

class QuotationTemplateBase(SQLModel):
    admin_id : str = Field(nullable=False,default=None)
    employee_id : str = Field(nullable=True,default=None)
    template_name : Optional[str] = Field(nullable=False,default=None)

    admin_emp_id : Optional[str] = Field(nullable=True,default=None)
    created_by_type : Optional[str] = Field(nullable=True,default=None)

    updated_by_type : Optional[str] = Field(nullable=True,default=None)
    updated_admin_emp_id : Optional[str] = Field(nullable=True,default=None)



class QuotationTemplate(QuotationTemplateBase,table = True):
    __tablename__ = "quotation_template"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)


class QuotationTemplateCreate(BaseModel):
    admin_id : Optional[str] = None
    employee_id : Optional[str] = None
    template_name : Optional[str] = None

class AdminIDRequest(BaseModel):
    admin_id: str
    employee_id: Optional[str] = None


class QuotationTemplatesDelete(BaseModel):
    template_id: str
    