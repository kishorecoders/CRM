from sqlmodel import SQLModel, Field, Column, JSON
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from src.parameter import get_current_datetime
from pydantic import BaseModel, root_validator
from typing import List, Dict, Union


class EmployeeTasksCustomerBase(SQLModel):
    admin_id: int = Field(nullable=True, default=None)
    emp_id: str = Field(nullable=True, default=None)
    customer_name: str = Field(nullable=True, default=None)
    site_name: Optional[str] = Field(nullable=True, default=None)
    


class EmployeeTasksCustomer(EmployeeTasksCustomerBase, table=True):
    __tablename__ = "Employee_Tasks_Customer"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    

class CustomerCreate(BaseModel):
    admin_id: Optional[str] = None
    emp_id: Optional[str] = None
    customer_name: Optional[str] = None
    site_name: Optional[str] = None
    
class CustomerGet(BaseModel):
    admin_id: Optional[str] = None
    emp_id: Optional[str] = None
    customer_id: Optional[str] = None
    

class Customerupdate(BaseModel):
    customer_id: Optional[str] = None
    admin_id: Optional[str] = None
    emp_id: Optional[str] = None
    customer_name: Optional[str] = None
    site_name: Optional[str] = None
    
class CustomerDelete(BaseModel):
    customer_id: Optional[str] = None
    admin_id: Optional[str] = None
    emp_id: Optional[str] = None
    
    
    