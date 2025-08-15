from pydantic import Json
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import time, datetime
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, UniqueConstraint

class TimeConfigBase(SQLModel):
    admin_id: int
    shift_name: str
    start_time_1st: str = Field(default="")
    end_time_1st: str = Field(default="")
    in_time_1st: str = Field(default="")
    out_time_1st: str = Field(default="")
    late_time_1st: str = Field(default="")
    lunch_time_start_1st: str = Field(default="")
    lunch_time_end_1st: str = Field(default="")
    lunch_time_interval_1st: str = Field(default="")
    start_time_2nd: str = Field(default="")
    end_time_2nd: str = Field(default="")
    in_time_2nd: str = Field(default="")
    out_time_2nd: str = Field(default="")
    late_time_2nd: str = Field(default="")
    lunch_time_start_2nd: str = Field(default="")
    lunch_time_end_2nd: str = Field(default="")
    lunch_time_interval_2nd: str = Field(default="")
    start_time_3rd: str = Field(default="")
    end_time_3rd: str = Field(default="")
    in_time_3rd: str = Field(default="")
    out_time_3rd: str = Field(default="")
    late_time_3rd: str = Field(default="")
    lunch_time_start_3rd: str = Field(default="")
    lunch_time_end_3rd: str = Field(default="")
    lunch_time_interval_3rd: str = Field(default="")
    start_time_general: str = Field(nullable=True,default="")
    end_time_general: str = Field(nullable=True,default="")
    in_time_general: str = Field(nullable=True,default="")
    out_time_general: str = Field(nullable=True,default="")
    late_time_general: str = Field(nullable=True,default="")
    lunch_time_start_general: str = Field(nullable=True,default="")
    lunch_time_end_general: str = Field(nullable=True,default="")
    lunch_time_interval_general: str = Field(nullable=True,default="")
    weekly_holidays: str = Field(default="")
    late_mark_1st: str = Field(nullable=True,default="")
    late_mark_2nd: str = Field(nullable=True,default="")
    late_mark_3rd: str = Field(nullable=True,default="")
    late_mark_general: str = Field(nullable=True,default="")
    
    shift1_weekly_holidays: str = Field(nullable=True,default="")
    shift2_weekly_holidays: str = Field(nullable=True,default="")
    shift3_weekly_holidays: str = Field(nullable=True,default="")
    
class TimeConfig(TimeConfigBase, table=True):
    __tablename__ = "time_config"


    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class Latemark(BaseModel):
    select_type : Optional[str] = None
    content : Optional[str] = None
    type : Optional[str] = None


class TimeConfigCreate(TimeConfigBase):
    pass


class TimeConfigRead(TimeConfigBase):
    id: int
    created_at: datetime
    updated_at: datetime




class AdminIDRequest(BaseModel):
    admin_id: int

