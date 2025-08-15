from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime

class StoreManagerServiceBase(SQLModel):
    admin_id : str = Field(nullable=False,default=0)
    emplpoyee_id :Optional[str] = Field(nullable=False,default=0)
    service_tital : str = Field(nullable=False,default=0)
    service_code : str = Field(nullable=False,default=0)
    categories : Optional[str] = Field(nullable=True,default=0)
    sub_categories : Optional[str] = Field(nullable=True,default=0)
    sac_code : Optional[str] = Field(nullable=True,default=None)
    gst_rate : Optional[str] = Field(nullable=False,default=None)
    discription : Optional[str] = Field(nullable=True,default=None)
    price_per_service : Optional[str] = Field(nullable=True,default=None)
    basis : Optional[str] = Field(nullable=True,default=None)
    milestone : Optional[str] = Field(nullable=True,default=None)
    time_required : Optional[str] = Field(nullable=True,default=None)
    unit : Optional[str] = Field(nullable=True,default=None)
    document : Optional[str] = Field(nullable=True,default=None)
    internal_manufacturing : Optional[str] = Field(nullable=True,default=None)
    
class storeManagerService(StoreManagerServiceBase,table = True):
    __tablename__ = "store_manager_service"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class storeManagerServiceCreate(StoreManagerServiceBase):
    pass

class storeManagerServiceRead(StoreManagerServiceBase):
    id : int