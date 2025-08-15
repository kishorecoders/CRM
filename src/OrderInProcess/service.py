from sqlalchemy.orm import Session
from datetime import datetime
from sqlmodel import select
from src.ProjectManagerOrder.models import ProjectManagerOrder
from src.ProductStages.models import ProductStages
from src.AdminSales.models import AdminSales
from src.QuotationProductEmployee.models import QuotationProductEmployee
from src.AdminAddEmployee.models import AdminAddEmployee
from src.DesignHandover.models import DesignHandover

def get_order_progress_service(request, session: Session):
    
    order_query = select(ProjectManagerOrder).where(
        ProjectManagerOrder.admin_id == request.admin_id,
        ProjectManagerOrder.id == request.order_id,
        ProjectManagerOrder.status == "Won"
    )
    # order_entry = session.exe(order_query).first()
    order_entry = session.execute(order_query).scalars().first()

    order_placed = order_entry is not None
    order_create_date = (
        order_entry.created_at.strftime("%Y-%m-%d %H:%M:%S") if order_entry and order_entry.created_at else None
    )

    design_handover_query = select(DesignHandover).where(
        DesignHandover.admin_id == request.admin_id,
        DesignHandover.order_id == request.order_id,
        DesignHandover.product_id == request.product_id
    )
    # design_handover_entry = session.exec(design_handover_query).first()
    design_handover_entry = session.execute(design_handover_query).scalars().first()

    design_handover = design_handover_entry is not None

    # Ensure `date_time` is a `datetime` object before calling `strftime`
    design_handover_date = None
    if design_handover_entry and design_handover_entry.date_time:
        if isinstance(design_handover_entry.date_time, str):
            try:
                design_handover_date = datetime.fromisoformat(design_handover_entry.date_time).strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                design_handover_date = design_handover_entry.date_time  # Keep as is if format is unknown
        else:
            design_handover_date = design_handover_entry.date_time.strftime("%Y-%m-%d %H:%M:%S")

    design_handover_file = (
        design_handover_entry.file if design_handover_entry else None
    )

    stages_query = select(ProductStages).where(
        ProductStages.product_id == request.product_id,
        ProductStages.type == request.product_type
    )
    # stages = session.exec(stages_query).all()
    stages = session.execute(stages_query).scalars().all()

    stage_list = []
    for stage in stages:
        employee_detail = {}
        if stage.assign_employee:
            employee_query = select(AdminAddEmployee).where(AdminAddEmployee.id == stage.assign_employee)
            # employee = session.exec(employee_query).first()
            employee = session.execute(employee_query).scalars().first()
            if employee:
                employee_detail = {
                    "employee_id": employee.employee_id,
                    "name": employee.employe_name,
                    "email": employee.employe_email_id,
                    "phone": employee.employe_phone_number,
                    "job_title": employee.employe_job_title
                }

        stage_data = {
            "step_name": stage.steps,
            "status": stage.status == "Completed",
            "assign_date_time": stage.assign_date_time.strftime("%Y-%m-%d %H:%M:%S") if stage.assign_date_time else None,
            "stage_detail": {
                "step_id": stage.step_id,
                "time_required": stage.time_riquired_for_this_process,
                "day": stage.day,
                "remark": stage.remark,
                "assign_employee": stage.assign_employee,
                "steps": stage.steps,
                "step_item": stage.step_item,
                "assign_date_time": str(stage.assign_date_time),
                "date_time":stage.date_time,
                "status":stage.status,
            },
            "assign_employee_detail": employee_detail
        }
        stage_list.append(stage_data)

    res = {
        "order_placed": order_placed,
        "order_create_date": order_create_date,
        "design_handover": design_handover,
        "design_handover_date": design_handover_date,
        "design_handover_file": design_handover_file,
        "stages_list": stage_list
    }
    
    return res
