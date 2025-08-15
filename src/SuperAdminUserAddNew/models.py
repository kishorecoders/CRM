from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List,Union
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime
from sqlalchemy import Column, DateTime, Text , BigInteger

class SuperAdminUserAddNewBase(SQLModel):
    full_name : str = Field(nullable=False,default=0)
    company_name : str = Field(nullable=False,default=0)
    designation : str = Field(nullable=False,default=0)
    email : str = Field(nullable=False,default=0)
    
    phone_number: int = Field(
        default=0,
        sa_column=Column(BigInteger, nullable=False, default=0)
    )
    
    plan_id : Optional[int] = Field(nullable=True,default=0)
    amount : Optional[float] = Field(nullable=True,default=0.0)
    demo_period_day : Optional[int] = Field(nullable=True,default=0)
    expiry_date : datetime = Field(nullable=True,default=None)
    password : Optional[str] = Field(nullable=True,default=0)
    confirm_password : Optional[str] = Field(nullable=True,default=0)
    gst_number : Optional[str] = Field(nullable=True,default=None)
    state : Optional[str] = Field(nullable=True,default=None)
    month : Optional[str] = Field(nullable=True,default=None)

    reset_token: Optional[str] = Field(nullable=True ,default=None)
    reset_token_expiry: Optional[datetime] = Field(nullable=True , default=None)
    device_token: Optional[str] = Field(nullable=True, default=None)
    device_type: Optional[str] = Field(nullable=True, default=None)
    
class SuperAdminUserAddNew(SuperAdminUserAddNewBase,table = True):
    __tablename__ = "super_admin_user_add_new_form"
    id : int = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    is_deleted: bool = Field(default=False, nullable=False)
    is_active:  bool = Field(default=False, nullable=False)
    deleted_date: Optional[datetime] = Field(default=None, nullable=True)
    

class SuperAdminUserAddNewCreate(BaseModel):
    full_name: Optional[str] = None
    company_name: Optional[str] = None
    designation: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[int] = None
    plan_id: Optional[int] = None
    amount: Optional[float] = None
    demo_period_day: Optional[int] = None
    expiry_date: Optional[Union[str, int]] = None
    month : Optional[str] = None
    password: Optional[str] = None
    confirm_password: Optional[str] = None  

  
class SuperAdminUserAddNewRead(SuperAdminUserAddNewBase):
    id : int    
    
class SuperAdminUserAddNewUpdate(SQLModel):
    full_name: Optional[str] = None
    company_name: Optional[str] = None
    designation: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[int] = None
    plan_id: Optional[int] = None
    amount: Optional[float] = None
    demo_period_day: Optional[int] = None
    expiry_date: Optional[Union[str, int]] = None
    password: Optional[str] = None
    confirm_password: Optional[str] = None  
    month : Optional[str] = None

  
class UpdatePassword(SQLModel):
    password: Optional[str] = None      
    
class PromptTypeBase(SQLModel):
    prompt_type : str = Field(nullable=False,default=None)
    
class PromptType(PromptTypeBase,table = True):
    __tablename__ = "prompt_type"
    id : int = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    
class PromptTypeCreate(PromptTypeBase):
    pass         



class UserExistenceCheck(BaseModel):
    mobile_number: Optional[int] = None  
    email: Optional[str] = None
    