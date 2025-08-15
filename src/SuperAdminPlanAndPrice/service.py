from .models import SuperAdminPlanAndPrice,SuperAdminPlanAndPriceCreate
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status,HTTPException
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew


# def get_all_plan_price(db: Session):
#     data = db.query(SuperAdminPlanAndPrice).all()
#     response = {'status': status.HTTP_200_OK,'message':"Data Recived Successfully",'data':data}
#     return response

def get_all_plan_price(db: Session):
    data = db.query(SuperAdminPlanAndPrice).order_by(SuperAdminPlanAndPrice.id.desc()).all()

    response_data = []

    for form in data:
        plan_details = db.query(SuperAdminPlanAndPrice).filter_by(id=form.id).all()

        if plan_details:
            module_access_details = {
                "admin": plan_details[0].admin,
                "sales": plan_details[0].sales,
                "project_manager": plan_details[0].project_manager,
                "store_engineer": plan_details[0].store_engineer,
                "purchase": plan_details[0].purchase,
                "dispatch": plan_details[0].dispatch,
                "account": plan_details[0].account,
                "customer": plan_details[0].customer,
                "status_update": plan_details[0].status_update,
                "employee_attendance": plan_details[0].employee_attendance,
                "employee_leave": plan_details[0].employee_leave,
                "employee_task": plan_details[0].employee_task,
            }
        else:
            module_access_details = {
                "admin": "default_value",
                "sales": "default_value",
                "project_manager": "default_value",
                "store_engineer": "default_value",
                "purchase": "default_value",
                "dispatch": "default_value",
                "account": "default_value",
                "customer": "default_value",
                "status_update": "default_value",
                "employee_attendance": "default_value",
                "employee_leave": "default_value",
                "employee_task": "default_value",
            }

        temp = {
            'subscription_plan_details': form,
            'module_access_details': module_access_details
        }
        response_data.append(temp)

    response = {'status': 'true', 'message': "Data Received Successfully", 'data': response_data}
    return response



def create(db: Session, super_admin_plan_price: SuperAdminPlanAndPriceCreate):
    plans = db.query(SuperAdminPlanAndPrice).filter(
        SuperAdminPlanAndPrice.plan_type == "Campaign",
        super_admin_plan_price.plan_type == "Campaign"
        ).first()
    if plans:
        return {'status': 'false','message':F"Campaign Plan {plans.name_of_the_subscription} already exist"}


    db_super_admin_plan_price = SuperAdminPlanAndPrice(**super_admin_plan_price.dict())
    db.add(db_super_admin_plan_price)
    db.commit()
    db.refresh(db_super_admin_plan_price)
    response = {'status': 'true','message':"Super Admin Plan And Price Create Successfully",'data':db_super_admin_plan_price}
    return response

def get_plan_by_id(plan_id: int, db: Session):
    data = db.query(SuperAdminPlanAndPrice).filter(SuperAdminPlanAndPrice.id == plan_id).all()
    response = {'status': 'true','message':"Data Recived Successfully",'data':data}
    return response
   

def update(plan_id:int,super_admin_plan_price:SuperAdminPlanAndPriceCreate,db:Session):
    # Check if another Campaign plan exists (excluding the one being updated)
    existing_plan = db.query(SuperAdminPlanAndPrice).filter(
        SuperAdminPlanAndPrice.plan_type == "Campaign",
        SuperAdminPlanAndPrice.id != plan_id,  # Exclude current plan_id
        super_admin_plan_price.plan_type == "Campaign"
    ).first()

    if existing_plan:
        return {
            'status': 'false',
            'message': f"Campaign Plan '{existing_plan.name_of_the_subscription}' already exists"
        }
    super_admin_plan_price_update = super_admin_plan_price.dict(exclude_unset=True)
    db.query(SuperAdminPlanAndPrice).filter(SuperAdminPlanAndPrice.id == plan_id).update(super_admin_plan_price_update)
    db.commit()
    response = {'status': 'true','message':"Data Updated Successfully",'data':super_admin_plan_price_update}
    return response

def plan_by_plan_id(plan_id:int,db:Session):
    data = db.query(SuperAdminPlanAndPrice).filter(SuperAdminPlanAndPrice.id==plan_id).order_by(SuperAdminPlanAndPrice.id.asc()).all()
    response = {'status': 'true','message':"Data Recived Successfully",'data':data}
    return response



# def delete_plan(plan_id: int, db: Session):
#     plan = db.query(SuperAdminPlanAndPrice).filter(SuperAdminPlanAndPrice.id == plan_id).first()
#     if plan:
#         plan.status = "Deactivate"
#         db.commit()
#         db.refresh(plan)
#         return {'status':'true', 'message':"Super Admin Subscription PlanPrice deleted successfully", 'data':plan}
#     return {"status": "Plan not found"}
def delete_plan(plan_id: int, db: Session):
    plan = db.query(SuperAdminPlanAndPrice).filter(SuperAdminPlanAndPrice.id == plan_id).first()
    if not plan:
        return {"status": "false", "message": "Plan not found"}

    
    user_using_plan = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.plan_id == plan_id).first()
    if user_using_plan:
        return {"status": "false", "message": "Cannot delete plan as it is being used by a user"}

    plan.status = "Deactivate"
    db.commit()
    db.refresh(plan)
    return {"status": "true", "message": "Plan deactivated successfully", "data": plan}




def reactive_plan(plan_id: int, db: Session):
    plan = db.query(SuperAdminPlanAndPrice).filter(SuperAdminPlanAndPrice.id == plan_id).first()
    if plan:
        plan.status = "Activate"
        db.commit()
        db.refresh(plan)
        return {'status':'true', 'message':"Super Admin Subscription PlanPrice Re Activate successfully", 'data':plan}
    return {"status": "Plan not found"}