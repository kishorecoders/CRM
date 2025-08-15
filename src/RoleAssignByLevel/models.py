from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime
from sqlmodel import SQLModel, Field, Column, JSON



class RoleAssignByLevelBase(SQLModel):
    admin_id : int = Field(nullable=False,default=0)
    employe_id_from : str = Field(nullable=False,default=0)
    employe_id_to : Optional[List[str]] = Field(default_factory=list, sa_column=Column(JSON))
    
    
class RoleAssignByLevel(RoleAssignByLevelBase,table = True):
    __tablename__ = "employee_assign_by_level"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class RoleAssignByLevelCreate(RoleAssignByLevelBase):
    pass

class RoleAssignByLevelRead(RoleAssignByLevelBase):
    id : int    