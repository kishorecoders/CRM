from .models import CreateDispatch, CreateDispatchBase,DispatchListRequest
from sqlmodel import Session, select
from sqlalchemy import cast
from sqlalchemy.types import String
from sqlalchemy import desc



def create(db: Session, dispatch_create: CreateDispatchBase):
   
    missing_fields = []
    if not dispatch_create.admin_id:
        missing_fields.append("admin_id")
    if not dispatch_create.product_id:
        missing_fields.append("product_id")
    if not dispatch_create.vendor_id:
        missing_fields.append("vendor_id")

    if missing_fields:
        return {
            'status': 'false',
            'message': f"The {', '.join(missing_fields)} field is required."
        }

    
    db_dispatch = CreateDispatch(**dispatch_create.dict())
    db.add(db_dispatch)
    db.commit()
    db.refresh(db_dispatch)
    
    return {
        'status': 'true',
        'message': "Dispatch Added Successfully",
        'data': db_dispatch
    }



def get_dispatch_list(db: Session, request: DispatchListRequest):
    query = select(CreateDispatch).where(CreateDispatch.admin_id == request.admin_id)

    if request.employee_id:
        query = query.where(CreateDispatch.employee_id == request.employee_id)

    dispatches = db.exec(query).all()

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