from sqlmodel import SQLModel, Field, Relationship
from pydantic import UUID4
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime
from sqlalchemy import Column, DateTime, Text , BigInteger

class PaymentTermBase(SQLModel):
    admin_id: int = Field(nullable=False, default=None)
    type: str = Field(nullable=False, default=None)
    file_path: Optional[str] = Field(nullable=True, default=None)
    content: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=False)  # <-- set nullable here
    )

class PaymentTerm(PaymentTermBase, table=True):
    __tablename__ = "payment_term"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)


class PaymentTermCreate(PaymentTermBase):
    pass


class PaymentTermRead(PaymentTermBase):
    admin_id: int


class UpdatePaymentTermRequest(BaseModel):
    admin_id: int
    payment_term_id: int
    type: str = None
    file_path: Optional[str] = None
    content: str = None



class PaymentTermDelete(BaseModel):
    admin_id: int
    payment_term_id: int
