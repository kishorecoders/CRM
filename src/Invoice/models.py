from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime

class InvoiceBase(SQLModel):
    admin_id : Optional[str] = Field(nullable=False,default=None)
    employe_id : Optional[str] = Field(nullable=False,default=None)
    admin_sales_id : Optional[str] = Field(nullable=False,default=None)
    company_name : Optional[str] = Field(nullable=False,default=None)
    product_id : Optional[str] = Field(nullable=False,default=None)
    invoice_date : Optional[str] = Field(nullable=False,default=date.today())
    invoice_number : Optional[str] = Field(nullable=False,default=None)
    order : Optional[str] = Field(nullable=False,default=None)
    reference : Optional[str] = Field(nullable=True,default=None)
    sales_persone : Optional[str] = Field(nullable=True,default=None)
    subject : Optional[str] = Field(nullable=False,default=None)
    gst_treatment : Optional[str] = Field(nullable=False,default=None)
    billing_address : Optional[str] = Field(nullable=False,default=None)
    billing_city : Optional[str] = Field(nullable=False,default=None)
    billing_state : Optional[str] = Field(nullable=False,default=None)
    billing_country : Optional[str] = Field(nullable=False,default=None)
    billing_pincode : Optional[str] = Field(nullable=False,default=None)
    shipping_address : Optional[str] = Field(nullable=False,default=None)
    shipping_city : Optional[str] = Field(nullable=False,default=None)
    shipping_state : Optional[str] = Field(nullable=False,default=None)
    shipping_country : Optional[str] = Field(nullable=False,default=None)
    shipping_pincode : Optional[str] = Field(nullable=False,default=None)
    sgst : Optional[str] = Field(nullable=False,default=None)
    cgst : Optional[str] = Field(nullable=False,default=None)
    igst : Optional[str] = Field(nullable=False,default=None)
    rounding : Optional[str] = Field(nullable=False,default=None)
    total : Optional[str] = Field(nullable=False,default=None)
    payment_made : Optional[str] = Field(nullable=False,default=None)
    payment_option : Optional[str] = Field(nullable=False,default=None)
    notes : Optional[str] = Field(nullable=False,default=None)
    bank_charges : Optional[str] = Field(nullable=False,default=None)
    date : Optional[str] = Field(nullable=False,default=date.today())
    payment_mode : Optional[str] = Field(nullable=False,default=None)
    quantity : Optional[str] = Field(nullable=False,default=None)
    discount : Optional[str] = Field(nullable=False,default=None)

class Invoice(InvoiceBase,table = True):
    __tablename__ = "invoice"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceRead(InvoiceBase):
    id : int