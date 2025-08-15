from sqlmodel import SQLModel,Field
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from src.parameter import get_current_datetime
from sqlalchemy import Column, DateTime, Text , BigInteger

class InventoryOutwardRemarkBase(SQLModel):
    admin_id : str = Field(nullable=True,default="0")
    emplpoyee_id :Optional[str] = Field(nullable=True,default=None)
    type : Optional[str] = Field(nullable=True,default=None)
    InventoryOutward_id : Optional[str] = Field(nullable=True,default=None)
    
    add_remark: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )
    
class InventoryOutwardRemark(InventoryOutwardRemarkBase,table = True):  
    __tablename__ = "inventory_outward_remark"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class InventoryOutwardRemarkCreate(BaseModel):
    admin_id: str = None
    employee_id: Optional[str] = None
    type: Optional[str] = None
    InventoryOutward_id: Optional[str] = None
    add_remark: Optional[str] = None
    
