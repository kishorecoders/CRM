from sqlmodel import SQLModel,Field
from datetime import datetime
from typing import Optional
from src.parameter import get_current_datetime

class FacebookLeadBase(SQLModel):
    id: Optional[int] = Field(nullable=True, default=None)
    form_id: str = Field(nullable=True, default=None)
    leadgen_id: str = Field(nullable=True, default=None)
    field_data: str = Field(nullable=True, default=None)  

class FacebookLead(FacebookLeadBase, table=True):
    __tablename__ = "FacebookLead"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
