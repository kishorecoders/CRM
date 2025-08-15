from sqlmodel import SQLModel, Field, Column
from typing import Optional, List
from datetime import datetime
from src.parameter import get_current_datetime
from pydantic import BaseModel, root_validator
from sqlalchemy import Column ,  Text , LargeBinary
from datetime import date
from pydantic import BaseModel, validator

class TaskRequestBase(SQLModel):
    admin_id: int = Field(nullable=False)
    emp_id_from: str = Field(nullable=False)
    emp_id_to: str = Field(nullable=False)

    task_title: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=False)  # <-- set nullable here
    )

    task_details: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )
    task_priority: str = Field(nullable=False)  
    task_status: str = Field(nullable=False)  
    from_date_time: datetime = Field(nullable=True)
    to_date_time: datetime = Field(nullable=True)
    task_type_status: str = Field(nullable=False) 
    create_by: Optional[str] = Field(nullable=True)
    
    customer_id: Optional[str] = Field(nullable=True)
    
    created_by_type : Optional[str] = Field(nullable=True)
    admin_emp_id : Optional[str] = Field(nullable=True)

    updated_by_type : Optional[str] = Field(nullable=True)
    updated_admin_emp_id : Optional[str] = Field(nullable=True)


    task_remark: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )
    
    complete_file_path: Optional[str] = Field(nullable=True)
    project_id: Optional[str] = Field(nullable=True , default="0")
    task_routine: Optional[str] = Field(nullable=True , default=None)
    
class TaskRequest(TaskRequestBase, table=True):
    __tablename__ = "employee_task"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    # task_file_image: List[Dict[str, Union[str, List[int]]]] = Field(sa_column=Column(JSON))
    task_file_image: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True)  # <-- set nullable here
    )
    


class TaskRequestCreate(BaseModel):
    admin_id: int = None
    emp_id_from: str = None
    emp_id_to: str = None
    task_title: str = None
    task_details: Optional[str] = None
    task_priority: str = None  
    task_status: str = None  
    from_date_time: datetime = None
    to_date_time: datetime = None
    task_type_status: str = None 
    create_by: Optional[str] = None
    customer_id: Optional[str] = None
    project_id: Optional[str] = None
    task_file_image: List[str]


    


class TaskRequestRead(TaskRequestBase):
    id: int
    created_at: datetime
    updated_at: datetime



class TaskListRequest(BaseModel):
    admin_id: int 
    emp_id_from: Optional[str] = None 
    emp_id_to: Optional[str] = None  
    from_date: Optional[str] = None 
    to_date: Optional[str] = None 
    task_priority: Optional[str] = None  
    task_status: Optional[str] = None
    customer_id: Optional[str] = None 
    project_id: Optional[str] = None 
    task_id: Optional[str] = None 


      

    @root_validator(pre=True)
    def check_empty_dates(cls, values):
        
        if values.get('from_date') == "":
            values['from_date'] = None
        if values.get('to_date') == "":
            values['to_date'] = None
        return values    
    

class DeleteTask(BaseModel):
    admin_id: int 
    emp_id: str
    task_id: int




class TaskRequestUpdate(BaseModel):
    task_id: int  
    admin_id: Optional[int] = None
    emp_id_from: Optional[str] = None
    emp_id_to: Optional[str] = None
    task_title: Optional[str] = None
    task_details: Optional[str] = None
    task_file_image: Optional[List[str]] = None
    #task_file_image: Optional[List[Dict[str, Union[str, List[int]]]]] = None  
    task_priority: Optional[str] = None
    task_status: Optional[str] = None
    from_date_time: Optional[datetime] = None
    to_date_time: Optional[datetime] = None
    task_type_status: Optional[str] = None
    create_by: Optional[str] = None
    customer_id: Optional[str] = None
    task_routine: Optional[str] = None

    created_by_type : Optional[str] = None
    admin_emp_id : Optional[str] = None

    updated_by_type : Optional[str] = None
    updated_admin_emp_id : Optional[str] = None


    
    
    

class TaskStatusUpdate(BaseModel):
    admin_id: int
    task_id: int
    emp_id_from: Optional[str] = None

    customer_id: Optional[str] = None
    to_date_time: Optional[datetime] = None
    emp_id_to: Optional[str] = None
        
    task_status: Optional[str] = None
    task_remark: Optional[str] = None
    create_by: Optional[str] = None
    complete_file_path: Optional[str] = None  # Assuming this is a binary file path
    file_type: Optional[str] = None
    project_id: Optional[str] = None
    
class TaskRequestCreatenew(BaseModel):
    task_title: Optional[str] = None
    task_details: Optional[str] = None
    task_file_image: Optional[List[str]] = None
    task_priority: Optional[str] = None
    task_status: Optional[str] = None
    from_date_time: Optional[datetime] = None
    to_date_time: Optional[datetime] = None
    task_type_status: Optional[str] = None
    create_by: Optional[str] = None
    created_by_type : Optional[str] = None
    admin_emp_id : Optional[str] = None
    project_id: Optional[str] = None

    updated_by_type : Optional[str] = None
    updated_admin_emp_id : Optional[str] = None
    task_file_image: List[str]

class TaskRequestCreatelist(BaseModel):
    customer_id: int
    admin_id: Optional[int] = None
    emp_id_from: Optional[str] = None
    emp_id_to: Optional[str] = None
    tasks: List[TaskRequestCreatenew]


class TaskRequestCount(BaseModel):
    admin_id: Optional[str] = None
    employee_id: Optional[str] = None

class EmpRequestCount(BaseModel):
    admin_id: Optional[int] = None

class AttendenceRequestCount(BaseModel):
    admin_id: Optional[str] = None
    employee_id: Optional[str] = None
    from_date: Optional[date] = None
    to_date: Optional[date] = None
    
    
    @validator('from_date', 'to_date', pre=True)
    def empty_string_to_none(cls, value):
        if value == "":
            return None
        return value
        
        
        
    