from fastapi import APIRouter, Depends,Header
from sqlmodel import Session
from src.database import get_db
from src.parameter import get_token
import json
from .models import ProjectManagerResourseFileRead ,ProjectManagerResourseFile ,ProjectManagerResourseFileDelete
from  .service import delete_project_manager_resource_file
router = APIRouter()


@router.post("/getProjectManagerResourseFile")
def get_project_manager_resource_file(
    request: ProjectManagerResourseFileRead,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db),
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request", "data": None}

    base_query = db.query(ProjectManagerResourseFile).filter(ProjectManagerResourseFile.admin_id == request.admin_id)

    if request.quotation_id:
        base_query = base_query.filter(ProjectManagerResourseFile.quotation_id == request.quotation_id)

    results = base_query.all()

    if not results:
        return {"status": "false", "message": "No files found", "data": None}

    all_files = []

    for result in results:
        try:
            file_data = json.loads(result.file_path) if result.file_path else None
            if isinstance(file_data, dict):
                file_data.update({
                    "id": result.id,
                    "admin_id": result.admin_id,
                    "emp_id": result.emp_id,
                    "quotation_id": result.quotation_id

                })

                all_files.append(file_data)
        except json.JSONDecodeError:
            continue  # Skip invalid entries

    return {
        "status": "true",
        "message": "File path(s) fetched successfully",
        "data": all_files
    }

@router.post("/ProjectManagerResourseFileDelete")
def resource_file(
    request: ProjectManagerResourseFileDelete,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db),
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    
    return delete_project_manager_resource_file(request= request, db=db)
