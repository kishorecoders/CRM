from sqlmodel import SQLModel, Field, Column
from typing import Optional, List
from datetime import datetime
from src.parameter import get_current_datetime
from pydantic import BaseModel, root_validator
from sqlalchemy import Column ,  Text , LargeBinary



class DailyReportBase(SQLModel):
    admin_id: Optional[str] = Field(nullable=True, default=None)
    employee_id: Optional[str] = Field(nullable=True, default=None)
    task_id: Optional[str] = Field(nullable=True, default=None)
    title: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  
    )
    file: Optional[str] = Field(nullable=True, default=None)
    status: Optional[str] = Field(nullable=True, default=None)
    
class DailyReport(DailyReportBase, table=True):
    __tablename__ = "dailyreport"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class ReportRequestCreate(BaseModel):
    admin_id: Optional[str] = None
    employee_id: Optional[str] = None
    task_id: Optional[str] = None
    title: Optional[str] = None
    file: Optional[str] = None
    status: Optional[str] = None
    
class ReportRequestCreatenew(BaseModel):
    task_id: Optional[str] = None
    title: Optional[str] = None
    file: Optional[str] = None
    status: Optional[str] = None

class ReportRequestCreatelist(BaseModel):
    admin_id: Optional[int] = None
    employee_id: Optional[str] = None
    reports: List[ReportRequestCreatenew]

class ReportRequestGet(BaseModel):
    admin_id: Optional[int] = None
    employee_id: Optional[str] = None
    task_id: Optional[str] = None


class ReportRequestDelete(BaseModel):
    admin_id: Optional[int] = None
    employee_id: Optional[str] = None
    report_id: Optional[str] = None

class ReportRequestUpdate(BaseModel):
    admin_id: Optional[int] = None
    employee_id: Optional[str] = None
    report_id: Optional[str] = None
    task_id: Optional[str] = None




