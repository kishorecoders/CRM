from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime
from src.QuotationProductEmployee.models import QuotationProductEmployeeCreate,QuotationProductEmployeeUpdate,QuotationProductEmployeeBase
from enum import Enum

from sqlalchemy import Column, DateTime, Text , BigInteger




class AccountPosition(str, Enum):
    PAYMENT_CLEAR = "PAYMENT AND DISPATCH CLEAR"
    WORK_PROCESS = "WORK IN PROCESS"
    CANCEL = "CANCEL"
    PARTLY_DISPATCH = "PARTLY DISPATCH"





class QuotationBase(SQLModel):
    admin_id : Optional[str] = Field(nullable=False,default=None)
    employe_id : Optional[str] = Field(nullable=False,default=None)
    lead_id : Optional[str] = Field(nullable=False,default=None)
    product_id : Optional[str] = Field(nullable=False,default=None)
    quotation_date : Optional[str] = Field(nullable=False,default=date.today())
    expiry_date : Optional[str] = Field(nullable=False,default=date.today())
    quotation_number : Optional[str] = Field(nullable=False,default=None)
    reference : Optional[str] = Field(nullable=True,default=None)
    sales_persone : Optional[str] = Field(nullable=True,default=None)
    subject : Optional[str] = Field(nullable=False,default=None)
    customer_notes : Optional[str] = Field(nullable=False,default=None)
    terms_condition : Optional[str] = Field(nullable=False,default=None)
    discription: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=False)  # <-- set nullable here
    )    

    quantity : Optional[str] = Field(nullable=False,default=None)
    discount : Optional[str] = Field(nullable=False,default=None)

    delevery_address: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )
    

    total_amount : Optional[str] = Field(nullable=True,default=None)
    gst : Optional[str] = Field(nullable=True,default=None)
    delevery_date : Optional[str] = Field(nullable=True,default=date.today())
    payment_term : Optional[str] = Field(nullable=True,default=None)
    term_and_condition : Optional[str] = Field(nullable=True,default=None)
    discount_percent : Optional[str] = Field(nullable=True,default=None)
    discount_type : Optional[str] = Field(nullable=True,default="Percent")
    
    site_name :Optional[str] = Field(nullable=True,default=None)
    self_company:Optional[str] = Field(nullable=True,default=None)
    customer_id:Optional[str] = Field(nullable=True,default=None)
    
    series : Optional[str] = Field(nullable=True,default=None)
    contact_person : Optional[str] = Field(nullable=True,default=None)
    sales_credit : Optional[str] = Field(nullable=True,default=None)
    shipping_address : Optional[str] = Field(nullable=True,default=None)
    #note: Optional[str] = Field(nullable=True,default=None)
    
    note: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )
    
    
    bank_detail: Optional[str] = Field(nullable=True,default=None)
    file: Optional[str] = Field(nullable=True,default=None)
    save_as_template: Optional[str] = Field(nullable=True,default=None)
    share_by_email: Optional[str] = Field(nullable=True,default=None)
    share_by_whatsapp: Optional[str] = Field(nullable=True,default=None)
    account_status: Optional[str] = Field(nullable=True,default=0)
    
    
    
    po_number: Optional[str] = Field(default=None)
    pi_number: Optional[str] = Field(default=None)
    pi_date: Optional[str] = Field(default_factory=date.today)
    taxable_amount: Optional[str] = Field(default=None)
    total_receivable: Optional[str] = Field(default=None)
    total_received: Optional[str] = Field(default=None)
    cash_balance: Optional[str] = Field(default=None)
    account_balance: Optional[str] = Field(default=None) 

    invoice_number: Optional[str] = Field(default=None)
    invoice_file : Optional[str] = Field(default=None)

    invoice_status : Optional[int] = Field(default=0) 
    status: Optional[int] = Field(default=0) 
    
    account_position: Optional[AccountPosition] = Field(default=AccountPosition.PAYMENT_CLEAR)

    quotation_status : Optional[int] = Field(default=0) 
    created_by_type : Optional[str] = Field(nullable=True,default=None)
    admin_emp_id : Optional[str] = Field(nullable=True,default=None)

    comver_order_status : Optional[str] = Field(nullable=True,default="pending")

    updated_by_type : Optional[str] = Field(nullable=True,default=None)
    updated_admin_emp_id : Optional[str] = Field(nullable=True,default=None)

    pi_series: Optional[str] = Field(nullable=True,default=None)
    po_series: Optional[str] = Field(nullable=True,default=None)
    dc_series: Optional[str] = Field(nullable=True,default=None)
    inv_series: Optional[str] = Field(nullable=True,default=None)

    sales_credit_id : Optional[str] = Field(nullable=True,default=None)
    specification: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )

class Quotation(QuotationBase,table = True):
    __tablename__ = "quotation"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)



# class QuotationCreate(QuotationBase):
#     pass

class StageDetails(BaseModel):
    steps: str
    time_riquired_for_this_process: str
    day: str
    assign_employee: str
    type: str
    step_id: str
    stage_id: Optional[int]
    parent_stage_id: Optional[str]
    created_by_type: Optional[str]
    admin_emp_id: Optional[str]

class QuotationProductEmployeeCreate(QuotationProductEmployeeBase):
    stages: List[StageDetails]  
 


class QuotationCreate(BaseModel):
    admin_id : Optional[str] = None
    employe_id : Optional[str] = None
    lead_id : Optional[str] = None
    product_id : Optional[str] = None
    quotation_date : Optional[str] = None
    expiry_date : Optional[str] = None
    quotation_number : Optional[str] = None
    reference : Optional[str] = None
    sales_persone : Optional[str] = None
    subject : Optional[str] = None
    customer_notes : Optional[str] = None
    terms_condition : Optional[str] = None
    discription : Optional[str] = None
    quantity : Optional[str] = None
    discount : Optional[str] = None
    delevery_address : Optional[str] = None
    total_amount : Optional[str] = None
    gst : Optional[str] = None
    delevery_date : Optional[str] = None
    payment_term : Optional[str] = None
    term_and_condition : Optional[str] = None
    discount_percent : Optional[str] = None
    
    site_name :Optional[str] = None
    self_company:Optional[str] = None
    customer_id:Optional[str] = None

    series: Optional[str] = None
    contact_person : Optional[str] = None
    sales_credit : Optional[str] = None
    shipping_address : Optional[str] = None
    note: Optional[str] = None
    bank_detail: Optional[str] = None
    file: Optional[str] = None
    save_as_template: Optional[str] = None
    share_by_email: Optional[str] = None
    share_by_whatsapp: Optional[str] = None
    account_status: Optional[str] = None



    po_number: Optional[str] = None
    pi_number: Optional[str] = None
    pi_date: Optional[str] = None
    taxable_amount: Optional[str] = None
    total_receivable: Optional[str] = None
    total_received: Optional[str] = None
    cash_balance: Optional[str] = None
    account_balance: Optional[str] = None

    invoice_number: Optional[str] = None
    invoice_file : Optional[str] = None

    invoice_status : Optional[int] = None
    status: Optional[int] = None

    account_position: Optional[AccountPosition] = None

    quotation_status : Optional[int] = None
    created_by_type : Optional[str] = None
    admin_emp_id : Optional[str] = None

    comver_order_status : Optional[str] = None

    updated_by_type : Optional[str] = None
    updated_admin_emp_id : Optional[str] = None
    discount_type : Optional[str] = None
    sales_credit_id : Optional[str] = None
     
    products: List[QuotationProductEmployeeCreate]


class StageUpdateRequest(BaseModel):
    id: Optional[int]  
    admin_id: str
    product_id: Optional[str] = None
    assign_employee: Optional[str] = None
    steps: Optional[str] = None
    stage_id: Optional[int]
    time_riquired_for_this_process: Optional[str] = None
    day: Optional[str] = None
    type: str


class QuotationProductEmployeeUpdate(BaseModel):
    id: Optional[int]  
    admin_id: str
    employee_id: Optional[str] = None
    quote_id: Optional[str] = None
    lead_id: Optional[str] = None
    product_name: Optional[str] = None
    product_code: Optional[str] = None
    hsn_code: Optional[str] = None
    rate_per_unit: Optional[float] = None
    quantity: Optional[int] = None
    total: Optional[float] = None
    gst_percentage: Optional[float] = None
    gross_total: Optional[float] = None
    availability: Optional[str] = None
    discount_type: Optional[str] = None
    discount_amount: Optional[float] = None
    discount_percent: Optional[float] = None
    unit:Optional[str] = None
    product_payment_type:Optional[str] = None
    product_cash_balance:Optional[str] = None
    product_account_balance:Optional[str] = None
    
    manufacture_quantity: Optional[str] = None
    available_quantity: Optional[str] = None
    
    #product_type:Optional[str] = None
    product_id:Optional[str] = None
    specification:Optional[str] = None
    stages: List[StageUpdateRequest]


class Quotationupdate(BaseModel):
    admin_id: Optional[str] = None
    employe_id: Optional[str] = None
    lead_id: Optional[str] = None
    product_id: Optional[str] = None
    quotation_date: Optional[str] = None
    expiry_date: Optional[str] = None
    quotation_number: Optional[str] = None
    reference: Optional[str] = None
    sales_persone: Optional[str] = None
    subject: Optional[str] = None
    customer_notes: Optional[str] = None
    terms_condition: Optional[str] = None
    discription: Optional[str] = None
    quantity: Optional[str] = None
    discount: Optional[str] = None
    delevery_address: Optional[str] = None
    total_amount: Optional[str] = None
    gst: Optional[str] = None
    delevery_date: Optional[str] = None
    payment_term: Optional[str] = None
    term_and_condition: Optional[str] = None
    discount_percent: Optional[str] = None
    
    site_name :Optional[str] = None
    self_company:Optional[str] = None
    customer_id:Optional[str] = None
    
    series : Optional[str] = None
    contact_person : Optional[str] = None
    sales_credit : Optional[str] =  None
    shipping_address : Optional[str] = None
    note: Optional[str] = None
    bank_detail: Optional[str] = None
    file: Optional[str] = None
    save_as_template: Optional[str] = None
    share_by_email: Optional[str] = None
    share_by_whatsapp: Optional[str] = None
    quotation_status: Optional[str] = None
    updated_by_type : Optional[str] = None
    updated_admin_emp_id : Optional[str] = None
    sales_credit_id : Optional[str] = None
    discount_type : Optional[str] = None

    products: List[QuotationProductEmployeeUpdate]






class QuotationRead(QuotationBase):
    id : int
    
    
    
class CreateInvoiceRequest(BaseModel):
    admin_id: str
    employee_id: Optional[str] = None
    quote_id: str
    invoice_number: str

class FileItem(BaseModel):
    file_name: str
    file_path: str

class Product(BaseModel):
    product_id: Optional[str] = None
    product_code: Optional[str] = None
    available_quantity: Optional[str] = None
    manufacture_quantity: Optional[str] = None

class Convertorder(BaseModel):
    admin_id: Optional[str] = None
    employe_id: Optional[str] = None
    quotation_id: Optional[str] = None
    lead_id: Optional[str] = None
    files: Optional[List[FileItem]]
    Product_details: Optional[List[Product]]




class QuotationApprove(BaseModel):
    account_id : int
    quotation_status: int