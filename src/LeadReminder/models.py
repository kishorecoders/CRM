from sqlmodel import SQLModel, Field, Relationship
from pydantic import UUID4
from datetime import datetime, date
from typing import Optional, List, Union
from pydantic import BaseModel, validator
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime


class LeadReminderBase(SQLModel):
    admin_id: int = Field(nullable=False, default=None)
    employee_id: str = Field(nullable=False, default=None)
    Lead_id: str = Field(nullable=False, default=None)
    reminder_time: datetime = Field(nullable=False, default=None)
    about_reminder: str = Field(nullable=True, default=None)
    status: str = Field(nullable=True, default=None)

    


class LeadReminder(LeadReminderBase, table=True):
    __tablename__ = "lead_reminder"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)


class LeadReminderCreate(BaseModel):
    admin_id: int
    employee_id: str
    Lead_id: str
    reminder_time: datetime  
    about_reminder: str
    status: str

    @validator("reminder_time", pre=True, always=True)
    def parse_reminder_time(cls, value):
        try:
           
            return datetime.strptime(value, "%d-%m-%Y %I:%M %p")
        except ValueError:
            raise ValueError("Invalid date format. Expected format: 'DD-MM-YYYY HH:MM AM/PM'")
        

class LeadReminderFilterRequest(BaseModel):
    admin_id: int
    employee_id: Optional[str] = None 




class UpdateReminderRequest(BaseModel):
    reminder_id: int
    admin_id: Optional[int]
    employee_id: Optional[str]
    Lead_id: Optional[str]
    reminder_time: Optional[Union[str, datetime]]  
    about_reminder: Optional[str]
    status: Optional[str]

    @validator("reminder_time", pre=True, always=True)
    def parse_reminder_time(cls, value):
        if isinstance(value, str): 
            try:
                return datetime.strptime(value, "%d-%m-%Y %I:%M %p")
            except ValueError:
                raise ValueError("Invalid date format. Expected format: 'DD-MM-YYYY HH:MM AM/PM'")
        return value  


class DeleteReminderRequest(BaseModel):
    reminder_id: int
    admin_id: int
    employee_id: int