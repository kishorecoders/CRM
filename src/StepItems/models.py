from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime

class StepItemsBase(SQLModel):
    admin_id : str = Field(nullable=False,default=None)
    employe_id : Optional[str] = Field(nullable=False,default=None)
    step_id : Optional[int] = Field(nullable=False,default=None)
    item_name : Optional[str] = Field(nullable=False,default=None)
    aval_quantity : Optional[str] = Field(nullable=True,default=None)
    discription : Optional[str] = Field(nullable=True,default=None)
    product_id : Optional[str] = Field(nullable=True,default=None)
    required_quantity : Optional[str] = Field(nullable=True,default=None)
    stage_id : Optional[str] = Field(nullable=True,default=None)

    created_by_type : Optional[str] = Field(nullable=True,default=None)
    admin_emp_id : Optional[str] = Field(nullable=True,default=None)

    updated_by_type : Optional[str] = Field(nullable=True,default=None)
    updated_admin_emp_id : Optional[str] = Field(nullable=True,default=None)


class StepItems(StepItemsBase,table = True):
    __tablename__ = "step_items"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class StepItemsCreate(BaseModel):
    admin_id : str = None
    employe_id : Optional[str] = None
    step_id : Optional[int] = None
    item_name : Optional[str] = None
    aval_quantity : Optional[str] = None
    discription : Optional[str] = None
    product_id : Optional[str] = None
    required_quantity : Optional[str] = None
    stage_id : Optional[str] = None

class StepItemsRead(StepItemsBase):
    id : int



class StepItemFilterRequest(BaseModel):
    admin_id: str
    step_id: Optional[int] = None
    employee_id: Optional[str] = None
    stage_id: Optional[str] = None
    product_ids: Optional[list[int]] = None

class StepItemUpdateRequest(BaseModel):
    step_item_id: int
    admin_id: str
    employe_id : Optional[str] = None
    item_name: Optional[str] = None
    step_id: Optional[int] = None
    aval_quantity: str
    discription: str
    required_quantity: str



class StepItemDeleteRequest(BaseModel):
    admin_id: str
    step_item_id: int
    
    
    

class StepItemsBulkCreateRequest(BaseModel):
    step_items: List[StepItemsCreate]


