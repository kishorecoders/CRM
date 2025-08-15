from sqlmodel import SQLModel, Field, Relationship
from pydantic import UUID4
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime
from sqlalchemy import Column, DateTime, Text , BigInteger


class BrouncherBase(SQLModel):
    admin_id: int = Field(nullable=False, default=None)
    categories: str = Field(nullable=False, default=None)
    files_path: str = Field(nullable=False, default=None)
    pdf_thumbnail: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=False)  # <-- set nullable here
    )

class Brouncher(BrouncherBase, table=True):
    __tablename__ = "brouncher"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)


class BrouncherCreate(BrouncherBase):
    pass


class BrouncherRead(BrouncherBase):
    admin_id: int



class BrouncherDelete(BaseModel):
    admin_id: int
    brouncher_id: int
