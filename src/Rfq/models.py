from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime
from typing import Optional
import os
import base64
import uuid

class RfqBase(SQLModel):
    admin_id : str = Field(nullable=False,default=None)
    employee_id : Optional[str] = Field(nullable=True,default=None)
    req_id : Optional[str] = Field(nullable=True,default=None)
    rfq_id : Optional[str] = Field(nullable=True,default=None)
    req_number: Optional[str] = Field(nullable=True,default=None)
    series_id: Optional[str] = Field(nullable=True, default=None)
    req_date : Optional[str] = Field(nullable=True, default=None)
    vendor_id :  Optional[str] = Field(nullable=True, default=None)
    quotation_due_date : Optional[str] = Field(nullable=True, default=None)
    request_by :  Optional[str] = Field(nullable=True, default=None)
    file_path  : Optional[str] = Field(nullable=True, default=None)
    file_name : Optional[str] = Field(nullable=True, default=None)
    
class Rfq(RfqBase,table = True):
    __tablename__ = "rfq"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class RfqCreate(RfqBase):
    pass

class RfqRead(RfqBase):
    id : int
    
    
    
    
class RfqFilterRequest(BaseModel):
    admin_id: str
    employee_id: Optional[str] = None
    
    
    
    
class RfqUpdate(RfqBase):
    id: int  
    
    
    
    
class RfqFileUploadRequest(BaseModel):
    rfq_id: str
    filename: str
    base64_file: str

class RfqEmail(BaseModel):
    rfq_id: str
    file_url: str






