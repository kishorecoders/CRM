from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime

class OcrBase(SQLModel):
    admin_id : str = Field(nullable=False,default=None)
    employe_id : Optional[str] = Field(nullable=False,default=None)
    company_name : str = Field(nullable=False,default=None)
    mobile_number_1 : str = Field(nullable=False,default=None)
    mobile_number_2 : str = Field(nullable=False,default=None)
    name : Optional[str] = Field(nullable=False,default=None)
    gmail : Optional[str] = Field(nullable=False,default=None)
    address1 : Optional[str] = Field(nullable=True,default=None)
    address2 : Optional[str] = Field(nullable=True,default=None)
    address3 : Optional[str] = Field(nullable=False,default=None)
    discription : Optional[str] = Field(nullable=False,default=None)
    image : Optional[str] = Field(nullable=False,default=None)


class Ocr(OcrBase,table = True):
    __tablename__ = "ocr"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class OcrCreate(OcrBase):
    pass

class OcrRead(OcrBase):
    id : int