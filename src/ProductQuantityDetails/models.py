from sqlmodel import SQLModel,Field
from datetime import datetime
from typing import Optional
from src.parameter import get_current_datetime
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Text , BigInteger



class ProductQuantityBase(SQLModel):
    admin_id : str = Field(nullable=True,default=None)
    emplpoyee_id :Optional[str] = Field(nullable=True,default=None)
    prev_opening_stock : Optional[str] = Field(nullable=True,default=None)
    new_opening_stock : Optional[str] = Field(nullable=True,default=None)
    created_by_type : Optional[str] = Field(nullable=True,default=None)
    admin_emp_id : Optional[str] = Field(nullable=True,default=None)
    product_id : Optional[str] = Field(nullable=True,default=None)

    add_remark: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )
    
class ProductQuantity(ProductQuantityBase,table = True):
    __tablename__ = "Product_Quantity"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class ProductQuantityRead(BaseModel):
    admin_id: str
    employee_id: Optional[str] = None
    product_id: Optional[str] = None

