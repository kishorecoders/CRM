from sqlmodel import SQLModel, Field, Column, JSON
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from src.parameter import get_current_datetime
from pydantic import BaseModel, root_validator
from typing import List, Dict, Union


class ProjectTaskBase(SQLModel):
    admin_id: int = Field(nullable=True, default=None)
    emp_id: str = Field(nullable=True, default=None)
    customer_id: Optional[str] = Field(nullable=True, default=None)
    project_name: Optional[str] = Field(nullable=True, default=None)
    


class ProjectTask(ProjectTaskBase, table=True):
    __tablename__ = "project_tasks"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    

class ProjectCreate(BaseModel):
    admin_id: Optional[str] = None
    emp_id: Optional[str] = None
    customer_id: Optional[str] = None
    project_name: Optional[str] = None

class ProjectGet(BaseModel):
    admin_id: Optional[str] = None
    emp_id: Optional[str] = None
    project_id: Optional[str] = None
    customer_id: Optional[str] = None

class ProjectUpdate(BaseModel):
    project_id: Optional[str] = None
    customer_id: Optional[str] = None
    project_name: Optional[str] = None

class ProjectDelete(BaseModel):
    project_id: Optional[str] = None
    
    
    