from typing import List, Optional
from sqlmodel import Session

from src.ActivityComment.models import ActivityComment,ActivityCommentCreate,ActivityCommentResponse
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status,HTTPException
from src.AdminSales.models import AdminSales
from src.AdminAddEmployee.models import AdminAddEmployee
from sqlalchemy.exc import SQLAlchemyError
from src.parameter import get_token




def create_activity_comment(db: Session, activity_comment: ActivityCommentCreate):
    
    existing_comment = db.query(ActivityComment).filter(
        ActivityComment.activity_id == activity_comment.activity_id,
        ActivityComment.admin_emp_id == activity_comment.admin_emp_id,
        ActivityComment.activity_comment_id == activity_comment.activity_comment_id,
        ActivityComment.type == activity_comment.type
    ).first()

    if existing_comment:
        response = {
            'status': 'false',
            'message': "Comment with the same type already added for this activity ID and admin employee ID."
        }
        return response

   
    db_activity_comment = ActivityComment(**activity_comment.dict())
    db.add(db_activity_comment)
    db.commit()
    db.refresh(db_activity_comment)

    response = {
        'status': 'true',
        'message': "Activity comment added successfully",
        'data': db_activity_comment
    }
    return response





def get_activity_comments(db: Session, activity_id: str) -> dict:
    
    comments = db.query(ActivityComment).filter(ActivityComment.activity_id == activity_id).all()

    
    if not comments:
        return {
            "status": "false",
            "message": "No comments found for the given activity ID",
            "data": []
        }

   
    response_data = [
        ActivityCommentResponse(
            id=comment.id,
            activity_id=comment.activity_id,
            admin_emp_id=comment.admin_emp_id,
            activity_comment=comment.activity_comment,
            activity_comment_id=comment.activity_comment_id,
            type=comment.type,
            activity_docs=comment.activity_docs,
            created_at=comment.created_at.isoformat(),
            updated_at=comment.updated_at.isoformat(),
        )
        for comment in comments
    ]

    
    return {
        "status": "true",
        "message": "Comments retrieved successfully",
        "data": response_data
    }




def delete_activity_comment_service(activity_id: str, activity_comment_id: str, db: Session):
   
    comment = db.query(ActivityComment).filter(
        ActivityComment.activity_id == activity_id,
        ActivityComment.id == activity_comment_id
    ).first()

    if not comment:
        return {"status": "false", "message": "Comment not found"}

    
    db.delete(comment)
    db.commit()

    return {"status": "true", "message": "Comment deleted successfully"}


