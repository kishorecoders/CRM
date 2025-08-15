from typing import List
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from src.SuperAdminReffralAndPlan.models import SuperAdminReffralAndPlan,SuperAdminReffralAndPlanCreate
from src.SuperAdminReffralAndPlan.service import create,get_all_reffral_plan,get_reffral_plan_by_id,reffral_plan_by_reffral_plan_id,update,delete_reffral_plan_id
from src.parameter import get_token

router = APIRouter()

@router.get("/")
def get_all_reffral_details(auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_all_reffral_plan(db=db)
    
    return inner_get_plan(auth_token)

@router.post("/")
def create_reffral_details(super_admin_reffral_plan: SuperAdminReffralAndPlanCreate,
                auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return create(db=db, super_admin_reffral_plan=super_admin_reffral_plan)
    
    return inner_get_plan(auth_token)

# @router.get("/{plan_id}")
# def read_plan_by_id(plan_id: int, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
#         def inner_get_plan(auth_token: str):
#             if auth_token != get_token():
#                return {"status": "false", "message": "Unauthorized Request"}
#             else:
#                 return get_plan_by_id(plan_id=plan_id, db=db)
    
#         return inner_get_plan(auth_token)
     
@router.put("/{reffral_plan_id}")
def update_reffral_details(reffral_plan_id:int,super_admin_reffral_plan:SuperAdminReffralAndPlanCreate,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db:Session=Depends(get_db)):
       def inner_get_plan(auth_token: str):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return update(reffral_plan_id=reffral_plan_id,super_admin_reffral_plan=super_admin_reffral_plan,db=db)
    
       return inner_get_plan(auth_token)

# @router.get("/plan_id/{plan_id}")
# def get_plan_by_id(plan_id:int,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db: Session = Depends(get_db)):
#         def inner_get_plan(auth_token: str):
#             if auth_token != get_token():
#                return {"status": "false", "message": "Unauthorized Request"}
#             else:
#                 return plan_by_plan_id(plan_id=plan_id,db=db)
    
#         return inner_get_plan(auth_token)

@router.delete("/delete_reffral_plan_id/{reffral_plan_id}")
def delete_reffral_plan_by_reffral_plan_id(reffral_plan_id: int, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
        def inner_get_plan(auth_token: str):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return delete_reffral_plan_id(reffral_plan_id=reffral_plan_id, db=db)
    
        return inner_get_plan(auth_token)