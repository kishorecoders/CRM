from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session
from src.database import get_db
from src.SuperAdminPlanAndPrice.models import SuperAdminPlanAndPrice, SuperAdminPlanAndPriceCreate
from src.SuperAdminPlanAndPrice.service import create, get_all_plan_price, get_plan_by_id, update, plan_by_plan_id, \
    delete_plan, reactive_plan
from src.parameter import get_token

router = APIRouter()


@router.get("/ShowPlanAndPrice")
def get_plan(auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_all_plan_price(db=db)

    return inner_get_plan(auth_token)


@router.post("/CreatePlanAndPrice")
def create_plan(super_admin_plan_price: SuperAdminPlanAndPriceCreate,
                auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return create(db=db, super_admin_plan_price=super_admin_plan_price)

    return inner_get_plan(auth_token)


@router.get("/ShowPlanAndPriceByPlanId/{plan_id}")
def read_plan_by_id(plan_id: int, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                    db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_plan_by_id(plan_id=plan_id, db=db)

    return inner_get_plan(auth_token)


@router.put("/UpdatePlanAndPrice/{plan_id}")
def update_plan(plan_id: int, super_admin_plan_price: SuperAdminPlanAndPriceCreate,
                auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return update(plan_id=plan_id, super_admin_plan_price=super_admin_plan_price, db=db)

    return inner_get_plan(auth_token)


@router.get("/plan_id/{plan_id}")
def get_plan_by_id(plan_id: int, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                   db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return plan_by_plan_id(plan_id=plan_id, db=db)

    return inner_get_plan(auth_token)


# @router.get("/delete_plan/{plan_id}")
# def delete_plan_by_plan_id(plan_id: int, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#                            db: Session = Depends(get_db)):
#     def inner_get_plan(auth_token: str):
#         if auth_token != get_token():
#             return {"status": "false", "message": "Unauthorized Request"}
#         else:
#             return delete_plan(plan_id=plan_id, db=db)

#     return inner_get_plan(auth_token)
@router.get("/delete_plan/{plan_id}")
def delete_plan_by_plan_id(
    plan_id: int,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db),
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    return delete_plan(plan_id=plan_id, db=db)


@router.get("/reactivate_plan/{plan_id}")
def reactivate_plan_by_plan_id(plan_id: int,
                               auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                               db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return reactive_plan(plan_id=plan_id, db=db)

    return inner_get_plan(auth_token)
