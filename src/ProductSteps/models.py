from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime

class ProductStepsBase(SQLModel):
    admin_id : str = Field(nullable=False,default=None)
    employe_id : Optional[str] = Field(nullable=False,default=None)
    step_name : Optional[str] = Field(nullable=False,default=None)
    position : int = Field(nullable=True,default=None)
    
    created_by_type : Optional[str] = Field(nullable=True,default=None)
    admin_emp_id : Optional[str] = Field(nullable=True,default=None)

    updated_by_type : Optional[str] = Field(nullable=True,default=None)
    updated_admin_emp_id : Optional[str] = Field(nullable=True,default=None)
    
    file_path : Optional[str] = Field(nullable=True,default=None)
    type : Optional[str] = Field(nullable=True,default=None)


class ProductSteps(ProductStepsBase,table = True):
    __tablename__ = "product_steps"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class ProductStepsCreate(BaseModel):
    admin_id :Optional[str] = None
    employe_id : Optional[str] = None
    step_name : Optional[str] = None
    position : Optional[int] = 0
    file_path : Optional[str] = None
    type : Optional[str] = None
    
class ProductStepsRead(ProductStepsBase):
    id : int


class GetStepsRequest(BaseModel):
    admin_id: str
    employe_id: Optional[str] = None
    is_visible: Optional[bool] = None


class UpdateStepRequest(BaseModel):
    step_id: int
    admin_id: str
    employe_id: str = None
    step_name: str = None
    position:  int = None
    file_path : Optional[str] = None
    type : Optional[str] = None

class DeleteStepRequest(BaseModel):
    admin_id: str
    step_id: int
    
    
class DeleteStepfile(BaseModel):
    step_id: int
    
    
    