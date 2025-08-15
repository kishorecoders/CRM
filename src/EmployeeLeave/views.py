from typing import List
from fastapi import APIRouter, Depends, HTTPException, status,Header,Body
from sqlmodel import Session
from src.database import get_db
from typing import Optional, List
from src.EmployeeLeave.models import EmployeeLeaveCreate,EmployeeLeave,EmployeeLeaveStatusUpdate,EmployeeLeaveUpdate,EmployeeLeaveDelete
from src.EmployeeLeave.service import create,get_leave_list_service,update_leave_status,update_leave_details,delete_leave_record
from src.parameter import get_token
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/create-leave")
def create_leave_details(
    leave: EmployeeLeaveCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
   
    if auth_token != get_token():  
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    
    return create(db=db, leave=leave)


@router.post("/get-leave-list", response_model=dict)
def get_leave_list(
    admin_id: Optional[str] = Body(None),
    employee_id: Optional[str] = Body(None),
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db),
):
    try:
       
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}

      
        results = get_leave_list_service(db=db, admin_id=admin_id, employee_id=employee_id)

        if not results:
            return {"status": "true", "message": "No leave records found", "data": []}

        return {"status": "true", "message": "Leave records fetched successfully", "data": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail={"status": "false", "message": str(e)})
    




@router.post("/update-leave-status")
def update_leave_status_api(
    leave_data: EmployeeLeaveStatusUpdate,
    db: Session = Depends(get_db)
):
    try:
        
        updated_leave = update_leave_status(db, leave_data)

        
        response = {
            'status': 'true',
            'message': "Leave status updated successfully",
            'data': {
                "id": updated_leave.id,
                "admin_id": updated_leave.admin_id,
                "employee_id": updated_leave.employee_id,
                "leave_type": updated_leave.leave_type,
                "start_date": updated_leave.start_date.strftime("%Y-%m-%d %I:%M %p"),
                "end_date": updated_leave.end_date.strftime("%Y-%m-%d %I:%M %p"),
                "leave_priority": updated_leave.leave_priority,
                "pdf_file_or_image": updated_leave.pdf_file_or_image,
                "type": updated_leave.type,
                "leave_matter": updated_leave.leave_matter,
                "status": updated_leave.status,
                "remark":updated_leave.remark,
            }
        }
        return response

    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                'status': 'false',
                'message': e.detail
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                'status': 'false',
                'message': "An unexpected error occurred"
            }
        )
    

@router.post("/update-leave")
def update_leave_details_route(
    leave_update: EmployeeLeaveUpdate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

  
    return update_leave_details(db=db, leave_update=leave_update)




@router.post("/delete-leave")
def delete_leave_record_route(
    leave_delete: EmployeeLeaveDelete,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
  
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    return delete_leave_record(db=db, leave_delete=leave_delete)