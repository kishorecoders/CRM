from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime
from sqlalchemy import Column, DateTime, Text , BigInteger


class QuotationProductBase(SQLModel):
    admin_id : str = Field(nullable=False,default=None)
    employee_id: Optional[str] = Field(nullable=True)
    template_id: Optional[str] = Field(nullable=False)
    product_name: Optional[str] = Field(nullable=False)
    product_code: Optional[str] = Field(nullable=False)
    hsn_code: Optional[str] = Field(nullable=False)
    rate_per_unit: Optional[float] = Field(nullable=False)
    quantity: Optional[int] = Field(nullable=False)
    total: Optional[float] = Field(nullable=False)
    gst_percentage: Optional[float] = Field(nullable=False)
    gross_total: Optional[float] = Field(nullable=False)
    availability: Optional[str] = Field(nullable=False)
    product_id: Optional[str] = Field(nullable=True,default=None)

    discription: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )    

    unit: Optional[str] = Field(nullable=True,default=None)
   




    
class QuotationProduct(QuotationProductBase,table = True):
    __tablename__ = "quotation_product"
    
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

    

class QuotationProductCreate(BaseModel):
    admin_id : str = None
    employee_id: Optional[str] = None
    template_id: Optional[str] = None
    product_name: Optional[str] = None
    product_code: Optional[str] = None
    hsn_code: Optional[str] = None
    rate_per_unit: Optional[float] = None
    quantity: Optional[int] = None
    total: Optional[float] = None
    gst_percentage: Optional[float] = None
    gross_total: Optional[float] = None
    availability: Optional[str] = None
    product_id: Optional[str] = Field(nullable=True,default=None)
    discription: Optional[str] = Field(nullable=True,default=None)
    unit: Optional[str] = Field(nullable=True,default=None)
   

class QuotationProductRead(QuotationProductBase):
    id: int

class ProductQuery(BaseModel):
    admin_id: str
    template_id: str



class QuotationProductCreateList(BaseModel):
    products: List[QuotationProductCreate]


class QuotationProductDeleteRequest(BaseModel):
    admin_id: str
    template_id: str
    product_id: str



class QuotationProductUpdate(BaseModel):
    admin_id: str
    template_id: str
    product_id: str
    product_name: Optional[str] = None
    product_code: Optional[str] = None
    hsn_code: Optional[str] = None
    rate_per_unit: Optional[float] = None
    quantity: Optional[int] = None
    total: Optional[float] =None
    gst_percentage: Optional[float] = None
    availability: Optional[str] = None