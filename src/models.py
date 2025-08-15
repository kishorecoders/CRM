from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship


class ActiveMixin(SQLModel):
    is_active: Optional[bool] = Field(default=True)


class CreatedTimestampMixin(SQLModel):
    created_by: Optional[str] = Field(default="test")
    created_date: Optional[datetime] = Field(default="now()")


class ModifiedTimestampMixin(SQLModel):
    modified_by: Optional[str] = Field(default="test")
    modified_date: Optional[datetime] = Field(default="now()")
