from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime

from pydantic import BaseModel, validator
from typing import Optional
from datetime import date

from pydantic import validator



class InventoryOutwardBase(SQLModel):
    admin_id : str = Field(nullable=False,default=0)
    emplpoyee_id :Optional[str] = Field(nullable=True,default=None)
    outward_datetime : datetime = Field(nullable=False,default=datetime.now())
    outward_id : Optional[str] = Field(nullable=True,default=None)
    product_id : Optional[str] = Field(nullable=True,default=None)
    order_id : Optional[int] = Field(nullable=True,default=0)
    released_to_person : Optional[str] = Field(nullable=False,default=None)
    ask_qty : Optional[str] = Field(nullable=False,default=None)
    given_qty : Optional[str] = Field(nullable=True,default=None)
    left : Optional[str] = Field(nullable=True,default=None)
    status: str = Field(nullable=True,default=None)
    
    challan_status: Optional[int] = Field(nullable=True,default=0)
    
    
    
    
    approve_by : str = Field(nullable=True,default=None)
    
    created_by_type : Optional[str] = Field(nullable=True,default=None)
    admin_emp_id : Optional[str] = Field(nullable=True,default=None)
    
    book_status:  str = Field(nullable=True,default=0)

    approve_by_type : Optional[str] = Field(nullable=True,default=None)
    approve_by_id : Optional[str] = Field(nullable=True,default=None)
    
    dispatch_status : Optional[str] = Field(nullable=True,default="Pending")
    
    
    dispatch_type :  Optional[str] = Field(nullable=True,default="Product")
    order_id_id : Optional[str] = Field(nullable=True,default=None)
    
    
    authorized_img : Optional[str] = Field(nullable=True,default=None)
    dispatch_img : Optional[str] = Field(nullable=True,default=None)
    challan_date : Optional[str] = Field(nullable=True,default=None)
    eway_bill_no : Optional[str] = Field(nullable=True,default=None)
    
    dispatch_by_type : Optional[str] = Field(nullable=True,default=None)
    dispatch_admin_emp_id : Optional[str] = Field(nullable=True,default=None)
    dispatch_created_at : Optional[str] = Field(nullable=True,default=None)

    dispatch_approve_by_type : Optional[str] = Field(nullable=True,default=None)
    dispatch_approve_by_id : Optional[str] = Field(nullable=True,default=None)
    dispatch_updated_at : Optional[str] = Field(nullable=True,default=None)
    dispatch_remark : Optional[str] = Field(nullable=True,default=None)

    today_dispatch_date : Optional[str] = Field(nullable=True,default=None) 


class InventoryOutward(InventoryOutwardBase,table = True):  
    __tablename__ = "inventory_outward"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class InventoryOutwardCreate(BaseModel):
    admin_id: str
    employee_id: Optional[str] = None
    outward_datetime: Optional[datetime] = None
    outward_id: Optional[str] = None
    product_id: Optional[str] = None
    order_id: Optional[str] = None
    released_to_person: Optional[str] = None
    ask_qty: Optional[str] = None
    given_qty: Optional[str] = None
    left: Optional[str] = None
    status: Optional[str] = None

class InventoryOutwardRead(InventoryOutwardBase):
    id : int



class UpdateStatusRequest(BaseModel):
    admin_id: str
    inventory_id: int
    status: str
    employee_id: Optional[str] = None
    
    type: Optional[str] = None
    add_remark: Optional[str] = None
    
    


class BookStatusRequest(BaseModel):
    admin_id: str
    inventory_id: int
    book_status: str
    employee_id: Optional[str] = None

    type: Optional[str] = None
    add_remark: Optional[str] = None


        
        
        
class InventoryFilterRequest(BaseModel):
    admin_id: str
    employee_id: Optional[str] = None
    status: Optional[str] = None
    outward_date: Optional[date] = None
    dispatch_status: Optional[str] = None
    from_date: Optional[date] = None   # <-- Add this
    to_date: Optional[date] = None   
    today_dispatch_date: Optional[date] = None   

    @validator('outward_date', pre=True)
    def parse_outward_date(cls, value):
        if value == "" or value is None:
            return None
        try:
            return datetime.strptime(value, "%d-%m-%Y").date()
        except ValueError:
            raise ValueError("outward_date must be in format dd-mm-yyyy")
        
    @validator('today_dispatch_date', pre=True)
    def parse_dispatch_created_at(cls, value):
        if value == "" or value is None:
            return None
        try:
            return datetime.strptime(value, "%d-%m-%Y").date()
        except ValueError:
            raise ValueError("today_dispatch_date must be in format dd-mm-yyyy")
    
    
    @validator('from_date', pre=True)
    def parse_from_date(cls, value):
        if value in ("", None):
            return None
        try:
            return datetime.strptime(value, "%d-%m-%Y").date()
        except ValueError:
            raise ValueError("from_date must be in format dd-mm-yyyy")

    @validator('to_date', pre=True)
    def parse_to_date(cls, value):
        if value in ("", None):
            return None
        try:
            return datetime.strptime(value, "%d-%m-%Y").date()
        except ValueError:
            raise ValueError("to_date must be in format dd-mm-yyyy")
        
        
class UpdateDispatchStatusRequest(BaseModel):
    admin_id: str
    inventory_id: Optional[int] = None
    dispatch_status: str
    dispatch_remark: Optional[str] = None
    employee_id: Optional[str] = None
    authorized_img: Optional[str] = None  # base64 string
    dispatch_img: Optional[str] = None    # base64 string
    challan_date: Optional[str] = None  
    eway_bill_no: Optional[str] = None 
    
    
    
    
class AddDispatchOrderRequest(BaseModel):
    admin_id: str
    order_id_id: str
    dispatch_type: str
    employee_id: Optional[str] = None
    product_id: Optional[str] = None
    ask_qty: Optional[str] = None
    given_qty: Optional[str] = None
    released_to_person: Optional[str] = None

    

