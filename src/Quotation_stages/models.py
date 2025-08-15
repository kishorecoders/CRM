from sqlmodel import SQLModel, Field, Relationship
from pydantic import UUID4
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime



class QuotationStagesBase(SQLModel):
    admin_id: str = Field(nullable=True, default=None)
    product_id: str = Field(nullable=True, default=None)
    assign_employee: str = Field(nullable=True, default=None)
    type: Optional[str] = Field(nullable=True,default=None)
    step_id: Optional[str] = Field(nullable=True,default=None)
    stage_id: Optional[str] = Field(nullable=True,default=None)
    step_item: Optional[str] = Field(nullable=True,default=None)
    remark: Optional[str] = Field(nullable=True,default=None)
    date_time: Optional[str] = Field(nullable=True,default=None)
    assign_date_time: datetime = Field(default_factory=get_current_datetime, nullable=True)
    previous_date_time: Optional[str] = Field(nullable=True,default=None)
    previous_employee: Optional[str] = Field(nullable=True,default=None)
    status: Optional[str] = Field(nullable=True,default="Pending")
    sub_product_ids: Optional[str] = Field(nullable=True, default=None)
    created_by_type: Optional[str] = Field(nullable=True, default=None)
    admin_emp_id: Optional[str] = Field(nullable=True, default=None)
    

class QuotationStages(QuotationStagesBase, table=True):
    __tablename__ = "Quotation_Product_Stages"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=True)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=True)


