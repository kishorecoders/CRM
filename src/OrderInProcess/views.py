from fastapi import APIRouter, Depends, HTTPException, Header
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import Optional, List
from src.database import get_db
from src.OrderInProcess.service import get_order_progress_service
from src.parameter import get_token

router = APIRouter()

# Request Model
class OrderProgressRequest(BaseModel):
    admin_id: str
    product_id: str
    product_type: str
    order_id: str

# Response Models
class StageDetailResponse(BaseModel):
    step_id: Optional[str]
    time_required: Optional[str]
    day: Optional[str]
    remark: Optional[str]
    assign_employee: Optional[str]
    steps: Optional[str]
    step_item: Optional[str]
    assign_date_time: Optional[str]
    date_time:Optional[str]
    status:Optional[str]

class AssignEmployeeDetailResponse(BaseModel):
    employee_id: Optional[str]
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    job_title: Optional[str]

class StageResponse(BaseModel):
    step_name: str
    status: bool
    assign_date_time: Optional[str]
    stage_detail: StageDetailResponse
    assign_employee_detail: Optional[AssignEmployeeDetailResponse]

class OrderProgressResponse(BaseModel):
    order_placed: bool
    order_create_date: Optional[str] = None
    stages_list: List[StageResponse]
    design_handover: Optional[bool] = None
    design_handover_date: Optional[str] = None
    design_handover_file: Optional[str] = None

@router.post("/get_order_progress", response_model=OrderProgressResponse)
def get_order_progress(
    request: OrderProgressRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    session: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    
    return get_order_progress_service(request, session)
