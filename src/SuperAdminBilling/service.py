from .models import SuperAdminBilling, SuperAdminBillingCreate
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status, HTTPException
from src.SuperAdminPlanAndPrice.models import SuperAdminPlanAndPrice
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew


def get_all_billing(db: Session):
    admin_billing = db.query(SuperAdminBilling).order_by(SuperAdminBilling.id.desc()).all()

    data_array = []

    for billing in admin_billing:
        admin_details = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == billing.user_add_new_id).all()

        if admin_details:
            plan_id = admin_details[0].plan_id
            plan_details = None

            if plan_id is not None:
                plan_details = db.query(SuperAdminPlanAndPrice).filter(SuperAdminPlanAndPrice.id == plan_id).first()

            temp = {
                'billing_details': billing.dict(),
                'admin_details': [admin.dict() for admin in admin_details],
                'plan_details': plan_details.dict() if plan_details else None,
            }

            data_array.append(temp)

    response = {
        'status': 'true',
        'message': "Data Received Successfully",
        'data': data_array,
    }

    return response


def create(db: Session, super_admin_billing: SuperAdminBillingCreate):
    db_super_admin_billing = SuperAdminBilling(**super_admin_billing.dict())
    db.add(db_super_admin_billing)
    db.commit()
    db.refresh(db_super_admin_billing)
    response = {'status': 'true', 'message': "Super Admin Billing Create Successfully", 'data': db_super_admin_billing}
    return response


def update(billing_id: int, super_admin_reffral_plan: SuperAdminBilling, db: Session):
    super_admin_billing_update = super_admin_reffral_plan.dict(exclude_unset=True)
    db.query(SuperAdminBilling).filter(SuperAdminBilling.id == billing_id).update(super_admin_billing_update)
    db.commit()
    response = {'status': 'true', 'message': "Data Updated Successfully", 'data': super_admin_billing_update}
    return response
