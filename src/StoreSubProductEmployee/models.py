from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime

class StoreSubProductEmployeeBase(SQLModel):
    admin_id : Optional[str] = Field(nullable=True,default=None)
    emp_id: Optional[str] = Field(nullable=True ,default=None)
    product_id :Optional[str] = Field(nullable=True,default=None)
    sub_product_name : Optional[str]= Field(nullable=True,default=None)
    quantity : Optional[str]= Field(nullable=True,default=None)

    add_remark : Optional[str]= Field(nullable=True,default=None)
    production_id : Optional[str]= Field(nullable=True,default=None)

    parent_subproduct_id : Optional[str]= Field(nullable=True,default=None)


class StoreSubProductEmployee(StoreSubProductEmployeeBase,table = True):
    __tablename__ = "Store_sub_product_employee"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)


# class SubProductItem(BaseModel):
#     sub_product_name: str
#     quantity: int

# class QuotationSubProductEmployeeCreate(BaseModel):
#     admin_id: str
#     emp_id: str
#     product_id: str
#     add_remark: str
#     sub_products: List[SubProductItem]

# class QuotationSubProductEmployeeRead(BaseModel):
#     product_id : Optional[str]
#     product_code : Optional[str]

# class QuotationSubProductEmployeeDelete(BaseModel):
#     subproduct_id: int

# class QuotationSubProductAddRemark(BaseModel):
#     subproduct_id: int
#     add_remark: str

