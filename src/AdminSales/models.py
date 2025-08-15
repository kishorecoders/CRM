from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime
from pydantic import BaseModel, validator
from sqlalchemy import Column, DateTime, Text , BigInteger


class FileItem(BaseModel):
    file_name: str
    file_path: str

class AdminSalesBase(SQLModel):
    admin_id : int = Field(nullable=False,default=None)
    lead_source : Optional[str] = Field(nullable=True,default=None)
    name : Optional[str] = Field(nullable=False,default=None)
    business_name : Optional[str] = Field(nullable=True,default=None)
    email : Optional[str] = Field(nullable=True,default=None)
    contact_details : str = Field(nullable=True,default=None)
    contact_details_2 : Optional[str] = Field(nullable=True,default=None)
    lead_status : Optional[str] = Field(nullable=True,default="Not Assigned")
    allocated_emplyee_id : Optional[str] = Field(nullable=True,default=None)
    profile_image : Optional[str] = Field(nullable=True,default=None)
    status : Optional[str] = Field(nullable=True,default=None)

    address: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )
    
    discription: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )    

    gst_number : Optional[str] = Field(nullable=True,default=None)
    city : Optional[str] = Field(nullable=True,default=None)
    pincode : Optional[str] = Field(nullable=True,default=None)
    state : Optional[str] = Field(nullable=True,default=None)
    mark_status : Optional[str] = Field(nullable=True,default=None)
    created_by_type : Optional[str] = Field(nullable=True,default=None)
    admin_emp_id : Optional[str] = Field(nullable=True,default=None)
    lead_source_name : Optional[str] = Field(nullable=True,default=None)

    is_duplicate: Optional[bool] = Field(default=False)


    file_path : Optional[str] = Field(nullable=True,default=None)

    updated_by_type : Optional[str] = Field(nullable=True,default=None)
    updated_admin_emp_id : Optional[str] = Field(nullable=True,default=None)
    gst_verify: Optional[bool] = Field(default=False, nullable=True)

    
class AdminSales(AdminSalesBase,table = True):
    __tablename__ = "admin_sales"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
   
   

class AdminSalesCreate(BaseModel):
    admin_id: int
    lead_source: str
    name: str
    business_name: Optional[str] = None
    email: Optional[str] = None
    contact_details: str
    contact_details_2: str
    lead_status: Optional[str] = "Not Assigned"
    allocated_emplyee_id: Optional[str] = None
    profile_image: Optional[str] = None
    status: Optional[str] = None
    address: Optional[str] = None
    discription: Optional[str] = None
    gst_number: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None
    state: Optional[str] = None
    mark_status: Optional[str] = None
    created_by_type: Optional[str] = None
    admin_emp_id: Optional[str] = None
    lead_source_name: Optional[str] = None
    updated_admin_emp_id: Optional[str] = None
    updated_by_type: Optional[str] = None
    gst_verify: Optional[bool] = None
    files: Optional[List[FileItem]]


class Leads(BaseModel):
    lead_source: str
    name: str
    business_name: Optional[str] = None
    email: Optional[str] = None
    contact_details: str
    contact_details_2: str
    lead_status: Optional[str] = "Not Assigned"
    allocated_emplyee_id: Optional[str] = None
    profile_image: Optional[str] = None
    status: Optional[str] = None
    address: Optional[str] = None
    discription: Optional[str] = None
    gst_number: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None
    state: Optional[str] = None
    mark_status: Optional[str] = None
    lead_source_name: Optional[str] = None

class AdminSalesM(BaseModel):
    admin_id: int
    created_by_type: Optional[str] = None
    admin_emp_id: Optional[str] = None
    Leads: Optional[list[Leads]] 



class AdminSalesRead(AdminSalesBase):
    id : int 



class AssignLeadsRequest(BaseModel):
    lead_ids: List[int] 
    employee_id: str
    admin_id: int


class AdminAssignLeadsRequest(BaseModel):
    admin_id: int
    employee_id: str


class AdminSalesFilterRequest(BaseModel):
    admin_id: int
    employe_id: Optional[str] = None
    status: Optional[str] = None
    lead_source: Optional[str] = None
    lead_name: Optional[str] = None
    lead_from_date: Optional[datetime] = None  
    lead_to_date: Optional[datetime] = None
    mobile_num: Optional[str] = None
    time_frame: Optional[str] = None
    lead_id_from: Optional[str] = None  
    lead_id_to: Optional[str] = None  
    page: Optional[int] = None
    page_size: Optional[int] = None
    
    
    
      
    
    @validator('lead_from_date', 'lead_to_date', pre=True, always=True)
    def empty_string_to_none(cls, v):
        if v == "":
            return None
        return v
    
    @validator('lead_id_from', 'lead_id_to', pre=True, always=True)
    def validate_lead_ids(cls, v):
        if v == "":
            return None 
        return v
    
    @validator('time_frame', always=True)
    def validate_time_frame(cls, v):
        if v and v not in ["Today", "Yesterday", "Last seven days", "This month"]:
            raise ValueError("Invalid time frame")
        return v

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }



class ReassignLeadsRequest(BaseModel):
    lead_ids: List[int]
    from_employee_id: str
    to_employee_id: str
    admin_id: int
    
    
class RemoveAdminSalesRequest(BaseModel):
    admin_id: Optional[int] = None
    employee_id: Optional[str] = None
    lead_id: int


class Leadcount(BaseModel):
    admin_id: int
    employee_id: Optional[str] = None

