# from typing import List, Optional
# from fastapi import APIRouter, Depends, HTTPException, status, Header
# from sqlmodel import Session
# from src.database import get_db
# from .models import SubscribeCreate, FetchSubscribeRequest
# from .service import create, fetch_subscribe_files
# from src.parameter import get_token

# router = APIRouter()

# @router.post("/create_subscribe")
# def create_subscribe(
#     subscribe_create: SubscribeCreate,
#     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#     db: Session = Depends(get_db)
# ):
    
#     if auth_token != get_token():
#         return {"status": "false", "message": "Unauthorized Request"}

#     return create(db=db, subscribe_create=subscribe_create)   


# @router.post("/get_subscribe_files")
# def get_subscribe_files(
#     request: FetchSubscribeRequest,
#     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#     db: Session = Depends(get_db)
# ):
#     if auth_token != get_token():
#         return {"status": "false", "message": "Unauthorized Request"}


#     results = fetch_subscribe_files(db=db, request=request)

#     if not results:
#         return {"status": "false", "message": "No records found"}

#     return {"status": "true", "message": "Subscriptions retrieved successfully", "data": results}





