from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime
from sqlalchemy import Column, DateTime, Text , BigInteger
from sqlalchemy import JSON



class ProductionBase(SQLModel):
    admin_id : str = Field(nullable=True,default=None)
    from_employee : str = Field(nullable=True,default=None)
    stage_name: Optional[str] = Field(nullable=True,default=None)
    assign_employee: Optional[str] = Field(nullable=True,default=None)
    ideal_time: Optional[str] = Field(nullable=True,default=None)
    custom_time: Optional[str] = Field(nullable=True,default=None)
    deadline: Optional[str] = Field(nullable=True,default=None)
    priority: Optional[str] = Field(nullable=True,default=None)
    type: Optional[str] = Field(nullable=True,default=None)
    quote_id : Optional[str] = Field(nullable=True,default=None)
    lead_id : Optional[str] = Field(nullable=True,default=None)
    product_name: Optional[str] = Field(nullable=True,default=None)
    product_code: Optional[str] = Field(nullable=True,default=None)
    hsn_code: Optional[str] = Field(nullable=True,default=None)
    rate_per_unit: Optional[float] = Field(nullable=True,default=None)
    quantity: Optional[int] = Field(nullable=True,default=None)
    total: Optional[float] = Field(nullable=True,default=None)
    gst_percentage: Optional[float] = Field(nullable=True,default=None)
    gross_total: Optional[float] = Field(nullable=True,default=None)
    availability: Optional[str] = Field(nullable=True,default=None)
    purchase_request_id : Optional[str] = Field(nullable=True,default=None)
    categories : Optional[str] = Field(nullable=True,default=None)
    sub_categories : Optional[str] = Field(nullable=True,default=None)
    gst_rate : Optional[str] = Field(nullable=True,default=None)
    discription : Optional[str] = Field(nullable=True,default=None)
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
    status:Optional[str] = Field(nullable=True,default=None)
    comment_mark:Optional[str] = Field(nullable=True,default=None)
    order_id:Optional[str] = Field(nullable=True, default=None)
    stage_id:Optional[str] = Field(nullable=True, default=None)
    from_status:Optional[str] = Field(nullable=True, default=None)
    step_id:Optional[str] = Field(nullable=True, default=None)
    
    add_remark: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )    

    quotation_id: Optional[str] = Field(nullable=True,default=None)

    production_engeneer: Optional[str] = Field(nullable=True,default=None)
    production_engeneer_status: Optional[str] = Field(nullable=True,default="Pending")

    production_engeneer_remark: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )   
    doc_no: Optional[str] = Field(nullable=True,default=None)
    doc_date: Optional[str] = Field(nullable=True,default=None)
    rec_date: Optional[str] = Field(nullable=True,default=None)
    exp_date: Optional[str] = Field(nullable=True,default=None)

    product_similar_stages: Optional[List[str]] = Field(default=None, sa_type=JSON)
    
    subproduct_list_ids: Optional[List[str]] = Field(default=None, sa_type=JSON)

    

# class ProductionStatusUpdate(BaseModel):
#     admin_id: str
#     employee_id: Optional[str] = None
#     production_id: str
#     status: str
    
class ProductionStatusUpdate(BaseModel):
    admin_id: str
    employee_id: Optional[str] = None
    production_id: str
    status: Optional[str] = None 
    comment_mark: Optional[str] = None  
    assign_employee: Optional[str] = None  
    subproduct_list_ids: Optional[List[str]]




    
class Production(ProductionBase,table = True):
    __tablename__ = "production"
    
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    started_at: datetime = Field(default=None, nullable=True)
    end_at: datetime = Field(default=None, nullable=True)

    

class CheckPointItem(BaseModel):
    check_point_name: str
    check_point_status: int

class SubProductItemWithCheckpoints(BaseModel):
    sub_product_name: str
    quantity: int
    add_remark: str
    parent_subproduct_id: str
    checkpoints: Optional[List[CheckPointItem]] 

class ProductionSubproduct(BaseModel):
    admin_id: str
    emp_id: str
    product_id: str
    add_remark: str
    sub_products: List[SubProductItemWithCheckpoints]


class templateItem(BaseModel):
    temp_key_name: str
    temp_value: str

class TemplateItemWithkeys(BaseModel):
    template_name: str
    template_key_value: Optional[List[templateItem]] 

class TemplateInput(BaseModel):
    product_id: str
    admin_id: str
    emp_id: str
    templates: List[TemplateItemWithkeys]

class ProductionStatusUpdateFromStageid(BaseModel):
    admin_id: str
    employee_id: Optional[str] = None
    stage_id: Optional[str] = None  

class ProductionCreate(BaseModel):
    admin_id : str = None
    from_employee : str = None
    stage_name: Optional[str] = None
    assign_employee: Optional[str] = None
    ideal_time: Optional[str] = None
    custom_time: Optional[str] = None
    deadline: Optional[str] = None
    priority: Optional[str] = None
    type: Optional[str] = None
    quote_id : Optional[str] = None
    lead_id : Optional[str] = None
    product_name: Optional[str] = None
    product_code: Optional[str] = None
    hsn_code: Optional[str] = None
    rate_per_unit: Optional[float] = None
    quantity: Optional[int] = None
    total: Optional[float] = None
    gst_percentage: Optional[float] = None
    gross_total: Optional[float] = None
    availability: Optional[str] = None
    purchase_request_id : Optional[str] = None
    categories : Optional[str] = None
    sub_categories : Optional[str] = None
    gst_rate : Optional[str] = None
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
    status:Optional[str] = None
    comment_mark:Optional[str] = None
    order_id:Optional[str] = None
    stage_id:Optional[str] = None
    from_status:Optional[str] = None
    step_id:Optional[str] = None
    quotation_id: Optional[str] = None
    
    production_engeneer: Optional[str] = None
    doc_no: Optional[str] = None
    doc_date: Optional[str] = None
    rec_date: Optional[str] = None
    exp_date: Optional[str] = None    
    product_similar_stages: Optional[List[str]]
    subproduct_list_ids: Optional[List[str]]

    product_sub_products: Optional[List[ProductionSubproduct]] 
    product_templates: Optional[List[TemplateInput]] 

class ProductionRead(BaseModel):
    admin_id: int
    employee_id: Optional[str] = None
    stage_id: Optional[str] = None
    
class AddRemark(BaseModel):
    Production_id: int
    remark: Optional[str] = None



class ProductionCreateList(BaseModel):
    products: List[ProductionCreate]

      
class Checkpoint(BaseModel):
    checkpoint_id: Optional[int] = None
    check_status: Optional[int] = None
    checkpoint_remark: Optional[str] = None
      
class Add_Check_Remark(BaseModel):
    production_id: int
    admin_id: Optional[str] = None
    employee_id: Optional[str] = None
    check_remark: Optional[str] = None
    production_engeneer_status: Optional[str] = None
    #point: list[Checkpoint]
    point: Optional[List[Checkpoint]] = None