from sqlmodel import SQLModel, Field, Relationship
from pydantic import UUID4
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime
from sqlalchemy import Column, DateTime, Text , BigInteger


class DeliveryChallanBase(SQLModel):
    admin_id: str = Field(nullable=True, default=None)
    employee_id: str = Field(nullable=True, default=None)
    product_id: str = Field(nullable=True, default=None)
    vendor_id: str = Field(nullable=True, default=None)
    company_name: str = Field(nullable=True, default=None)
    kindely_atention: str = Field(nullable=True, default=None)

    address: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )    
    
    kindely_atention: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )
    gst_no: str = Field(nullable=True, default=None)
    mobile_number: str = Field(nullable=True, default=None)
    vehicle_number: str = Field(nullable=True, default=None)
    status: str = Field(nullable=True, default=None)
    comment_mark: str = Field(nullable=True, default=None)

    comment_mark: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )    

    file_path : Optional[str] = Field(nullable=True,default=None)
    file_ext: Optional[str] = Field(nullable=True,default=None)

    inventryoutword_id: Optional[str] = Field(nullable=True,default=None)

    created_by_type : Optional[str] = Field(nullable=True,default=None)
    admin_emp_id : Optional[str] = Field(nullable=True,default=None)

    updated_by_type : Optional[str] = Field(nullable=True,default=None)
    updated_admin_emp_id : Optional[str] = Field(nullable=True,default=None)

    chalan_type : Optional[str] = Field(nullable=True,default=None)
    order_id : Optional[str] = Field(nullable=True,default=None)




class DeliveryChallan(DeliveryChallanBase, table=True):
    __tablename__ = "delivery_challan"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=True)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=True)


class DeliveryChallanCreate(BaseModel):
    admin_id: str = None
    employee_id: str = None
    product_id: str = None
    vendor_id: str = None
    company_name: str = None
    kindely_atention: str = None
    address: str = None
    gst_no: str = None
    mobile_number: str = None
    vehicle_number: str = None
    status: str = None
    comment_mark: str = None
    file_path : Optional[str] = None
    file_ext: Optional[str] = None
    inventryoutword_id: Optional[str] = None
    chalan_type : Optional[str]  = None
    order_id : Optional[str] = None


class DeliveryChallanRead(DeliveryChallanBase):
    admin_id: int



class DeliveryChallanRequest(BaseModel):
    admin_id: int
    employee_id: Optional[str] = None
    date: Optional[str] = None  



class UpdateChallanRequest(BaseModel):
    admin_id: int
    employee_id :Optional[str] = None
    
    vehicle_number : Optional[str] = None
    mobile_number : Optional[str] = None
    address : Optional[str] = None
    kindely_atention : Optional[str] = None
    company_name : Optional[str] = None
    
    delivery_challan_id: int
    file_path: Optional[str] = None
    file_ext: Optional[str] = None
    comment_mark: Optional[str] = None


class updatestatus(BaseModel):
    admin_id: int
    product_id : Optional[str] = None
    employee_id : Optional[str] = None
    inventryoutword_id : Optional[int] = None
    status : Optional[str] = None

class GetDispatch(BaseModel):
    admin_id: int
    employee_id : Optional[str] = None
    product_id : Optional[str] = None



