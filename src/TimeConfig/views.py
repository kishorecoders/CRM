from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from .service import create_or_update_time_config
from .models import TimeConfigCreate,AdminIDRequest,TimeConfig
from src.database import get_db
from src.parameter import get_token
from fastapi import FastAPI, HTTPException
from sqlmodel import select
from src.AdminAddEmployee.models import AdminAddEmployee

router = APIRouter()


@router.post("/createOrUpdateTimeConfig")
def create_or_update_time_config_route(
    time_config_create: TimeConfigCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    return create_or_update_time_config(db=db, time_config_create=time_config_create)



# @router.post("/getTimeConfigByAdmin")
# def get_time_config_by_admin(
#     admin_id_request: AdminIDRequest,
#     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#     db: Session = Depends(get_db),
# ):
    
#     if auth_token != get_token():
#         raise HTTPException(status_code=401, detail="Unauthorized Request")

    
#     query = select(TimeConfig).where(TimeConfig.admin_id == admin_id_request.admin_id)
#     time_configs = db.exec(query).all()

    
#     if not time_configs:
#         return {
#         "status": "false",
#         "message": "No time configurations found for admin id",
#     }
       

#     return {
#         "status": "true",
#         "message": "Time configurations fetched successfully",
#         "data": time_configs,
#     }


@router.post("/getTimeConfigByAdmin")
def get_time_config_by_admin(
    admin_id_request: AdminIDRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db),
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    query = select(TimeConfig).where(TimeConfig.admin_id == admin_id_request.admin_id)
    time_configs = db.execute(query).scalars().all()

    if not time_configs:
        return {
            "status": "false",
            "message": "No time configurations found for admin id",
        }

    data_with_shifts = []
    for config in time_configs:
        # Define all shift queries
        shift_one_query = select(AdminAddEmployee).where(
            AdminAddEmployee.admin_id == admin_id_request.admin_id,
            AdminAddEmployee.shift_name == "shift-1"
        )
        shift_two_query = select(AdminAddEmployee).where(
            AdminAddEmployee.admin_id == admin_id_request.admin_id,
            AdminAddEmployee.shift_name == "shift-2"
        )
        shift_three_query = select(AdminAddEmployee).where(
            AdminAddEmployee.admin_id == admin_id_request.admin_id,
            AdminAddEmployee.shift_name == "shift-3"
        )
        shift_general_query = select(AdminAddEmployee).where(
            AdminAddEmployee.admin_id == admin_id_request.admin_id,
            AdminAddEmployee.shift_name == "shift-general"
        )

        # Execute and check assignment
        shift_one_assign = db.execute(shift_one_query).first() is not None
        shift_two_assign = db.execute(shift_two_query).first() is not None
        shift_three_assign = db.execute(shift_three_query).first() is not None
        shift_general_assign = db.execute(shift_general_query).first() is not None

        # Add shift assignment flags to the config
        config_with_shifts = config.dict()
        config_with_shifts.update({
            "shift_one_assign": shift_one_assign,
            "shift_two_assign": shift_two_assign,
            "shift_three_assign": shift_three_assign,
            "shift_general_assign": shift_general_assign
        })

        data_with_shifts.append(config_with_shifts)

    return {
        "status": "true",
        "message": "Time configurations fetched successfully",
        "data": data_with_shifts,
    }



# @router.post("/getTimeConfigByAdmin")
# def get_time_config_by_admin(
#     admin_id_request: AdminIDRequest,
#     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#     db: Session = Depends(get_db),
# ):
    
#     if auth_token != get_token():
#         raise HTTPException(status_code=401, detail="Unauthorized Request")

    
#     query = select(TimeConfig).where(TimeConfig.admin_id == admin_id_request.admin_id)
#     time_configs = db.exec(query).all()

#     if not time_configs:
#         return {
#             "status": "false",
#             "message": "No time configurations found for admin id",
#         }

    
#     data_with_shifts = []
#     for config in time_configs:
#         shift_one_query = (
#             select(AdminAddEmployee)
#             .where(
#                 AdminAddEmployee.admin_id == admin_id_request.admin_id,
#                 AdminAddEmployee.shift_name == "shift-1"
#             )
#         )
#         shift_two_query = (
#             select(AdminAddEmployee)
#             .where(
#                 AdminAddEmployee.admin_id == admin_id_request.admin_id,
#                 AdminAddEmployee.shift_name == "shift-2"
#             )
#         )
#         shift_three_query = (
#             select(AdminAddEmployee)
#             .where(
#                 AdminAddEmployee.admin_id == admin_id_request.admin_id,
#                 AdminAddEmployee.shift_name == "shift-3"
#             )
#         )
#         shift_general_query = (
#             select(AdminAddEmployee)
#             .where(
#                 AdminAddEmployee.admin_id == admin_id_request.admin_id,
#                 AdminAddEmployee.shift_name == "shift-general"
#             )
#         )

        
#         shift_one_assign = db.exec(shift_one_query).first() is not None
#         shift_two_assign = db.exec(shift_two_query).first() is not None
#         shift_three_assign = db.exec(shift_three_query).first() is not None
#         shift_general_assign = db.exec(shift_general_query).first() is not None

       
#         config_with_shifts = config.dict()  
#         config_with_shifts.update({
#             "shift_one_assign": shift_one_assign,
#             "shift_two_assign": shift_two_assign,
#             "shift_three_assign": shift_three_assign,
#             "shift_general_assign": shift_general_assign
#         })

#         data_with_shifts.append(config_with_shifts)

   
#     return {
#         "status": "true",
#         "message": "Time configurations fetched successfully",
#         "data": data_with_shifts,
#     }

