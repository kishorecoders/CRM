from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime

class PublicHolidayBase(SQLModel):
    #admin_id : str = Field(sa_column=Column("admin_id", nullable=False))
    admin_id : str =  Field(nullable=False,default=None)
    event_name : Optional[str] = Field(nullable=False,default=None)
    event_date : datetime = Field(nullable=False)
   

class PublicHoliday(PublicHolidayBase,table = True):
    __tablename__ = "public_holiday"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)


class PublicHolidayCreate(BaseModel):
    admin_id: str
    event_name: str
    event_date: str  


class PublicHolidayRead(PublicHolidayBase):
    id : int


class PublicHolidayAdminRequest(BaseModel):
    admin_id: str


class PublicHolidayDeleteRequest(BaseModel):
    admin_id: str
    public_holiday_id: int
