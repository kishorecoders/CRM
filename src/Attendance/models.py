from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime
from sqlmodel import SQLModel, Field, Column, JSON
from pydantic import BaseModel, validator
from pydantic import BaseModel, root_validator
from fastapi import UploadFile

from sqlalchemy import Column, DateTime, Text , BigInteger

class AttendanceBase(SQLModel):
    admin_id: int = Field(nullable=False)
    employee_id: int = Field(nullable=False)
    employee_name: Optional[str] = Field(nullable=True, default="Null")
    latitude: Optional[float] = Field(nullable=True, default=None)
    longitude: Optional[float] = Field(nullable=True, default=None)
    date_time: datetime = Field(default_factory=get_current_datetime, nullable=False)

    address: Optional[str] = Field(
        default="Null",
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )    

    sign_in_id: Optional[str] = Field(nullable=True, default="Null")
    image: Optional[str] = Field(nullable=True, default="Null")
    late_minute: Optional[int]=Field(nullable=True, default=0)

    remark: Optional[str] = Field(
        default="Null",
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )    

    sign_out_id: Optional[str] = Field(nullable=True, default="Null")
    status: Optional[str] = Field(nullable=True, default="Null")
    check_in_id: Optional[str] = Field(nullable=True, default="Null")
    check_in_out_reason: Optional[str] = Field(nullable=True, default="Null")
    check_out_id: Optional[str] = Field(nullable=True, default="Null")
    from_time: Optional[str] = Field(nullable=True, default="Null")
    end_time: Optional[str] = Field(nullable=True, default="Null")
    over_time: Optional[str] = Field(nullable=True, default="Null")
    
    created_by_type : Optional[str] = Field(nullable=True,default=None)
    admin_emp_id : Optional[str] = Field(nullable=True,default=None)

    over_time_remark: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )


class Attendance(AttendanceBase, table=True):
    __tablename__ = "employee_attendance"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)


class AttendanceCreate(BaseModel):
    admin_id: int
    employee_id: int
    latitude: float
    longitude: float
    address: str
    sign_in_img: Optional[str] = "Null"
    status: str
    remark:str
    type:Optional[str] = "employee"


class AttendanceRead(AttendanceBase):
    id: int
    created_at: datetime
    updated_at: datetime


class CheckIn(BaseModel):
    sign_in_id: int
    address: str
    latitude: float
    longitude: float
    status: str
    check_in_out_reason: str



class CheckOut(BaseModel):
    sign_in_id: int
    address: str
    latitude: float
    longitude: float
    status: str
    check_in_out_reason: str


class SignOut(BaseModel):
    admin_id: int
    employee_id: int
    sign_in_id: int
    latitude: float
    longitude: float
    address: str
    sign_out_img: Optional[str] = "Null"
    status: str



class AttendanceRequest(BaseModel):
    employee_id: Optional[int] = None
    admin_id: Optional[int] = None



class AttendanceFilterRequest(BaseModel):
    admin_id: int
    employee_id: Optional[int] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    employee_name : Optional[str] = None

    @root_validator(pre=True)
    def check_empty_dates(cls, values):
        
        if values.get('from_date') == "":
            values['from_date'] = None
        if values.get('to_date') == "":
            values['to_date'] = None
        return values   
    



class AttendanceMenualCreate(BaseModel):
    admin_id: int
    employee_id: int
    date_time: datetime
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = "Null"
    sign_in_img: Optional[str] = "Null"
    from_time:Optional[str] = None
    end_time:Optional[str] = None
    remark:Optional[str] = None
    admin_emp_id:Optional[str] = None
    created_by_type:Optional[str] = None




class SalaryDetailsRequest(BaseModel):
    admin_id: int
    emp_id: Optional[int] = None

# class EmployeeSalaryResponse(BaseModel):
#     employee_id: str
#     employee_name: str
#     monthly_salary: float
#     calculated_salary: float
#     created_date: datetime
#     salary_slip_url: str
#     total_day_working: str
#     absent_date: str
#     present_date: str
#     total_days_of_month: int
#     employee_code: str
#     designation: Optional[str] = None
#     pan_no: Optional[str] = None
#     account_no: Optional[str] = None
#     bank_name: Optional[str] = None
#     paid_leave: Optional[int] = None
#     dearness_allowance: Optional[float] = None
#     HRA: Optional[float] = None
#     medical_allowance: Optional[float] = None
#     PF: Optional[float] = None  # Made optional
#     professional_tax: Optional[float] = None
#     TDS: Optional[float] = None


class EmployeeSalaryResponse(BaseModel):
    employee_id: str
    employee_name: str
    monthly_salary: float
    calculated_salary: float
    created_date: datetime
    salary_slip_url: str
    total_day_working: str
    public_holiday_dates: List[str] = []
    weekly_holiday_dates: List[str] = []
    absent_date: List[str]
    present_date: List[str]
    total_days_of_month: int
    employee_code: str
    designation: Optional[str] = None
    pan_no: Optional[str] = None
    account_no: Optional[str] = None
    bank_name: Optional[str] = None
    paid_leave: Optional[int] = None
    HRA: Optional[float] = None
    PF: Optional[float] = None
    professional_tax: Optional[float] = None
    TDS: Optional[float] = None
    net_salary: Optional[float] = None
    deduction_amount: Optional[float] = None
    bank_account_holder_name: Optional[str] = None
    bank_account_number: Optional[str] = None
    bank_ifsc_code: Optional[str] = None
    pan_card: Optional[str] = None
    house_rent_allowance: Optional[str] = None
    dearness_allowance: Optional[str] = None
    medical_allowance: Optional[str] = None
    special_allowance: Optional[str] = None
    bonus: Optional[str] = None
    telephone_reimbursement: Optional[str] = None
    fuel_reimbursement: Optional[str] = None
    medical_file:Optional[bytes]
    m_file_name:Optional[str] = None
    
    
    

class UpdateSignOutRequest(BaseModel):
    sign_out_id: int
    over_time: str
    remark: str
    
    
    
class TimerRequest(BaseModel):
    sign_out_id: int
    
    
class DeleteAtt(BaseModel):
    id: Optional[str] = None
    admin_id: Optional[str] = None
    emp_id: Optional[str] = None

class AttendanceOvertimeCreate(BaseModel):
    admin_id: Optional[str] = None
    employee_id: Optional[str] = None
    date_time: Optional[str] = get_current_datetime().date()
    over_time: Optional[str] = None
    over_time_remark: Optional[str] = None




