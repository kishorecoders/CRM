from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime

class VendorBase(SQLModel):
    admin_id : str = Field(nullable=False,default=None)
    employe_id : Optional[str] = Field(nullable=True,default=None)
    vendor_name : Optional[str] = Field(nullable=True,default=None)
    contact_person : Optional[str] = Field(nullable=True,default=None)
    contact_gst_number : Optional[str] = Field(nullable=True,default=None)
    contact_number : Optional[str] = Field(nullable=True,default=None)
    email : Optional[str] = Field(nullable=True,default=None)
    pan_no : Optional[str] = Field(nullable=True,default=None)
    vendor_address : Optional[str] = Field(nullable=True,default=None)
    vendor_state : Optional[str] = Field(nullable=True,default=None)
    vendor_pin : Optional[str] = Field(nullable=True,default=None)
    account_holder_name : Optional[str] = Field(nullable=True,default=None)
    account_number : Optional[str] = Field(nullable=True,default=None)
    ifsc_code : Optional[str] = Field(nullable=True,default=None)

    bank_name : Optional[str] = Field(nullable=True,default=None)
    business_name : Optional[str] = Field(nullable=True,default=None)

    created_by_type : Optional[str] = Field(nullable=True,default=None)
    admin_emp_id : Optional[str] = Field(nullable=True,default=None)

    updated_by_type : Optional[str] = Field(nullable=True,default=None)
    updated_admin_emp_id : Optional[str] = Field(nullable=True,default=None)


class Vendor(VendorBase,table = True):
    __tablename__ = "vendor"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class VendorCreate(BaseModel):
    admin_id : Optional[str] =None
    employe_id : Optional[str] =None
    vendor_name : Optional[str] =None
    contact_person : Optional[str] =None
    contact_gst_number : Optional[str] =None
    contact_number : Optional[str] =None
    email : Optional[str] =None
    pan_no : Optional[str] =None
    vendor_address : Optional[str] =None
    vendor_state : Optional[str] =None
    vendor_pin : Optional[str] =None
    account_holder_name : Optional[str] =None
    account_number : Optional[str] =None
    ifsc_code : Optional[str] =None
    bank_name : Optional[str] =None
    business_name : Optional[str] =None


class VendorRead(VendorBase):
    id : int
    
    
class VendorDelete(BaseModel):
    id : int
