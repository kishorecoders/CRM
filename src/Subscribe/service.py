from .models import  FetchSubscribeRequest, Subscribe, SubscribeCreate
from sqlmodel import Session
from src.AdminAddEmployee.models import AdminAddEmployee
from sqlalchemy import cast
from sqlmodel import Session, select
from datetime import datetime
from src.Account.service import save_base64_file


def create(db: Session, subscribe_create: SubscribeCreate):

    new_record = Subscribe(**subscribe_create.dict())
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    response = {
        "status": "true",
        "message": "Subscription Created Successfully",
        "data": new_record
    }
    return response


def fetch_subscribe_files(db: Session, request: FetchSubscribeRequest):

    query = db.query(Subscribe).filter(Subscribe.admin_id == request.admin_id)

    if request.employee_id not in (None, ""):
        query = query.filter(Subscribe.employee_id == request.employee_id)

    results = query.all()

    return results




