from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime
from sqlalchemy import Column, DateTime, Text , BigInteger


class QuotationProductEmployeeBase(SQLModel):
    admin_id : str = Field(nullable=False,default=None)
    employee_id: Optional[str] = Field(nullable=False)
    quote_id : str = Field(nullable=False,default=None)
    lead_id : Optional[str] = Field(nullable=True,default=None)

    product_name: Optional[str] = Field(sa_column=Column(Text, nullable=False))    

    product_code: Optional[str] = Field(nullable=False)
    hsn_code: Optional[str] = Field(nullable=False)
    rate_per_unit: Optional[float] = Field(nullable=False)
    quantity: Optional[int] = Field(nullable=False)
    total: Optional[float] = Field(nullable=False)
    gst_percentage: Optional[float] = Field(nullable=False)
    gross_total: Optional[float] = Field(nullable=False)
    availability: Optional[str] = Field(nullable=False)
    status: str = Field(nullable=True,default=None)
    steps : Optional[str] = Field(nullable=True,default=None)
    time_riquired_for_this_process : Optional[str] = Field(nullable=True,default=None)
    day : Optional[str] = Field(nullable=True,default=None)
    discount_type: Optional[str] = Field(nullable=True,default=None)
    discount_amount: Optional[str] = Field(nullable=True,default=None)
    discount_percent: Optional[str] = Field(nullable=True,default=None)
    unit : Optional[str] = Field(nullable=True,default=None)
    order_id : Optional[str] = Field(nullable=True,default=None)
    

    discription: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )    
    
    product_payment_type: Optional[str] = Field(nullable=True,default="Percentage")
    product_cash_balance: Optional[str] = Field(nullable=True,default="0%")
    product_account_balance: Optional[str] = Field(nullable=True,default="100%")
    
    
    dispatch_status: Optional[str] = Field(nullable=False,default="Pending")
    give_credit: Optional[str] = Field(nullable=True,default=None)
    
    remark: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )    
    
    
    booked_status: Optional[int] = Field(nullable=True,default=0)
    add_dispatch : bool = Field(nullable=True,default=False)


    product_type: Optional[str] = Field(nullable=True,default=None)
    product_id: Optional[str] = Field(nullable=True,default=None)
    specification: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )
    
    available_quantity: Optional[str] = Field(nullable=True,default=None)
    manufacture_quantity: Optional[str] = Field(nullable=True,default=None)

    
class QuotationProductEmployee(QuotationProductEmployeeBase,table = True):
    __tablename__ = "quotation_product_employee"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    product_release_at: datetime = Field(nullable=True,default=None)

    

class QuotationProductEmployeeCreate(QuotationProductEmployeeBase):
    pass


class QuotationProductEmployeeUpdate(QuotationProductEmployeeCreate):
    id: Optional[int]  




class QuotationProductEmployeeRead(QuotationProductEmployeeBase):
    id: int



class ProductEmployeeQuery(BaseModel):
    admin_id: str
    employee_id: str



class QuotationProductEmployeeCreateList(BaseModel):
    products: List[QuotationProductEmployeeCreate]



class ReleaseRequest(BaseModel):
    admin_id: str
    employee_id: str
    product_id: str
    status: str
    order_id: str
    
    type: Optional[str] = None
    InventoryOutward_id: Optional[str] = None
    add_remark: Optional[str] = None
    
    
class bookRequest(BaseModel):
    admin_id: str
    employee_id: str
    product_id: str
    status: str
    order_id: str


class ProductFilterQuery(BaseModel):
    admin_id: str
    employee_id: Optional[str] = None
    product_name: Optional[str] = None
    
    
    
class StageUpdateRequest(BaseModel):
    admin_id: str
    employee_id: Optional[str] = None
    product_id: str
    type: str
    stages: str


class ProductDispatchStatusUpdate(BaseModel):
    admin_id: str
    employee_id: Optional[str] = None
    quote_id: str
    product_id: str
    dispatch_status: str
    give_credit: Optional[str] = None
    remark: Optional[str] = None


class UpdateBookedStatus(SQLModel):
    id: int
    booked_status: int
    

class ProductList(BaseModel):
    product_id: str
    dispatch_status: str
    give_credit: Optional[str] = None
    remark: Optional[str] = None

class ProductmultipleDispatchStatusUpdate(BaseModel):
    admin_id: str
    employee_id: Optional[str] = None
    quote_id: str
    product : List[ProductList]


