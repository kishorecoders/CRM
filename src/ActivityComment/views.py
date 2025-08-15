from typing import List,Optional
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from src.ActivityComment.models import ActivityCommentCreate,DeleteActivityCommentRequest,ActivityCommentRequest
from src.ActivityComment.service import create_activity_comment,get_activity_comments,delete_activity_comment_service
from src.parameter import get_token

router = APIRouter()



# @router.post("/activity_comment")
# def create_activity_comment_endpoint(
#     activity_comment: ActivityCommentCreate,
#     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#     db: Session = Depends(get_db)
# ):
#     def inner_get_plan(auth_token: str):
#         if auth_token != get_token():
#             return {"status": "false", "message": "Unauthorized Request"}
#         else:
#             return create_activity_comment(db=db, activity_comment=activity_comment)
    
#     return inner_get_plan(auth_token)

@router.post("/activity_comment")
def create_activity_comment_endpoint(
    activity_comment: ActivityCommentCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    
    return create_activity_comment(db=db, activity_comment=activity_comment)




@router.post("/activity_comment_list", response_model=dict)
def get_activity_comments_endpoint(
    request: ActivityCommentRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    
    response = get_activity_comments(db=db, activity_id=request.activity_id)

    return response



@router.post("/delete_activity_comment")
def delete_activity_comment(
    request: DeleteActivityCommentRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
   
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    
    response = delete_activity_comment_service(
        activity_id=request.activity_id,
        activity_comment_id=request.activity_comment_id,
        db=db
    )

    return response