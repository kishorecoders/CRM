from sqlmodel import SQLModel, Field
from pydantic import UUID4
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime
from sqlalchemy import Column, DateTime, Text , BigInteger


class GrnInvoiceBase(SQLModel):
    admin_id: Optional[str] = Field(nullable=False, default=None)
    employee_id: Optional[str] = Field(nullable=True, default=None)
    grn_number: Optional[str] = Field(nullable=True, default=None)
    grn_id: Optional[str] = Field(nullable=True, default=None)
    invoice_amount: Optional[str] = Field(nullable=True, default=None)
    vendor_id: Optional[str] = Field(nullable=True, default=None)
    series_id: Optional[str] = Field(nullable=True, default=None)
    vender_invoice_number: Optional[str] = Field(nullable=True, default=None)
    invoice_date: Optional[str] = Field(nullable=True, default=None)
    status:Optional[str] = Field(nullable=True, default="Pending Payment")
    #remark:Optional[str] = Field(nullable=True, default=None)
    
    remark: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )

    created_by_type : Optional[str] = Field(nullable=True,default=None)
    admin_emp_id : Optional[str] = Field(nullable=True,default=None)
    
    updated_by_type : Optional[str] = Field(nullable=True,default=None)
    updated_admin_emp_id : Optional[str] = Field(nullable=True,default=None)

    

class GrnInvoice(GrnInvoiceBase,table = True):
    __tablename__ = "grn_invoice"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)




class GrnInvoiceCreate(BaseModel):
    admin_id: Optional[str] = None
    employee_id: Optional[str] = None
    grn_number: Optional[str] = None
    grn_id: Optional[str] = None
    invoice_amount: Optional[str] = None
    vendor_id: Optional[str] = None
    series_id: Optional[str] = None
    vender_invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    
    
    
    
class GrnInvoiceUpdate(BaseModel):
    id: int
    admin_id: Optional[str] = None
    employee_id: Optional[str] = None
    grn_number: Optional[str] = None
    grn_id: Optional[str] = None
    invoice_amount: Optional[str] = None
    vendor_id: Optional[str] = None
    vender_invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None




class GrnInvoiceGetRequest(BaseModel):
    admin_id: str
    employee_id: Optional[str] = None
    grn_id: Optional[str] = None
    
    
    
    
class GrnInvoiceProductItem(BaseModel):
    product_id: str
    accepted_qty_by_invoice: Optional[str] = None
    rate: Optional[str] = None
    amount: Optional[str] = None

class GrnInvoiceCreateExtended(GrnInvoiceCreate):
    products: List[GrnInvoiceProductItem]
    
    
    
    
class GrnInvoiceStatusUpdateRequest(BaseModel):
    id: int
    admin_id: Optional[str] = None
    employee_id: Optional[str] = None
    grn_id: str
    remark: Optional[str] = None



