from sqlmodel import SQLModel, Field, Relationship
from pydantic import UUID4
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime
from sqlalchemy import Column, DateTime, Text , BigInteger


class ProductStagesBase(SQLModel):
    admin_id: str = Field(nullable=True, default=None)
    product_id: str = Field(nullable=True, default=None)
    assign_employee: str = Field(nullable=True, default=None)
    steps : Optional[str] = Field(nullable=True,default=None)
    time_riquired_for_this_process : Optional[str] = Field(nullable=True,default=None)
    day : Optional[str] = Field(nullable=True,default=None)
    type: Optional[str] = Field(nullable=True,default=None)
    step_id: Optional[str] = Field(nullable=True,default=None)
    step_item: Optional[str] = Field(nullable=True,default=None)

    remark: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )    

    date_time: Optional[str] = Field(nullable=True,default=None)
    assign_date_time: datetime = Field(default_factory=get_current_datetime, nullable=True)
    previous_date_time: Optional[str] = Field(nullable=True,default=None)
    previous_employee: Optional[str] = Field(nullable=True,default=None)
    status: Optional[str] = Field(nullable=True,default="Pending")

    sub_product_ids: Optional[str] = Field(nullable=True, default=None)
    parent_stage_id: Optional[str] = Field(nullable=True, default=None)
    
    is_from_product: Optional[bool] = Field(nullable=True, default=False)

    selected_product_ids: Optional[str] = Field(nullable=True, default=None)

    serial_number: Optional[str] = Field(nullable=True, default=None)
    file_path: Optional[str] = Field(nullable=True, default=None)


class ProductStages(ProductStagesBase, table=True):
    __tablename__ = "product_stages"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=True)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=True)



class AssignStageRequest(BaseModel):
    admin_id: str
    product_id: str
    stage_id: int  
    assign_employee: str
    steps: Optional[str] = None
    time_riquired_for_this_process: Optional[str] = None
    day: Optional[str] = None
    type: str
    #step_id: str
    step_id: Optional[str] = None
    step_item: Optional[str] = None
    remark: Optional[str] = None
    date_time: Optional[str] = None
    parent_stage_id: Optional[str] = None
    file_path: Optional[str] = None
    serial_number: Optional[str] = None
    sub_product_ids: Optional[list[int]] = None
    selected_product_ids: Optional[list[int]] = None


class StageDeleteRequest(BaseModel):
    admin_id: str
    product_id: str
    stage_id: str
    
    
    

class GetStageListRequest(BaseModel):
    product_id: str
    type: str


    
    

   

