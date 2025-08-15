from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime

class BankBase(SQLModel):
    admin_id : str = Field(nullable=False,default=None)
    employee_id : Optional[str] = Field(nullable=False,default=None)
    bank_name : Optional[str] = Field(nullable=False,default=None)
    account_holder_name : Optional[str] = Field(nullable=True,default=None)
    branch : Optional[str] = Field(nullable=False,default=None)
    account_number : Optional[str] = Field(nullable=False,default=None)
    ifsc_code : Optional[str] = Field(nullable=False,default=None)
    is_default: bool = Field(default=False)

class Bank(BankBase,table = True):
    __tablename__ = "bank"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class BankCreate(BankBase):
    pass

class BankRead(BankBase):
    id : int



class BankListRequest(BaseModel):
    admin_id: str
    employee_id: Optional[str] = None 
    
    
    


class BankUpdateRequest(BaseModel):
    id: int
    admin_id: str
    employee_id: Optional[str] = None
    account_holder_name : Optional[str] = None
    bank_name: Optional[str] = None
    branch: Optional[str] = None
    account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    is_default: Optional[str] = None

class BankDeleteRequest(BaseModel):
    id: int
    admin_id: str