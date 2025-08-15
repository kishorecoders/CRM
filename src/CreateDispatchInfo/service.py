from .models import DispatchInfoCreate , DispatchInfo , DispatchListRequest
from sqlmodel import Session, select
from sqlalchemy import cast
from sqlalchemy.types import String
from sqlalchemy import desc



def create(db: Session, dispatch_create: DispatchInfoCreate):
   
    
    db_dispatch = DispatchInfo(**dispatch_create.dict())
    db.add(db_dispatch)
    db.commit()
    db.refresh(db_dispatch)
    
    return {
        'status': 'true',
        'message': "Dispatch Added Successfully",
        'data': db_dispatch
    }



def get_dispatch_list(db: Session, request: DispatchListRequest):
    query = select(DispatchInfo).where(DispatchInfo.admin_id == request.admin_id)

    if request.employee_id:
        query = query.where(DispatchInfo.employee_id == request.employee_id)

    dispatches = db.execute(query).scalars().all()

    if not dispatches:
        return {
            'status': 'false',
            'message': 'No dispatch records found.'
        }

    return {
        'status': 'true',
        'message': 'Dispatch records fetched successfully.',
        'data': dispatches
    }

