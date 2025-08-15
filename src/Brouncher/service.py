from .models import Brouncher, BrouncherCreate
from sqlmodel import Session
from src.Settings.models import Setting
from sqlalchemy import cast
from sqlalchemy.types import String
from sqlalchemy import desc


def create(db: Session, brouncher_create: BrouncherCreate):
    db_brouncher = Brouncher(**brouncher_create.dict())
    db.add(db_brouncher)
    db.commit()
    db.refresh(db_brouncher)
    response = {'status': 'true', 'message': "Brouncher Added Successfully", 'data': db_brouncher}
    return response





def get_all_brouncher_by_admin_id(db: Session, admin_id: int) -> dict:
   
    db_brouncher = db.query(Brouncher).filter(Brouncher.admin_id == admin_id).order_by(desc(Brouncher.id)).all()

    if not db_brouncher:
        return{
            "status": "false",
            "message": "Brouncher not found for this admin id",
        }

    response = {
        "status": "true",
        "message": "Brouncher retrieved successfully",
        "data": db_brouncher
    }

    return response



def delete_brouncher(db: Session, admin_id: int, brouncher_id: int) -> bool:
    
    brouncher = db.query(Brouncher).filter(
        Brouncher.admin_id == admin_id,
        Brouncher.id == brouncher_id
    ).first()

    if not brouncher:
        return False

    
    db.delete(brouncher)
    db.commit()
    return True
