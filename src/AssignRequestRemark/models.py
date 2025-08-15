from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime
from sqlmodel import SQLModel, Field, Column, JSON

from sqlalchemy import Column, DateTime, Text , BigInteger


class AssignRequestRemarkBase(SQLModel):
    admin_id : Optional[str] = Field(nullable=True,default=None)
    employee_id : Optional[str] = Field(nullable=True,default=None)

    employee_id_from : Optional[str] = Field(nullable=True,default=None)
    employee_id_to : Optional[str] = Field(nullable=True,default=None)
    employee_asssign_request_id : Optional[str] = Field(default=None, nullable=True)
    status : Optional[str] = Field(nullable=True,default=None)
    remark: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )

class AssignRequestRemark(AssignRequestRemarkBase,table = True):
    __tablename__ = "assign_request_remark"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

