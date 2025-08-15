from .models import SuperAdminReffralAndPlan,SuperAdminReffralAndPlanCreate
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status,HTTPException

def get_all_reffral_plan(db: Session):
    data = db.query(SuperAdminReffralAndPlan).order_by(SuperAdminReffralAndPlan.id.desc()).all()
    response = {'status': 'true', 'message': "Data Received Successfully", 'data': data}
    return response

def create(db: Session, super_admin_reffral_plan: SuperAdminReffralAndPlanCreate):
    cupon_code = super_admin_reffral_plan.cupon_code
    existing_coupon_code = db.query(SuperAdminReffralAndPlan).filter(SuperAdminReffralAndPlan.cupon_code == cupon_code).all()
    if cupon_code and len(existing_coupon_code) > 0:
        return {'status': 'false', 'message': "This cupon_code is already registered. Try another Coupon Code"}
    db_super_admin_reffral_plan = SuperAdminReffralAndPlan(**super_admin_reffral_plan.dict())
    db.add(db_super_admin_reffral_plan)
    db.commit()
    db.refresh(db_super_admin_reffral_plan)
    response = {'status': 'true','message':"Super Admin Reffral Plan Create Successfully",'data':db_super_admin_reffral_plan}
    return response

def get_reffral_plan_by_id(reffral_plan_id: int, db: Session):
    data = db.query(SuperAdminReffralAndPlan).filter(SuperAdminReffralAndPlan.id == reffral_plan_id).all()
    response = {'status': 'true','message':"Data Recived Successfully",'data':data}
    return response
   

def update(reffral_plan_id:int,super_admin_reffral_plan:SuperAdminReffralAndPlan,db:Session):
    super_admin_reffral_plan_update = super_admin_reffral_plan.dict(exclude_unset=True)
    db.query(SuperAdminReffralAndPlan).filter(SuperAdminReffralAndPlan.id == reffral_plan_id).update(super_admin_reffral_plan_update)
    db.commit()
    response = {'status': 'true','message':"Data Updated Successfully",'data':super_admin_reffral_plan_update}
    return response

def reffral_plan_by_reffral_plan_id(reffral_plan_id:int,db:Session):
    data = db.query(SuperAdminReffralAndPlan).filter(SuperAdminReffralAndPlan.id==reffral_plan_id).order_by(SuperAdminReffralAndPlan.id.asc()).all()
    response = {'status': 'true','message':"Data Recived Successfully",'data':data}
    return response


from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew

def delete_reffral_plan_id(reffral_plan_id: int, db: Session):
    plan = db.query(SuperAdminReffralAndPlan).filter(SuperAdminReffralAndPlan.id == reffral_plan_id).first()

    if not plan:
        return {'status': 'false', 'message': "Referral Plan not found."}

    asign = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.plan_id == reffral_plan_id).first()

    if asign:
        if asign.expiry_date and asign.expiry_date > datetime.now():
            return {
                'status': 'false',
                'message': "This Referral Plan is currently assigned to a Super Admin User and not yet expired. You cannot delete it."
            }

    db.delete(plan)
    db.commit()
    return {
        'status': 'true',
        'message': "Super Admin Referral Plan deleted successfully"
    }

    
    
    