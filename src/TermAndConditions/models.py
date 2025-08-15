from sqlmodel import SQLModel, Field, Relationship
from pydantic import UUID4
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime
from sqlalchemy import Column, DateTime, Text , BigInteger

class TermAndConditionBase(SQLModel):
    admin_id: int = Field(nullable=False, default=None)
    type: str = Field(nullable=False, default=None)
    file_path: str = Field(nullable=False, default=None)


    content: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=False)  # <-- set nullable here
    )

class TermAndCondition(TermAndConditionBase, table=True):
    __tablename__ = "term_and_conditions"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)


class ContentItem(BaseModel):
    content: str

class TermAndConditionCreate(TermAndConditionBase):
    admin_id: int
    type: str
    file_path: str
    content: List[ContentItem]

class TermAndConditionRead(BaseModel):
    admin_id: int


class UpdateTermAndConditionRequest(BaseModel):
    admin_id: int
    term_and_condition_id: int
    type: str = None
    file_path: str = None
    content: str = None



class TermAndConditionDelete(BaseModel):
    admin_id: int
    term_and_condition_id: int
