from sqlmodel import SQLModel,Field,Relationship
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from src.parameter import get_current_datetime
from pydantic import BaseModel, validator



class FileItem(BaseModel):
    file_name: str
    file_path: str

class ProjectManagerResourseFileBase(SQLModel):
    admin_id : int = Field(nullable=False,default=None)
    emp_id : Optional[int] = Field(nullable=False,default=None)
    lead_id : Optional[str] = Field(nullable=False,default=None)
    quotation_id : Optional[str] = Field(nullable=False,default=None)
    file_path : Optional[str] = Field(nullable=True,default=None)

class ProjectManagerResourseFile(ProjectManagerResourseFileBase,table = True):
    __tablename__ = "ProjectManagerResourseFile"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)




class ProjectManagerResourseFileRead(BaseModel):
    admin_id:Optional[str] = None
    quotation_id:Optional[str] = None

class ProjectManagerResourseFileDelete(BaseModel):
    id:Optional[int] = None