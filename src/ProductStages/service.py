from sqlmodel import Session, select
from .models import AssignStageRequest,ProductStages,StageDeleteRequest
from src.StoreManagerProduct.models import storeManagerProduct
from datetime import datetime  
from src.Production.models import Production
from src.QuotationProductEmployee.models import QuotationProductEmployee


from datetime import datetime, timezone 

from datetime import datetime, timedelta
from src.parameter import get_current_datetime  
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import timedelta
from src.database import get_db


import pytz
TZ = pytz.timezone("Asia/Kolkata")



# def assign_or_update_stage(request: AssignStageRequest, db: Session):
#     if request.type == "Admin":
#         product = db.query(storeManagerProduct).filter(
#             storeManagerProduct.id == request.product_id,
#             storeManagerProduct.admin_id == request.admin_id
#         ).first()
#     elif request.type == "Lead":
#         product = db.query(QuotationProductEmployee).filter(
#             QuotationProductEmployee.id == request.product_id,
#             QuotationProductEmployee.admin_id == request.admin_id
#         ).first()
#     else:
#         return {"status": "false", "message": "Invalid type specified"}

    
#     if request.stage_id != 0:
#         existing_stage = db.query(ProductStages).filter(
#             ProductStages.id == request.stage_id,
#             ProductStages.product_id == request.product_id
#         ).first()

#         if existing_stage:
#             existing_stage.steps = request.steps
#             existing_stage.time_riquired_for_this_process = request.time_riquired_for_this_process
#             existing_stage.day = request.day
#             existing_stage.assign_employee = request.assign_employee
#             existing_stage.type = request.type
#             existing_stage.updated_at = datetime.now()
#             existing_stage.step_id = request.step_id
#             existing_stage.step_item = request.step_item
#             #existing_stage.step_id = request.step_id
#             existing_stage.step_item = request.remark
#             existing_stage.date_time = request.date_time
#             db.commit()
#             db.refresh(existing_stage)

           
#             update_production_base(existing_stage.id, request.admin_id, request.assign_employee, db)

#             return {
#                 "status": "true",
#                 "message": "Stage updated successfully",
#                 "stage_id": existing_stage.id
#             }
#         else:
#             return {"status": "false", "message": "Stage not found"}

    
#     else:
#         new_stage = ProductStages(
#             admin_id=request.admin_id,
#             product_id=request.product_id,
#             assign_employee=request.assign_employee,
#             steps=request.steps,
#             time_riquired_for_this_process=request.time_riquired_for_this_process,
#             day=request.day,
#             type=request.type,
#             #step_id=request.step_id,
#             step_id=request.step_id,
#             remark=request.remark,
#             step_item=request.step_item,
#             date_time=request.date_time,
#             created_at=datetime.now(),
#             updated_at=datetime.now()
#         )

#         db.add(new_stage)
#         db.commit()
#         db.refresh(new_stage)

        
#         update_production_base(new_stage.id, request.admin_id, request.assign_employee, db)

#         return {
#             "status": "true",
#             "message": "New stage assigned successfully",
#             "stage_id": new_stage.id
#         }


def assign_or_update_stage(request: AssignStageRequest, db: Session):
  
  
    if request.date_time:
        try:
            # Convert request date_time to datetime object with timezone
            date_time_obj = datetime.fromisoformat(request.date_time).replace(tzinfo=TZ)

            # Get current date & time in IST
            current_time_ist = datetime.now(TZ)

            # Extract only the date part for comparison
            current_date = current_time_ist.date()
            provided_date = date_time_obj.date()

            # Case 1: If the date is in the past ? ? Invalid
            if provided_date < current_date:
                return {"status": "false", "message": "Date cannot be in the past"}

            # Case 2: If the date is today ? Check time
            if provided_date == current_date and date_time_obj.time() <= current_time_ist.time():
                return {"status": "false", "message": "Time must be in the future"}

            # Case 3: If the date is in the future ? ? Accept any time
        except ValueError:
            return {"status": "false", "message": "Invalid date-time format"}



    if request.type == "Admin":
        product = db.query(storeManagerProduct).filter(
            storeManagerProduct.id == request.product_id,
            storeManagerProduct.admin_id == request.admin_id
        ).first()
    elif request.type == "Lead":
        product = db.query(QuotationProductEmployee).filter(
            QuotationProductEmployee.id == request.product_id,
            QuotationProductEmployee.admin_id == request.admin_id
        ).first()
    else:
        return {"status": "false", "message": "Invalid type specified"}

    if not product:
        return {"status": "false", "message": "Product not found"}

    if request.stage_id != 0:
        existing_stage = db.query(ProductStages).filter(
            ProductStages.id == request.stage_id,
            ProductStages.product_id == request.product_id
        ).first()

        if existing_stage:
            
            if existing_stage.assign_employee != request.assign_employee:
                existing_stage.previous_employee = existing_stage.assign_employee
                existing_stage.previous_date_time = existing_stage.date_time

            existing_stage.steps = request.steps
            existing_stage.time_riquired_for_this_process = request.time_riquired_for_this_process
            existing_stage.day = request.day
            existing_stage.assign_employee = request.assign_employee
            existing_stage.type = request.type
            existing_stage.updated_at = datetime.now()
            #existing_stage.step_id = request.step_id
            existing_stage.step_item = request.step_item
            existing_stage.remark = request.remark
            existing_stage.date_time = request.date_time
            existing_stage.assign_date_time = datetime.now() 
            existing_stage.file_path = request.file_path
            existing_stage.serial_number = request.serial_number
            existing_stage.status ="Pending" 
            existing_stage.sub_product_ids = (",".join(map(str, request.sub_product_ids)) if request.sub_product_ids else existing_stage.sub_product_ids)
            existing_stage.selected_product_ids = (",".join(map(str, request.selected_product_ids)) if request.selected_product_ids else existing_stage.selected_product_ids)

            db.commit()
            db.refresh(existing_stage)

            update_production_base(existing_stage.id, request.admin_id, request.assign_employee, db)

            return {
                "status": "true",
                "message": "Stage updated successfully",
                "stage_id": existing_stage.id
            }
        else:
            return {"status": "false", "message": "Stage not found"}

    else:
        new_stage = ProductStages(
            admin_id=request.admin_id,
            product_id=request.product_id,
            assign_employee=request.assign_employee,
            steps=request.steps,
            time_riquired_for_this_process=request.time_riquired_for_this_process,
            day=request.day,
            type=request.type,
            step_id=request.step_id,
            step_item=request.step_item,
            remark=request.remark,
            parent_stage_id=request.parent_stage_id,
            date_time=request.date_time,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            assign_date_time=datetime.now(),
            serial_number=request.serial_number,
            file_path=request.file_path,
            status="Pending",
            sub_product_ids=(",".join(map(str, request.sub_product_ids)) if request.sub_product_ids else None),
            selected_product_ids=(",".join(map(str, request.selected_product_ids)) if request.selected_product_ids else None),
            is_from_product=True,

        )

        db.add(new_stage)
        db.commit()
        db.refresh(new_stage)

        update_production_base(new_stage.id, request.admin_id, request.assign_employee, db)

        return {
            "status": "true",
            "message": "New stage assigned successfully",
            "stage_id": new_stage.id
        }
    







def update_production_base(stage_id: int, admin_id: str, assign_employee: str, db: Session):
    production_record = db.query(Production).filter(
        Production.stage_id == stage_id,
        Production.admin_id == admin_id
    ).first()

    if production_record:
        production_record.assign_employee = assign_employee
        db.commit()
        db.refresh(production_record)



def delete_stage(request: StageDeleteRequest, db: Session):
    
    stage = db.query(ProductStages).filter(
        ProductStages.id == request.stage_id,
        ProductStages.admin_id == request.admin_id,
        ProductStages.product_id == request.product_id
    ).first()

    if not stage:
        return {
            "status": "false",
            "message": "Stage not found"
        }

    
    db.delete(stage)
    db.commit()

    return {
        "status": "true",
        "message": f"Stage deleted successfully"
    }
    
    
    
    

def update_expired_stages(db: Session):
    current_time = get_current_datetime()  

    # Ensure current_time is timezone-aware
    if current_time.tzinfo is None or current_time.tzinfo.utcoffset(current_time) is None:
        current_time = current_time.replace(tzinfo=timezone.utc)  

    print("Current Time:", current_time)

    expired_stages = db.query(ProductStages).filter(
        ProductStages.status != "Completed",
        ProductStages.time_riquired_for_this_process.isnot(None),
        ProductStages.day.in_(["Hours", "Days", "Week"]),
    ).all()

    for stage in expired_stages:
        try:
            required_time = int(stage.time_riquired_for_this_process)
            date_time = stage.date_time  

            # Ensure assign_date_time is also timezone-aware
            if date_time.tzinfo is None or date_time.tzinfo.utcoffset(date_time) is None:
                date_time = date_time.replace(tzinfo=timezone.utc)  

            # Calculate expiration time
            if stage.day == "Hours":
                expiration_time = date_time + timedelta(hours=required_time)
            elif stage.day == "Days":
                expiration_time = date_time + timedelta(days=required_time)
            elif stage.day == "Week":
                expiration_time = date_time + timedelta(weeks=required_time)
            else:
                continue  

            # Debugging logs
            print(f"Stage ID: {stage.id}, Assign Time: {date_time}, Expiration Time: {expiration_time}")

            # Check if expired
            if current_time >= expiration_time:
                stage.status = "Expired"
                stage.updated_at = current_time
                db.add(stage)

        except ValueError:
            continue

    db.commit()



def scheduler_job_wrapper():
    db = next(get_db())
    try:
        update_expired_stages(db)
    finally:
        db.close()



# def start_scheduler1():
#     """Start the scheduler to check expired stages every 60 seconds."""
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(
#         func=lambda: update_expired_stages(next(get_db())),
#         trigger="interval",
#         seconds=60,  
#     )
#     scheduler.start()


def start_scheduler1():
    """Start the scheduler to check expired stages every 60 seconds."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=scheduler_job_wrapper,
        trigger="interval",
        seconds=60,  
    )
    scheduler.start()


    
    
    
    







