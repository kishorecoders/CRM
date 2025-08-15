from sqlmodel import SQLModel, Field, Relationship
from pydantic import UUID4
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime


class SettingFilesBase(SQLModel):
    settings_id: int = Field(nullable=False, default=None)
    file_path: str = Field(nullable=False, default=None)


class SettingFiles(SettingFilesBase, table=True):
    __tablename__ = "setting_files"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)


class SettingFilesCreate(SettingFilesBase):
    pass


class SettingFilesRead(SettingFilesBase):
    id: int
