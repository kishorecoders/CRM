from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime

from sqlalchemy import Column, DateTime, Text , BigInteger
from sqlmodel import SQLModel, Field, Column, JSON

class ActivityCommentBase(SQLModel):
    activity_id : str = Field(nullable=False,default=0)
    admin_emp_id : str = Field(nullable=False,default=0)
    #activity_comment : str = Field(nullable=False,default=0)
    
    activity_comment: Optional[str] = Field(
        default=0,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )

    
    activity_comment_id : str = Field(nullable=False,default=0)
    type : Optional[str] = Field(nullable=True,default=0)
    activity_docs : Optional[str] = Field(nullable=True,default=None)
    name : Optional[str] = Field(nullable=True,default=None)
    


class ActivityComment(ActivityCommentBase,table = True):
    __tablename__ = "activity_comment"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class ActivityCommentCreate(ActivityCommentBase):
    pass

class ActivityCommentRead(ActivityCommentBase):
    id : int



class ActivityCommentRequest(BaseModel):
    activity_id: str



class ActivityCommentResponse(BaseModel):
    id: int
    activity_id: str
    admin_emp_id: str
    activity_comment_id: str
    activity_comment: str
    type: Optional[str]
    activity_docs: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True




class DeleteActivityCommentRequest(BaseModel):
    activity_id: str
    activity_comment_id: str