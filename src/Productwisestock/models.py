from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime

class ProductWiseStockBase(SQLModel):
    admin_id : str = Field(nullable=False,default=0)
    emplpoyee_id :Optional[str] = Field(nullable=False,default=None)
    product_id : Optional[int] = Field(nullable=False,default=None)
    total_quantity : int = Field(nullable=False,default=None)
    
class ProductWiseStock(ProductWiseStockBase,table = True):  
    __tablename__ = "product_wise_stock"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class ProductWiseStockCreate(ProductWiseStockBase):
    pass

class ProductWiseStockRead(ProductWiseStockBase):
    id : int