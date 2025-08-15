from pydantic import BaseModel
from typing import Optional
from sqlmodel import SQLModel, Field
from src.parameter import get_current_datetime
from datetime import datetime
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy import Column, DateTime, Text , BigInteger
# ✅ Base class (not mapped to DB)
class PaymentRequestBase(SQLModel):
    account_id: str
    admin_id: Optional[str] = None
    emp_id: Optional[str] = None
    product_id: Optional[str] = None
    rcvd_amt: Optional[float] = None
    payment_type: Optional[str] = None
    sent_by: Optional[str] = None
    handover_name: Optional[str] = None
    payment_date: Optional[str] = None
    bank_name: Optional[str] = None
    account_holder_name: Optional[str] = None
    branch_name: Optional[str] = None
    ifsc_code: Optional[str] = None
    ac_no: Optional[str] = None
    gst: Optional[str] = None

    payment_method_type: Optional[str] = None
    cheque_no: Optional[str] = None
    cheque_date: Optional[str] = None 
    cheque_image: Optional[str] = None
    upi_number_or_id: Optional[str] = None
    transaction_upi_id: Optional[str] = None
    upi_image: Optional[str] = None
    file_path :Optional[str] = None
    
    note: Optional[str] = Field(
        default=None,
        sa_column=Column(LONGTEXT, nullable=True)  # <-- set nullable here
    ) 

# ✅ Mapped Table (Corrected version)
class PaymentRequest(PaymentRequestBase, table=True):
    __tablename__ = "add_payment"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

# ✅ Request Schema (Used for API Validation)
class PaymentRequestSchema(BaseModel):
    account_id: str
    admin_id: str = ""
    emp_id: str = ""
    product_id: str = ""
    rcvd_amt: float = ""
    payment_type: str = ""
    sent_by: str = ""
    handover_name: str = ""
    payment_date: str = ""
    bank_name: str = ""
    account_holder_name: str = ""
    branch_name: str = ""
    ifsc_code: str = ""
    ac_no: str = ""
    gst: str = ""

    # New fields added based on the JSON
    payment_method_type: str = ""
    cheque_no: str = ""
    cheque_date: str = ""
    cheque_image: str = ""
    upi_number_or_id: str = ""
    transaction_upi_id: str = ""
    upi_image: str = ""
    file_path : str = ""
    note: str = ""

class GetPaymentsAccount(BaseModel):
    account_id: str
    

class EditPaymentRequest(BaseModel):
    payment_id: int
    account_id: str
    admin_id: str
    emp_id: str
    product_id: str
    rcvd_amt: str
    payment_type: str
    sent_by: str
    handover_name: str
    payment_date: str
    bank_name: str
    account_holder_name: str
    branch_name: str
    ifsc_code: str
    ac_no: str
    gst: str

    # New fields added based on the JSON
    payment_method_type: str
    cheque_no: str
    cheque_date: str
    cheque_image: str
    upi_number_or_id: str
    transaction_upi_id: str
    upi_image: str\
    
# ✅ Request Model
class DeletePaymentRequest(BaseModel):
    payment_id: int
    
    