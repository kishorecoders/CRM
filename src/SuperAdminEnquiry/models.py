from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime

class SuperAdminEnquiryBase(SQLModel):
    enquiry_source : str = Field(nullable=False,default=0)
    enquiry_user_name : str = Field(nullable=False,default=0)
    enquiry_subject : Optional[str] = Field(nullable=False,default=0)
    support_request : Optional[str] = Field(nullable=False,default=0)
    replay_request : Optional[str] = Field(nullable=False,default=0)
    status : Optional[int] = Field(nullable=False,default=0)
    

class SuperAdminEnquiry(SuperAdminEnquiryBase,table = True):
    __tablename__ = "super_admin_enquiry"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class SuperAdminEnquiryCreate(SuperAdminEnquiryBase):
    pass

class SuperAdminEnquiryRead(SuperAdminEnquiryBase):
    id : int