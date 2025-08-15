from sqlmodel import SQLModel, Field
from pydantic import UUID4
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime

class GrnOrderIssueBase(SQLModel):
    admin_id: Optional[str] = Field(nullable=False, default=None)
    employee_id: Optional[str] = Field(nullable=True, default=None)
    purchase_order_id: Optional[str] = Field(nullable=True, default=None)
    grn_number: Optional[str] = Field(nullable=True, default=None)
    series_id: Optional[str] = Field(nullable=True, default=None)
    grn_date: Optional[str] = Field(nullable=True, default=None)
    vendor_id: Optional[str] = Field(nullable=True, default=None)
    invoice_chalan: Optional[str] = Field(nullable=True, default=None)
    invoice_chalan_date: Optional[str] = Field(nullable=True, default=None)
    business_name: Optional[str] = Field(nullable=True, default=None)
    grn_status: Optional[str] = Field(nullable=True, default="Pending")
    invoice_created : Optional[str] = Field(nullable=True, default="0")

    created_by_type : Optional[str] = Field(nullable=True,default=None)
    admin_emp_id : Optional[str] = Field(nullable=True,default=None)
    
    updated_by_type : Optional[str] = Field(nullable=True,default=None)
    updated_admin_emp_id : Optional[str] = Field(nullable=True,default=None)

    

class GrnOrderIssue(GrnOrderIssueBase,table = True):
    __tablename__ = "grn_order_issue"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)


class GrnOrderProductInputForGrn(BaseModel):
    product_id: Optional[str] = None
    recived_quantity: Optional[str] = None
    accepted_quantity: Optional[str] = None
    reject_quantity: Optional[str] = None
    remark: Optional[str] = None
    accepted_qty_by_invoice: Optional[str] = None
    rate: Optional[str] = None
    amount: Optional[str] = None

class GrnOrderIssueCreate(BaseModel):
    admin_id: Optional[str] = None
    employee_id: Optional[str] = None
    purchase_order_id: Optional[str] = None
    grn_number: Optional[str] = None
    series_id: Optional[str] = None
    grn_date: Optional[str] = None
    vendor_id: Optional[str] = None
    invoice_chalan: Optional[str] = None
    invoice_chalan_date: Optional[str] = None
    business_name: Optional[str] = None
    products: List[GrnOrderProductInputForGrn]

class GrnOrderIssueUpdate(BaseModel):
    grn_order_issue_id :Optional[str] = None
    admin_id: Optional[str] = None
    employee_id: Optional[str] = None
    purchase_order_id: Optional[str] = None
    grn_number: Optional[str] = None
    series_id: Optional[str] = None
    grn_date: Optional[str] = None
    vendor_id: Optional[str] = None
    invoice_chalan: Optional[str] = None
    invoice_chalan_date: Optional[str] = None
    business_name: Optional[str] = None
    products: List[GrnOrderProductInputForGrn]


class GrnOrderProductGet(BaseModel):
    admin_id: Optional[str] = None
    employee_id: Optional[str] = None
    grn_status: Optional[str] = None


class GrnOrderProductDelete(BaseModel):
    admin_id: Optional[str] = None
    employee_id: Optional[str] = None
    grn_id: Optional[str] = None



