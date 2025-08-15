from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime
from sqlalchemy import Column, DateTime, Text , BigInteger
from pydantic import validator
from datetime import date
from sqlalchemy import JSON, Column,DateTime
from sqlalchemy import Text
from typing import Any
from typing import Any, Dict, List # Make sure you have these imports

class ProductQuantity(BaseModel):
    product_id: str
    quotation_product_id: str
    manufacture_quantity: str
    available_quantity: str
    quantity: str
    @validator("*", pre=True)
    def force_str(cls, v):
        return str(v)


class ProjectManagerOrderBase(SQLModel):
    admin_id : str = Field(nullable=False,default=0)
    emplpoyee_id :Optional[str] = Field(nullable=False,default=None)
    customer_name : str = Field(nullable=False,default=None)
    customer_email_id : str = Field(nullable=False,default=None)
    customer_company : str = Field(nullable=False,default=None)
    customer_contact : str = Field(nullable=False,default=None)
    order_id : str = Field(nullable=False,default=None)
    product_id : str = Field(nullable=False,default=None)
    new_quantity : str = Field(nullable=False,default=None)
    request_date : Optional[str] = Field(nullable=True,default=date.today())
    sales_persone_name : str = Field(nullable=True,default=None)
    upload_docs : str = Field(nullable=True,default=None)
    city : Optional[str] = Field(nullable=True,default=None)
    shipping_address_state : Optional[str] = Field(nullable=True,default=None)
    shipping_address : Optional[str] = Field(nullable=True,default=None)
    shipping_address_pincode : Optional[str] = Field(nullable=True,default=None)
    status : Optional[str] = Field(nullable=True,default=None)
    country : Optional[str] = Field(nullable=True,default=None)
    subject : Optional[str] = Field(nullable=True,default=None)
    order_by: Optional[str] = Field(nullable=True,default=None)
    qr_code:  Optional[str] = Field(nullable=True,default=None)
    is_stage_clear: bool = Field(default=False, nullable=True)
    stage_status: Optional[str] = Field(nullable=True,default="Pending")
    series: str = Field(nullable=True,default=None)
    manual_sale_order_id : str = Field(nullable=True,default=None)
    lead_id: Optional[str] = Field(default=True, nullable=True)
    quotation_id: Optional[str] = Field(nullable=True, default=None)

    hold_by_name: Optional[str] = Field(nullable=True,default=None)
    hold_remark: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )
    hold_re_status: Optional[str] = Field(nullable=True,default="Pending")
    date_of_hold :Optional[str] = Field(nullable=True,default=None)

    
    created_by_type : Optional[str] = Field(nullable=True,default=None)
    admin_emp_id : Optional[str] = Field(nullable=True,default=None)

    updated_by_type : Optional[str] = Field(nullable=True,default=None)
    updated_admin_emp_id : Optional[str] = Field(nullable=True,default=None)

    challan_status: Optional[int] = Field(nullable=True,default=0)

    challan_date : Optional[str] = Field(nullable=True,default=None)
    eway_bill_no : Optional[str] = Field(nullable=True,default=None)
    dispatch_img : Optional[str] = Field(nullable=True,default=None)
    authorized_img : Optional[str] = Field(nullable=True,default=None)
    
    
    dispatch_by_type: Optional[str] = Field(nullable=True,default=None)
    dispatch_admin_emp_id : Optional[str] = Field(nullable=True,default=None)
    dispatch_at: Optional[datetime] = Field(default_factory=get_current_datetime, nullable=True)
    hold_status: Optional[str] = Field(nullable=True,default="pending")
    hold_status_remark: Optional[str] = Field(nullable=True,default=None)

    hold_by_type : Optional[str] = Field(nullable=True,default=None)
    hold_admin_emp_id : Optional[str] = Field(nullable=True,default=None)
    hold_at: datetime = Field(default=None, nullable=True)


    product_id_and_quantity: Optional[List[Dict[str, Any]]] = Field(
            default=None, sa_column=Column(JSON, nullable=True)
        )
    
    
class ProjectManagerOrder(ProjectManagerOrderBase,table = True):
    __tablename__ = "project_manager_order"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    @classmethod
    def from_request(cls, data: dict):
        # Force conversion of all product_id_and_quantity values to strings
        if "product_id_and_quantity" in data:
            serialized_items = []
            for item in data["product_id_and_quantity"]:
                if isinstance(item, dict):
                    serialized_item = {}
                    for k, v in item.items():
                        serialized_item[k] = str(v) if isinstance(v, (int, float)) else str(v) if v is not None else None
                    serialized_items.append(serialized_item)
                elif hasattr(item, "dict"):
                    serialized_items.append(
                        {k: str(v) if isinstance(v, (int, float)) else str(v) if v is not None else None for k, v in item.dict().items()}
                    )
            data["product_id_and_quantity"] = serialized_items

        # Force all non-optional, non-boolean fields to strings
        for field in cls.__fields__.values():
            if field.type_ is str and field.allow_none:
                continue
            if field.name in data and isinstance(data[field.name], (int, float)):
                data[field.name] = str(data[field.name])

        return cls(**data)

class ProductQuantityItem(BaseModel):
    product_id: str
    #quotation_product_id: Optional[str] = None
    manufacture_quantity: str
    available_quantity: str
    quantity: str


class ProjectManagerOrderCreate(BaseModel):
    admin_id : str = "0"
    emplpoyee_id :Optional[str] = None
    customer_name : str = None
    customer_email_id : str = None
    customer_company : str = None
    customer_contact : str = None
    order_id : str = None
    product_id : str = None
    new_quantity : str = None
    request_date : Optional[str] = date.today()
    sales_persone_name : str = None
    upload_docs : str = None
    city : Optional[str] = None
    shipping_address_state : Optional[str] = None
    shipping_address : Optional[str] = None
    shipping_address_pincode : Optional[str] = None
    status : Optional[str] = None
    country : Optional[str] = None
    subject : Optional[str] = None
    order_by: Optional[str] = None
    qr_code:  Optional[str] = None
    manual_sale_order_id:  Optional[str] = None
    series:  Optional[str] = None
    is_stage_clear: bool = False
    stage_status: Optional[str] = "Pending"
    
    lead_id: Optional[str] = None
    quotation_id: Optional[str] = None
    
    convert_status: Optional[str] = "Pending"

    hold_by_name: Optional[str] = None
    hold_remark: Optional[str] = None
    hold_re_status: Optional[str] = "Pending"
    date_of_hold :Optional[str] = None
    product_id_and_quantity: Optional[List[ProductQuantityItem]] = None


class ProjectManagerOrderRead(ProjectManagerOrderBase):
    id : int
    
class StatusUpdate(SQLModel):
    status: Optional[str] = None

class UpdateHoldStatus(SQLModel):
    admin_id: str
    employee_id: Optional[str] = None
    id: int 
    hold_re_status: Optional[str] = None
    hold_remark: Optional[str] = None
    date_of_hold: Optional[str] = None


class FetchOrdersRequest(BaseModel):
    admin_id: str
    employee_id: Optional[str] = None
    availability: Optional[str] = None
    order_id: Optional[str] = None
    is_stage_clear: Optional[bool] = None
    status: Optional[str] = None
    product_type: Optional[str] = None
    from_date: Optional[date] = None
    to_date: Optional[date] = None
    dispatch_at: Optional[date] = None
    
    @validator('dispatch_at', pre=True)
    def parse_dispatch_at(cls, value):
        if value in ("", None):
            return None
        try:
            return datetime.strptime(value, "%d-%m-%Y").date()
        except ValueError:
            raise ValueError("dispatch_at must be in format dd-mm-yyyy")

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
        
    
    

class UpdateStageStatusRequest(BaseModel):
    admin_id: Optional[str] = None
    employee_id: Optional[str] = None
    order_id: Optional[str] = None
    status: Optional[str] = None
    hold_status: Optional[str] = None
    hold_status_remark: Optional[str] = None
    challan_date : Optional[str] =None
    eway_bill_no : Optional[str] =None
    dispatch_img : Optional[str] =None
    authorized_img : Optional[str] =None


class AccepetIntentryQuantity(SQLModel):
    projectmanager_id: str
    product_id: Optional[str] = None
    productquantity: Optional[str] = None






