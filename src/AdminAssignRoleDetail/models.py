from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime

class AdminAssignRoleDetailsBase(SQLModel):
    admin_id : int = Field(nullable=False,default=0)
    employe_id : Optional[str] = Field(nullable=True,default=None)
    current_role_id : Optional[str] = Field(nullable=True,default=None)
    switched_role_id : Optional[str] = Field(nullable=True,default=None)
    status : Optional[str] = Field(nullable=True,default=None)
    admin_asign_id : Optional[str] = Field(nullable=True,default=None)

class AdminAssignRoleDetails(AdminAssignRoleDetailsBase,table = True):
    __tablename__ = "admin_assign_role_details"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    started_at: Optional[datetime] = Field(default=None, nullable=True)

class AdminAssignRoleEmployeeRead(BaseModel):
    id : int    