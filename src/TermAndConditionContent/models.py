from sqlmodel import SQLModel, Field, Relationship
from pydantic import UUID4
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime

from sqlalchemy import Column, DateTime, Text , BigInteger

class TermAndConditionContentBase(SQLModel):
    termAndCondition_id: int = Field(nullable=False, default=None)
    content: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=False)  # <-- set nullable here
    )
class TermAndConditionContent(TermAndConditionContentBase, table=True):
    __tablename__ = "term_and_conditions_content"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)


