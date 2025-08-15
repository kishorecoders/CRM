from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime
from src.PurchaseOrderProduct.models import PurchaseOrderProductBase
from sqlalchemy import Column, DateTime, Text , BigInteger

class PurchaseOrderIssueBase(SQLModel):
    admin_id : str = Field(nullable=False,default=0)
    emplpoyee_id :Optional[str] = Field(nullable=False,default=None)
    vendor_id : str = Field(nullable=False,default=None)
    purchase_request_id : str = Field(nullable=False,default=None)
    product_id : str = Field(nullable=False,default=None)
    po_number : str = Field(nullable=False,default=None)
    request_datetime : Optional[datetime] = Field(nullable=True,default=datetime.now())
    #dilevery_location : Optional[str] = Field(nullable=True,default=None)
    
    dilevery_location: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )    

    deadline : Optional[str] = Field(nullable=True,default=None)

    remark_schedual: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )    

    last_status : Optional[str] = Field(nullable=True,default="Pending")
    term_and_condition : Optional[str] = Field(nullable=True,default=None)
    payment_term : Optional[str] = Field(nullable=True,default=None)
    site_name :Optional[str] = Field(nullable=True,default=None)
    bussiness_name:Optional[str] = Field(nullable=True,default=None)
    series : Optional[str] = Field(nullable=True,default=None)
    
    shipping_address: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )
    
    billing_address: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )
    

    note: Optional[str] = Field(nullable=True,default=None)
    order_date : Optional[str] = Field(nullable=True,default=date.today())
    expiry_date : Optional[str] = Field(nullable=True,default=date.today())
    order_number : Optional[str] = Field(nullable=True,default=None)
    reference : Optional[str] = Field(nullable=True,default=None)
    file: Optional[str] = Field(nullable=True,default=None)
    quote_file: Optional[str] = Field(nullable=True,default=None)
    frieght_mode : Optional[str] = Field(nullable=True,default=None)
    #delivery_term : Optional[str] = Field(nullable=True,default=None)

    delivery_term: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )    

    model_of_delivery : Optional[str] = Field(nullable=True,default=None)
    contact_person : Optional[str] = Field(nullable=True,default=None)
    contact_number : Optional[str] = Field(nullable=True,default=None)


    
class PurchaseOrderIssue(PurchaseOrderIssueBase,table = True):
    __tablename__ = "purchase_order_issue"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class PurchaseOrderIssueCreate(PurchaseOrderIssueBase):
    #po_series : Optional[str] = None
    pass

class PurchaseOrderIssueRead(PurchaseOrderIssueBase):
    id : int
    
class PurchaseOrderIssueLastStatusUpdate(SQLModel):
    last_status: Optional[str] = None   




class PurchaseOrderProductInput(SQLModel):
    product_name: str
    product_code: str
    hsn_code: str
    rate_per_unit: float
    quantity: int
    total: float
    gst_percentage: float
    gross_total: float
    availability: str
    status: Optional[str] = None
    discount_type: Optional[str] = None
    discount_amount: Optional[str] = None
    discount_percent: Optional[str] = None
    unit: Optional[str] = None
    discription: Optional[str] = None
    cgst: Optional[str] = None
    sgst: Optional[str] = None
    type: Optional[str] = None
    purchase_order_id: Optional[str] = None



class PurchaseOrderIssueCreateWithProducts(PurchaseOrderIssueCreate):
    products: List[PurchaseOrderProductInput]


class PurchaseOrderIssueRequest(BaseModel):
    order_data: PurchaseOrderIssueCreateWithProducts

