from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime

class DispatchVendorBase(SQLModel):
    admin_id : str = Field(nullable=False,default=None)
    employee_id : Optional[str] = Field(nullable=False,default=None)
    vendor_name : Optional[str] = Field(nullable=False,default=None)
    contact_number : Optional[str] = Field(nullable=False,default=None)
    another_contact_number : Optional[str] = Field(nullable=False,default=None)
    email : Optional[str] = Field(nullable=False,default=None)
    city  : Optional[str] = Field(nullable=False,default=None)
    drive : Optional[str] = Field(nullable=False,default=None)
    vehicle_type : Optional[str] = Field(nullable=False,default=None)
    vehicle_number : Optional[str] = Field(nullable=False,default=None)
    vehicle_operator_name : Optional[str] = Field(nullable=False,default=None)
    body_condition : Optional[str] = Field(nullable=False,default=None)
    file_path : Optional[str] = Field(nullable=False,default=None)
    company_name : Optional[str] = Field(nullable=True,default=None)

    created_by_type : Optional[str] = Field(nullable=True,default=None)
    admin_emp_id : Optional[str] = Field(nullable=True,default=None)

    updated_by_type : Optional[str] = Field(nullable=True,default=None)
    updated_admin_emp_id : Optional[str] = Field(nullable=True,default=None)


class DispatchVendor(DispatchVendorBase,table = True):
    __tablename__ = "dispatch_vendor"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class DispatchVendorCreate(BaseModel):
    admin_id : str = None
    employee_id : Optional[str] = None
    vendor_name : Optional[str] = None
    contact_number : Optional[str] = None
    another_contact_number : Optional[str] = None
    email : Optional[str] = None
    city  : Optional[str] = None
    drive : Optional[str] = None
    vehicle_type : Optional[str] = None
    vehicle_number : Optional[str] = None
    vehicle_operator_name : Optional[str] = None
    body_condition : Optional[str] = None
    file_path : Optional[str] = None
    company_name : Optional[str] = None


class VendorListRequest(BaseModel):
    admin_id: Optional[str] = None
    employee_id: Optional[str] = None

class DispatchVendorRead(DispatchVendorBase):
    id: int
    created_at: datetime
    updated_at: datetime

class VendorListResponse(BaseModel):
    status: str
    message: str
    data: List[DispatchVendorRead]



class VendorUpdateRequest(BaseModel):
    vendor_id: int
    admin_id: Optional[str] = None
    employee_id: Optional[str] = None
    vendor_name: Optional[str] = None
    contact_number: Optional[str] = None
    another_contact_number: Optional[str] = None
    email: Optional[str] = None
    city: Optional[str] = None
    drive: Optional[str] = None
    vehicle_type: Optional[str] = None
    vehicle_number: Optional[str] = None
    vehicle_operator_name: Optional[str] = None
    body_condition: Optional[str] = None
    file_path: Optional[str] = None




class VendorDeleteRequest(BaseModel):
    vendor_id: int
    admin_id: str
    employee_id: Optional[str] = None