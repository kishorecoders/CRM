from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime

class ProductionRequestBase(SQLModel):
    admin_id : str = Field(nullable=False,default=None)
    employe_id : Optional[str] = Field(nullable=False,default=None)
    production_id: Optional[str] = Field(nullable=False,default=None)
    material_name : Optional[str] = Field(nullable=False,default=None)
    quantity : Optional[str] = Field(nullable=False,default=None)
    order_id : Optional[str] = Field(nullable=True,default=None)
    pruduct_name : Optional[str] = Field(nullable=True,default=None)
    stage_id : Optional[str] = Field(nullable=True,default=None)
    status : Optional[str] = Field(nullable=True,default=None)

    created_by_type : Optional[str] = Field(nullable=True,default=None)
    admin_emp_id : Optional[str] = Field(nullable=True,default=None)

    updated_by_type : Optional[str] = Field(nullable=True,default=None)
    updated_admin_emp_id : Optional[str] = Field(nullable=True,default=None)


class ProductionRequest(ProductionRequestBase,table = True):
    __tablename__ = "production_request"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)


class ProductionRequestCreate(BaseModel):
    admin_id : str = None
    employe_id : Optional[str] = None
    production_id: Optional[str] = None
    material_name : Optional[str] = None
    quantity : Optional[str] = None
    order_id : Optional[str] = None
    pruduct_name : Optional[str] = None
    stage_id : Optional[str] = None
    status : Optional[str] = None


class ProductionRequestRead(BaseModel):
    admin_id: int
    employee_id: Optional[str] = None
    
    
    
class ProductionRequestUpdate(BaseModel):
    production_request_id: str
    admin_id: str
    status: str
    employe_id: Optional[str] = None

class ProductionRequestDelete(BaseModel):
    stage_id: str
    admin_id: str