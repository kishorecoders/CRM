from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime

class AdminAssignRoleEmployeeBase(SQLModel):
    admin_id : int = Field(nullable=False,default=0)
    role_id : int = Field(nullable=False,default=0)
    employe_id : Optional[str] = Field(nullable=True,default=None)
    status : Optional[str] = Field(nullable=True,default=0)
    asign_employe_id : Optional[str] = Field(nullable=False,default="0")

class AdminAssignRoleEmployee(AdminAssignRoleEmployeeBase,table = True):
    __tablename__ = "admin_assign_role"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class AdminAssignRoleEmployeeCreate(AdminAssignRoleEmployeeBase):
    pass

class AdminAssignRoleEmployeeRead(AdminAssignRoleEmployeeBase):
    id : int    