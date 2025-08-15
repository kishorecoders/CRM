from typing import List
from sqlmodel import Session
from src.Rfq.models import Rfq, RfqCreate, RfqRead,RfqUpdate
from typing import Optional
from sqlalchemy.future import select
from sqlalchemy import desc
from src.StoreManagerPurchase.models import StoreManagerPurchase
from sqlalchemy import update
from src.parameter import get_current_datetime
from src.AdminAddEmployee.models import AdminAddEmployee
from src.Notifications.models import Notification
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew


def create_rfq_record_old(db: Session, request: RfqCreate):
    new_rfq = Rfq(**request.dict())
    db.add(new_rfq)
    db.commit()
    db.refresh(new_rfq)

    empname = None
    if new_rfq.employee_id:
        empname = db.query(AdminAddEmployee.employe_name).filter(AdminAddEmployee.id == new_rfq.employee_id).first()
    else:
        empname = db.query(SuperAdminUserAddNew.full_name).filter(SuperAdminUserAddNew.id == new_rfq.admin_id).first()

    # Create notification for the admin
    notification = Notification(
        admin_id=new_rfq.admin_id,
        title="New RFQ Created",
        description=f"A new RFQ has been created by {empname}.",
        type="RFQ",
        object_id=str(new_rfq.id),
        created_by_id=new_rfq.employee_id if new_rfq.employee_id not in [None, ""] else new_rfq.admin_id,
        created_by_type="employee" if new_rfq.employee_id not in [None, ""] else "admin"
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return {
        "status": "true",
        "message": "RFQ created successfully"
    }
    
    
    
def create_rfq_record(db: Session, request: RfqCreate):
    new_rfq = Rfq(**request.dict())
    db.add(new_rfq)
    db.commit()
    db.refresh(new_rfq)

    # ? Update rfq_create = "1" where admin_id and request_id match
    db.execute(
        update(StoreManagerPurchase)
        .where(
            StoreManagerPurchase.admin_id == request.admin_id,
            StoreManagerPurchase.id == request.req_id
        )
        .values(rfq_create="1", updated_at=get_current_datetime())
    )
    db.commit()

    return {
        "status": "true",
        "message": "RFQ created successfully"
    }




def get_rfq_list(db: Session, admin_id: str, employee_id: Optional[str] = None) -> List[Rfq]:
    query = select(Rfq).where(Rfq.admin_id == admin_id)

    if employee_id:
        query = query.where(Rfq.employee_id == employee_id)

    
    
    query = query.order_by(desc(Rfq.id))  

    rfq_records = db.scalars(query).all()
    
    
    return rfq_records
    
    
    
    
    
    
def update_rfq_record(db: Session, request: RfqUpdate):
    rfq = db.query(Rfq).filter(Rfq.id == request.id).first()

    if not rfq:
        return {"status": "false", "message": f"RFQ with ID {request.id} not found"}

    # Overwrite all updatable fields
    for field in RfqBase.__fields__:
        setattr(rfq, field, getattr(request, field))

    rfq.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(rfq)

    return {
        "status": "true",
        "message": "RFQ updated successfully",
        "data": {
            "id": rfq.id,
            "rfq_id": rfq.rfq_id
        }
    }
