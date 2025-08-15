from sqlmodel import SQLModel, Field, Relationship
from pydantic import UUID4
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime,LargeBinary
from src.parameter import get_current_datetime
from sqlmodel import Field, SQLModel, Column
from sqlalchemy import Text
from sqlalchemy.dialects.mysql import LONGBLOB
class EmployeeFilesBase(SQLModel):
    employee_id: int = Field(nullable=False, default=None)
    admin_id: int = Field(nullable=False, default=None)
    
    image_path: Optional[bytes] = Field(
        default=None,
        sa_column=Column(LargeBinary(length=4294967295), nullable=True)
    )
    
    file_path: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)
    )
    
    medical_file_path: Optional[bytes] = Field(
        default=None,
        sa_column=Column(LargeBinary(length=4294967295), nullable=True)
    )
    m_file_name: Optional[str] = Field(nullable=True, default=None)

    type: str = Field(nullable=False, default=None)


class EmployeeFiles(EmployeeFilesBase, table=True):
    __tablename__ = "employee_files"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)


class EmployeeFilesCreate(BaseModel):
    employee_id: int = None
    admin_id: int = None
    
    image_path: Optional[bytes]
    
    file_path: Optional[str] = None
    medical_file_path: Optional[bytes]
    m_file_name: Optional[str] = None
    type: str = None



class EmployeeFilesRead(EmployeeFilesBase):
    id: int


class FetchEmployeeFilesRequest(BaseModel):
    admin_id: Optional[int] = None
    employee_id: Optional[int] = None