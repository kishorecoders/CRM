from sqlmodel import SQLModel, Field, Column
from typing import Optional, List
from datetime import datetime
from src.parameter import get_current_datetime
from pydantic import BaseModel, root_validator
from sqlalchemy import Column ,  Text , LargeBinary
from sqlalchemy import Column, DateTime, Text , BigInteger


class ChatMessageModelBase(SQLModel):
    admin_id: Optional[str] = Field(nullable=False)
    employee_id: Optional[str] = Field(nullable=False)
    task_id: Optional[str] = Field(nullable=False)
    #message: Optional[str] = Field(nullable=False)
    file_byte_data: Optional[str] = None  # Base64 encoded string for file bytes



    message: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )
    


class ChatMessageModel(ChatMessageModelBase, table=True):
    __tablename__ = "chatmessagemodel"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    
class ChatMessageModelCreate(BaseModel):
    admin_id: Optional[str] = None
    employee_id: Optional[str] = None
    task_id: Optional[str] = None
    message: Optional[str] = None
    file_byte_data: Optional[str] = None  # Base64 encoded string for file bytes

class ChatMessageModelGet(BaseModel):
    admin_id: Optional[str] = None
    employee_id: Optional[str] = None
    task_id: Optional[str] = None

