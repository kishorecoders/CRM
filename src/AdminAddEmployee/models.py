from sqlmodel import SQLModel, Field, Relationship
from pydantic import UUID4
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Text , BigInteger
from sqlmodel import SQLModel, Field, Column, JSON
import json
from src.parameter import get_current_datetime

class AdminAddEmployeeBase(SQLModel):
    admin_id: int = Field(nullable=False, default=0)
    employe_email_id: str = Field(nullable=False, default=0)
    #employe_phone_number: Optional[str] = Field(nullable=False, default="0")
    #employe_phone_number: int = Field(nullable=False, default=0)
    
    employe_phone_number: int = Field(
        default=0,
        sa_column=Column(BigInteger, nullable=False, default=0)
    )
    employe_name: Optional[str] = Field(nullable=True, default=0)
    employe_job_title: Optional[str] = Field(nullable=True, default="Null")
    employee_id: Optional[str] = Field(nullable=False, default="Null")
    employe_user_name: Optional[str] = Field(nullable=True, default="Null")
    employe_password: Optional[str] = Field(nullable=True, default="Null")
    employe_confirm_password: Optional[str] = Field(nullable=True, default=None)
    employee_salary: Optional[str] = Field(nullable=True, default="Null")
    #employe_remark: Optional[str] = Field(nullable=True, default="Null")
    
    # ? Update this field to support large text
    employe_remark: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )
    
    level: str = Field(default="Level-6", nullable=False)
    shift_name: Optional[str] = Field(nullable=True, default="Null")
    paid_leave: Optional[str] = Field(nullable=True, default="")
    date_of_birth: Optional[str] = Field(nullable=True, default="Null")
    Designation: Optional[str] = Field(nullable=True, default="Null")
    is_active: bool = Field(default=True, nullable=True)


    school_or_college_name: Optional[str] = Field(nullable=True, default="Null")
    education_passout_year: Optional[int] = Field(nullable=True)
    #description: Optional[str] = Field(nullable=True, default="")

    description: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )
    
    
    bank_name: Optional[str] = Field(nullable=True, default=None)
    bank_account_holder_name: Optional[str] = Field(nullable=True, default=None)
    bank_account_number: Optional[str] = Field(nullable=True, default=None)
    bank_ifsc_code: Optional[str] = Field(nullable=True, default=None)
    pan_card: Optional[str] = Field(nullable=True, default=None)

    
    skills_list: Optional[List[str]] = Field(default_factory=list, sa_column=Column(JSON))
    position: Optional[str] = Field(nullable=True, default="Null")
    past_company_name: Optional[str] = Field(nullable=True, default="Null")
    experience: Optional[str] = Field(nullable=True, default="Null")

    reset_token: Optional[str] = Field(nullable=True ,default=None)
    reset_token_expiry: Optional[datetime] = Field(nullable=True , default=None)   



    house_rent_allowance : Optional[str] = Field(nullable=True, default=None)
    dearness_allowance: Optional[str] = Field(nullable=True, default=None)
    medical_allowance: Optional[str] = Field(nullable=True, default=None)
    special_allowance: Optional[str] = Field(nullable=True, default=None)
    bonus: Optional[str] = Field(nullable=True, default=None)
    telephone_reimbursement: Optional[str] = Field(nullable=True, default=None)
    fuel_reimbursement: Optional[str] = Field(nullable=True, default=None)
    device_token: Optional[str] = Field(nullable=True, default=None)
    device_type: Optional[str] = Field(nullable=True, default=None)
    


    
    


    @property
    def skills(self) -> List[str]:
        """Deserialize the JSON string to a list with error handling."""
        if not self.skills_list:
            return []
        try:
            return json.loads(self.skills_list)
        except (json.JSONDecodeError, TypeError):
            print("Error decoding skills_list JSON, returning empty list")
            return []

    @skills.setter
    def skills(self, value: List[str]) -> None:
        """Serialize the list to a JSON string."""
        self.skills_list = json.dumps(value) if value else json.dumps([])


class AdminAddEmployee(AdminAddEmployeeBase, table=True):
    __tablename__ = "admin_add_employee"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)



class AdminAddEmployeeCreate(BaseModel):
    admin_id: int 
    employe_email_id: str = None
    employe_phone_number: int 
    employe_name: Optional[str] = None
    employe_job_title: Optional[str] = None
    employee_id: Optional[str] = None
    employe_user_name: Optional[str] = None
    employe_password: Optional[str] = None
    employe_confirm_password: Optional[str] = None
    employee_salary: Optional[str] = None
    employe_remark: Optional[str] = None
    level: str =None
    shift_name: Optional[str] = None
    paid_leave: Optional[str] = None
    date_of_birth: Optional[str] = None
    Designation: Optional[str] = None
    is_active: bool = None
    school_or_college_name: Optional[str] = None
    education_passout_year: Optional[int] = None
    description: Optional[str] = None
    bank_name: Optional[str] = None
    bank_account_holder_name: Optional[str] = None
    bank_account_number: Optional[str] = None
    bank_ifsc_code: Optional[str] = None
    pan_card: Optional[str] = None
    skills_list: Optional[List[str]] = None
    position: Optional[str] = None
    past_company_name: Optional[str] = None
    experience: Optional[str] = None
    reset_token: Optional[str] = None
    reset_token_expiry: Optional[datetime] = None 
    house_rent_allowance : Optional[str] = None
    dearness_allowance: Optional[str] = None
    medical_allowance: Optional[str] = None
    special_allowance: Optional[str] = None
    bonus: Optional[str] = None
    telephone_reimbursement: Optional[str] = None
    fuel_reimbursement: Optional[str] = None



class AdminAddEmployeeRead(AdminAddEmployeeBase):
    id: int
    
    
class OTPRequest(BaseModel):
    phone_number: str
    device_token: Optional[str] = None
    
    
    
class UpdateEmployeeStatusRequest(BaseModel):
    admin_id: int
    employee_id: str
    is_active: bool

class DeleteEmployee(BaseModel):
    admin_id: int
    employee_id: str




    
