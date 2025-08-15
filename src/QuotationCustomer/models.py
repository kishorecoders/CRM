from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime

class QuotationCustomerBase(SQLModel):
    admin_id : str = Field(nullable=False,default=None)
    employe_id : Optional[str] = Field(nullable=False,default=None)
    first_name : Optional[str] = Field(nullable=False,default=None)
    last_name : Optional[str] = Field(nullable=False,default=None)
    gender : Optional[str] = Field(nullable=False,default=None)
    company_name : Optional[str] = Field(nullable=False,default=None)
    contact_number : Optional[str] = Field(nullable=False,default=None)
    email: Optional[str] = Field(nullable=False,default=None)
    customer_type: Optional[str] = Field(nullable=False,default=None)
    website: Optional[str] = Field(nullable=False,default=None)
    industry_and_segment: Optional[str] = Field(nullable=False,default=None)
    country: Optional[str] = Field(nullable=False,default=None)
    state: Optional[str] = Field(nullable=False,default=None)
    city: Optional[str] = Field(nullable=False,default=None)
    receivables : Optional[str] = Field(nullable=False,default=None)
    receivables_notes : Optional[str] = Field(nullable=False,default=None)
    bussiness_procpect : Optional[str] = Field(nullable=False,default=None)
    order_target : Optional[str] = Field(nullable=False,default=None)
    msme_no : Optional[str] = Field(nullable=False,default=None)
    pan_no : Optional[str] = Field(nullable=False,default=None)
    address : Optional[str] = Field(nullable=True,default=None)
    postal_code : Optional[str] = Field(nullable=True,default=None)
    gst_number : Optional[str]= Field(nullable=True,default=None)
    

class QuotationCustomer(QuotationCustomerBase,table = True):
    __tablename__ = "quotation_customer"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class QuotationCustomerCreate(QuotationCustomerBase):
    pass

class QuotationCustomerRead(QuotationCustomerBase):
    id : int



class GetCustomerRequest(BaseModel):
    admin_id: str 
    employe_id: Optional[str] = None  



class UpdateCustomerRequest(BaseModel):
    admin_id: str  
    customer_id: int  
    employe_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    company_name: Optional[str] = None
    contact_number: Optional[str] = None
    email: Optional[EmailStr] = None  
    customer_type: Optional[str] = None
    website: Optional[str] = None
    industry_and_segment: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    receivables: Optional[str] = None
    receivables_notes: Optional[str] = None
    bussiness_procpect: Optional[str] = None
    order_target: Optional[str] = None
    msme_no: Optional[str] = None
    pan_no: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    gst_number: Optional[str] = None
    




class DeleteCustomerRequest(BaseModel):
    admin_id: str
    customer_id: int
