from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime
from sqlmodel import SQLModel, Field, Column, JSON



class EmployeeAssignRequestBase(SQLModel):
    admin_id : int = Field(nullable=False,default=0)
    employee_id : Optional[str] = Field(nullable=True,default=None)

    employe_id_from : str = Field(nullable=False,default=0)
    employe_id_to : Optional[List[str]] = Field(default_factory=list, sa_column=Column(JSON))
    status : str = Field(nullable=False,default=0)
    
    
class EmployeeAssignRequest(EmployeeAssignRequestBase,table = True):
    __tablename__ = "employee_asssign_request"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class EmployeeAssignRequestCreate(EmployeeAssignRequestBase):
    pass

class EmployeeAssignRequestRead(EmployeeAssignRequestBase):
    id : int    



class EmployeeAssignRequestFilter(BaseModel):
    admin_id: Optional[int] = None
    employe_id_from: Optional[str] = None



class UpdateStatusRequest(BaseModel):
    admin_id: int
    employee_id: Optional[str] = None

    request_id: int
    status: str
    remark: Optional[str] = None



class DeleteRequest(BaseModel):
    admin_id: int
    from_id: str
    request_id: int
