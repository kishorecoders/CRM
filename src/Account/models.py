from sqlmodel import SQLModel, Field, Relationship
from pydantic import UUID4
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from src.parameter import get_current_datetime
from sqlalchemy import Column, DateTime, Text , BigInteger
from sqlalchemy.dialects.mysql import LONGTEXT

class AccountBase(SQLModel):
    admin_id: int = Field(nullable=False, default=None)
    employee_id: int = Field(nullable=True, default=None)

    note: Optional[str] = Field(
        default=None,
        sa_column=Column(LONGTEXT, nullable=False)  # <-- set nullable here
    )    

    quote_id: str = Field(nullable=False, default=None)
    file_path: str = Field(nullable=False, default=None)
    po_number: str = Field(nullable=True, default=None)
    pi_number: str = Field(nullable=True, default=None)
    percent_ac: str = Field(nullable=True, default=None)
    percent_cash: str = Field(nullable=True, default=None)
    adavnce_amt: str = Field(nullable=True, default=None)
    payment_type: str = Field(nullable=True, default=None)
    file_type: str = Field(nullable=True, default=None)
    acc_status: Optional[int] = Field(default=1) 
    
    
    select_remark: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )
    
    add_note: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )
    
    pending: str = Field(nullable=True, default=None)
    advance_cash: str = Field(nullable=True, default=None)
    advance_account: str = Field(nullable=True, default=None)
    
    adv: str = Field(nullable=True, default=None)

    rcvd_amt: Optional[float] = Field(nullable=True, default=None)
    payment_type: Optional[str] = Field(nullable=True, default=None)
    sent_by: Optional[str] = Field(nullable=True, default=None)
    handover_name: Optional[str] = Field(nullable=True, default=None)
    payment_date: Optional[str] = Field(nullable=True, default=None)
    bank_name: Optional[str] = Field(nullable=True, default=None)
    account_holder_name: Optional[str] = Field(nullable=True, default=None)
    branch_name: Optional[str] = Field(nullable=True, default=None)
    ifsc_code: Optional[str] = Field(nullable=True, default=None)
    ac_no: Optional[str] = Field(nullable=True, default=None)
    gst: Optional[str] = Field(nullable=True, default=None)
    
    payment_method_type: Optional[str] = Field(nullable=True, default=None)
    cheque_no: Optional[str] = Field(nullable=True, default=None)
    cheque_date: Optional[str] = Field(nullable=True, default=None) 
    cheque_image: Optional[str] = Field(nullable=True, default=None)
    upi_number_or_id: Optional[str] = Field(nullable=True, default=None)
    transaction_upi_id: Optional[str] = Field(nullable=True, default=None)
    upi_image: Optional[str] = Field(nullable=True, default=None)
    file_path2 :Optional[str] = Field(nullable=True, default=None)

    note2: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )


class Account(AccountBase, table=True):
    __tablename__ = "account"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)


class AccountCreate(BaseModel):
    admin_id: int
    employee_id: Optional[str] = None
    note: str
    quote_id: str
    file_path: Optional[str] = None 
    po_number: Optional[str] = None 
    pi_number: Optional[str] = None
    percent_ac: Optional[str] = None
    percent_cash: Optional[str] = None
    adavnce_amt: Optional[str] = None
    payment_type: Optional[str] = None
    file_type: Optional[str] = None
    
    rcvd_amt: Optional[float] = None
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
    file_path2: Optional[str] = None
    note2: Optional[str] = None    
    pi_series: Optional[str] = None    

class AccountRead(AccountBase):
    admin_id: int


class AccountRequest(BaseModel):
    admin_id: int
    employee_id: Optional[int] = None
    account_id: Optional[int] = None

class AccountApprove(BaseModel):
    account_id: int
    select_remark: Optional[str] = None
    add_note: Optional[str] = None
    status: Optional[int] = None
