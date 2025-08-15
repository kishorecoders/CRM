from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List 
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime
from pydantic import UUID4, ValidationError, validator, root_validator
import json
from sqlalchemy import Column, JSON
from sqlalchemy import Column, Text


class StoreManagerProductBase(SQLModel):
    admin_id : str = Field(nullable=False,default=0)
    emplpoyee_id :Optional[str] = Field(nullable=True,default=0)
    product_tital : str = Field(nullable=False,default=0)
    purchase_request_id : Optional[str] = Field(nullable=True,default=0)
    item_code : str = Field(nullable=False,default=0)
    categories : Optional[str] = Field(nullable=True,default=0)
    sub_categories : Optional[str] = Field(nullable=True,default=0)
    hsn_sac_code : Optional[str] = Field(nullable=True,default=None)
    gst_rate : Optional[str] = Field(nullable=True,default=None)
    discription: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )
    #discription : Optional[str] = Field(nullable=True,default=None)
    price_per_product : Optional[str] = Field(nullable=True,default=None)
    unit : Optional[str] = Field(nullable=True,default=None)
    sold_as : Optional[str] = Field(nullable=True,default=None)
    pack_of : Optional[str] = Field(nullable=True,default=None)
    steps : Optional[str] = Field(nullable=True,default=None)
    time_riquired_for_this_process : Optional[str] = Field(nullable=True,default=None)
    day : Optional[str] = Field(nullable=True,default=None)
    minimum_requuired_quantity_for_low_stock : Optional[str] = Field(nullable=True,default=None)
    document : Optional[str] = Field(nullable=True,default=None)
    opening_stock : Optional[str] = Field(nullable=True,default=None)
    internal_manufacturing : Optional[str] = Field(nullable=True,default=None)
    availability: Optional[str] = Field(nullable=True,default=None)
    Stages: Optional[str] = Field(nullable=True,default=None)
    type: Optional[str] = Field(nullable=True,default=None)
    add_on: Optional[str] = Field(nullable=True,default=None)
    
    created_by_type : Optional[str] = Field(nullable=True,default=None)
    admin_emp_id : Optional[str] = Field(nullable=True,default=None)
    
    updated_by_type : Optional[str] = Field(nullable=True,default=None)
    updated_admin_emp_id : Optional[str] = Field(nullable=True,default=None)

    quantity : Optional[str] = Field(nullable=True,default=None)
    
    is_visible : Optional[bool] = Field(nullable=True,default=False)

    
class storeManagerProduct(StoreManagerProductBase,table = True):
    __tablename__ = "store_manager_product"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

# class storeManagerProductCreate(StoreManagerProductBase):
#     pass
class StageItem(BaseModel):
    steps: str
    time_riquired_for_this_process: str
    day: str
    assign_employee: str
    type:str
    step_id:str
    step_item:str
    file_path: Optional[str] = None
    serial_number: Optional[str] = None
    selected_product_ids: Optional[list[int]] = None


class storeManagerProductCreate(BaseModel):
    admin_id : str = None
    emplpoyee_id :Optional[str] = None
    product_tital : str = None
    purchase_request_id : str = None
    item_code : str = None
    categories : Optional[str] = None
    sub_categories : Optional[str] = None
    hsn_sac_code : Optional[str] = None
    gst_rate : Optional[str] = Field(nullable=False,default=None)
    discription : Optional[str] = None
    price_per_product : Optional[str] = None
    unit : Optional[str] = None
    sold_as : Optional[str] = None
    pack_of : Optional[str] = None
    steps : Optional[str] = None
    time_riquired_for_this_process : Optional[str] = None
    day : Optional[str] = None
    minimum_requuired_quantity_for_low_stock : Optional[str] = None
    document : Optional[str] = None
    opening_stock : Optional[str] = None
    internal_manufacturing : Optional[str] = None
    availability: Optional[str] = None
    Stages: Optional[str] = None
    type: Optional[str] = None
    add_on: Optional[str] = None
    
    created_by_type : Optional[str] = None
    admin_emp_id : Optional[str] = None
    quantity : Optional[str] = None

    stage: List[StageItem] = []

class storeManagerProductRead(StoreManagerProductBase):
    id : int


class StoreManagerProductBatchCreate(BaseModel):
    products: List[storeManagerProductCreate]


 
    



class ProductFilterQuery(BaseModel):
    admin_id: str
    employee_id: Optional[str] = None
    product_name: Optional[str] = None
    is_visible: Optional[bool] = None
    
    
    
    

class ProductDetailsRequest(BaseModel):
    admin_id: str
    employee_id: Optional[str] = None
    product_id: int


class UpdateProductQuantity(BaseModel):
    admin_id: str
    employee_id: Optional[str] = None
    product_id: int
    quantity :Optional[str] = None
    add_remark :Optional[str] = None


class ProductUnableDisabled(BaseModel):
    product_id: Optional[int] = None
    is_visible: Optional[bool] = False


class UnableDisabled_id(BaseModel):
    admin_id: Optional[str] = None
    employee_id: Optional[str] = None
    is_visible: Optional[bool] = None

class ProductDetailsBycode(BaseModel):
    admin_id: Optional[str] = None
    product_code: List[str] = None




