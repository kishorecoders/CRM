from sqlmodel import Session
from fastapi import Depends
from .models import ProjectManagerResourseFileDelete, ProjectManagerResourseFile
from src.database import get_db
import json

def delete_project_manager_resource_file(
    request: ProjectManagerResourseFileDelete,
    db: Session
):
    query = db.query(ProjectManagerResourseFile).filter(ProjectManagerResourseFile.id == request.id).first()

    if not query:
        return {"status": "false", "message": "Record does not exist", "data": None}


    try:
        parsed_file_path = json.loads(query.file_path) if query.file_path else {}
    except json.JSONDecodeError:
        parsed_file_path = query.file_path  # return as-is if JSON is invalid
    # Serialize the record before deleting
    deleted_data = {
        "id": query.id,
        "admin_id": query.admin_id,
        "emp_id": query.emp_id,
        "lead_id": query.lead_id,
        "file_path": parsed_file_path
    }

    db.delete(query)
    db.commit()

    return {
        "status": "true",
        "message": "Record deleted successfully",
        "data": deleted_data
    }
