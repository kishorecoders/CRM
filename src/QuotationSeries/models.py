from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime

class QuotationSeriesBase(SQLModel):
    admin_id : str = Field(nullable=False,default=None)
    employee_id : Optional[str] = Field(nullable=False,default=None)
    series_type : Optional[str] = Field(nullable=False,default=None)
    series_name : Optional[str] = Field(nullable=False,default=None)
    quotation_formate : Optional[str] = Field(nullable=False,default=None)
   
    branch_name : Optional[str] = Field(nullable=False,default=None)
    is_default: bool = Field(default=False)
    
    
class QuotationSeries(QuotationSeriesBase,table = True):
    __tablename__ = "quotation_series"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class QuotationSeriesCreate(QuotationSeriesBase):
    pass

class QuotationSeriesRead(QuotationSeriesBase):
    id : int



class QuotationSeriesRequest(BaseModel):
    admin_id: str
    employee_id: Optional[str] = None 
    series_type: Optional[str] = None 
    series_name: Optional[str] = None 



class QuotationSeriesUpdateRequest(BaseModel):
    id: int
    admin_id: str
    employee_id: Optional[str] = None
    series_type: Optional[str] = None
    series_name: Optional[str] = None
    quotation_formate: Optional[str] = None
    branch_name: Optional[str] = None
    is_default: Optional[str] = None


class QuotationSeriesDeleteRequest(BaseModel):
    admin_id: str
    series_id: int
    
    
    
class QuotationSeriesDetailRequest(BaseModel):
    admin_id: str
    series_type: str
    series_name: str