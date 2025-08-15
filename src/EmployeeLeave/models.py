from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime
from pydantic import BaseModel, validator
from typing import Any
from pydantic import BaseModel, root_validator
from sqlalchemy import Column, DateTime, Text , BigInteger

class EmployeeLeaveBase(SQLModel):
    admin_id: str
    employee_id: str
    leave_type: str
    start_date: datetime
    end_date: datetime
    leave_priority: Optional[str] = None  
    pdf_file_or_image: Optional[str] = None 
    type: Optional[str] = None 
    
    
    leave_matter: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )
    
    
    status: Optional[str] = None 
    half_or_full_day: Optional[str] = None
    remark: Optional[str] = None 

    remark: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )
    
    created_by_type : Optional[str] = Field(nullable=True,default=None)
    admin_emp_id : Optional[str] = Field(nullable=True,default=None)

    updated_by_type : Optional[str] = Field(nullable=True,default=None)
    updated_admin_emp_id : Optional[str] = Field(nullable=True,default=None)

    approve_by_type : Optional[str] = Field(nullable=True,default=None)
    approve_admin_emp_id : Optional[str] = Field(nullable=True,default=None)
    approve_updated_at: datetime = Field(default_factory=get_current_datetime, nullable=True)

    rejacted_by_type : Optional[str] = Field(nullable=True,default=None)
    rejacted_admin_emp_id : Optional[str] = Field(nullable=True,default=None)
    rejacted_updated_at: datetime = Field(default_factory=get_current_datetime, nullable=True)


    
class EmployeeLeave(EmployeeLeaveBase,table = True):
    __tablename__ = "employee_leave"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)




class EmployeeLeaveCreate(BaseModel):
    admin_id: str
    employee_id: str
    leave_type: str
    start_date: date  
    end_date: date
    leave_priority: Optional[str] = None
    pdf_file_or_image: Optional[str] = None
    type: Optional[str] = None
    leave_matter: Optional[str] = None
    status: Optional[str] = None 
    half_or_full_day: Optional[str] = None

    created_by_type :Optional[str] = None
    admin_emp_id : Optional[str] =None


class EmployeeLeaveStatusUpdate(BaseModel):
    admin_id: str
    employee_id: str
    leave_id: str
    status: str
    remark: str

    approve_by_type : Optional[str] =None
    approve_admin_emp_id :Optional[str] = None

    rejacted_by_type :Optional[str] = None
    rejacted_admin_emp_id :Optional[str] = None

class EmployeeLeaveRead(EmployeeLeaveBase):
    id: int


class EmployeeLeaveUpdate(BaseModel):
    admin_id: str
    employee_id: str
    leave_id: int 
    leave_type: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    leave_priority: Optional[str] = None
    pdf_file_or_image: Optional[str] = None
    type: Optional[str] = None
    leave_matter: Optional[str] = None
    status: Optional[str] = None
    remark: Optional[str] = None
    half_or_full_day: Optional[str] = None
    
    updated_by_type :Optional[str] = None
    updated_admin_emp_id :Optional[str] = None


class EmployeeLeaveDelete(BaseModel):
    admin_id: str
    employee_id: str
    leave_id: int

