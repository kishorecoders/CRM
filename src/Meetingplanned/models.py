from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime
from sqlalchemy import Column, DateTime, Text , BigInteger

class MeetingplannedBase(SQLModel):
    admin_sales_id : int = Field(nullable=False,default=0)
    employe_id : str = Field(nullable=False,default=0)
    meeting_date : date = Field(nullable=False,default=date.today())
    meeting_time : Optional[str] = Field(nullable=True,default=0)
    meeting_status : Optional[str] = Field(nullable=True,default=None)
    


    meeting_discription: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )
        

    cancel_remark : Optional[str] = Field(nullable=True,default=None)
    meeting_type : Optional[str] = Field(nullable=True,default=None)
    meeting_link : Optional[str] = Field(nullable=True,default=None)

    admin_id : Optional[str] = Field(nullable=True,default=None)
    admin_emp_id : Optional[str] = Field(nullable=True,default=None)
    created_by_type : Optional[str] = Field(nullable=True,default=None)


class Meetingplanned(MeetingplannedBase,table = True):
    __tablename__ = "meeting_planned"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class MeetingplannedCreate(MeetingplannedBase):
    pass
    
    #admin_emp_id :Optional[str] = None
    #created_by_type :Optional[str] = None



class MeetingplannedRead(MeetingplannedBase):
    id : int
    
    
class MeetingplannedReadRequest(BaseModel):
     lead_id: Optional[str] = None
     admin_id: Optional[str] = None
     employee_id: Optional[str] = None
     meeting_status: Optional[str] = None
     name: Optional[str] = None





