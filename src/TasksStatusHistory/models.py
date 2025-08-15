from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from src.parameter import get_current_datetime
from sqlalchemy import Column, DateTime, Text , BigInteger

class TaskStatusHistoryBase(SQLModel):
    admin_id: Optional[str] = Field(nullable=True)
    emp_id_from: Optional[str] = Field(nullable=True)
    task_id: Optional[str] = Field(nullable=True)
    task_status: Optional[str] = Field(nullable=True)
    created_by_type: Optional[str] = Field(nullable=True)
    admin_emp_id: Optional[str] = Field(nullable=True)
    task_history_remark: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )


class TaskStatusHistory(TaskStatusHistoryBase, table=True):
    __tablename__ = "task_status_history"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

