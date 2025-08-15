from .models import DesignHandover,DesignHandoverCreate,DesignHandoverRead
from sqlmodel import Session
from src.ProjectManagerOrder.models import ProjectManagerOrder
from src.AdminAddEmployee.models import AdminAddEmployee
from src.QuotationProductEmployee.models import QuotationProductEmployee


def create_design_handover(db: Session, handover_create: DesignHandoverCreate):
    missing_fields = []
    if not handover_create.admin_id:
        missing_fields.append("admin_id")
    if not handover_create.product_id:
        missing_fields.append("product_id")
    if not handover_create.order_id:
        missing_fields.append("order_id")
    if not handover_create.file:
        missing_fields.append("file")
    if not handover_create.type:
        missing_fields.append("type")
    
    if missing_fields:
        return {
            'status': 'false',
            'message': f"The {', '.join(missing_fields)} field is required."
        }

    db_handover = DesignHandover(**handover_create.dict())
    db.add(db_handover)
    db.commit()
    db.refresh(db_handover)
    
    return {
        'status': 'true',
        'message': "Design Handover Added Successfully",
        'data': db_handover
    }



# def get_design_handover(db: Session, request_data: DesignHandoverRead):
#         missing_fields = []
#         if not request_data.admin_id:
#             missing_fields.append("admin_id")
        
#         if missing_fields:
#             return {
#                 'status': 'false',
#                 'message': f"The {', '.join(missing_fields)} field is required."
#             }
        
#         query = db.query(DesignHandover).filter(DesignHandover.admin_id == request_data.admin_id)
#         if request_data.employee_id:
#             query = query.filter(DesignHandover.employee_id == request_data.employee_id)
        
#         #handovers = query.all()
#         handovers = query.order_by(DesignHandover.id.desc()).all()
        
#         return {
#             'status': 'true',
#             'message': "Design Handovers Fetched Successfully",
#             'data': handovers
#         }

from src.Quotation.models import Quotation
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew

        
def get_design_handover(db: Session, request_data: DesignHandoverRead):
    missing_fields = []
    if not request_data.admin_id:
        missing_fields.append("admin_id")

    if missing_fields:
        return {
            'status': 'false',
            'message': f"The {', '.join(missing_fields)} field is required."
        }

    query = db.query(DesignHandover).filter(DesignHandover.admin_id == request_data.admin_id)

    if request_data.employee_id:
        query = query.filter(DesignHandover.employee_id == request_data.employee_id)

    handovers = query.order_by(DesignHandover.id.desc()).all()

    result_data = []
    employee_name = None
    for handover in handovers:

        if handover.employee_id and str(handover.employee_id).isdigit():
            employee = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == int(handover.employee_id)).first()
            employee_name = employee.employe_name if employee else None
        else:
            employee = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == int(handover.admin_id)).first()
            employee_name = employee.full_name if employee else None

        
        order = db.query(ProjectManagerOrder).filter(ProjectManagerOrder.id == handover.order_id).first()
        order_code = order.order_id if order else None
        
        
        product = db.query(QuotationProductEmployee).filter(QuotationProductEmployee.id == handover.product_id).first()
        product_code = product.product_code if product else None


        sales_order_id = None
        if order.status == "Manual" :
            sales_order_id = order.manual_sale_order_id if order.status == "Manual" else None

        if order.status == "Won":
            quot = db.query(Quotation).filter(Quotation.id == order.quotation_id).first()
            sales_order_id = quot.pi_number if quot else None


        handover_data = handover.dict()  
        handover_data["employee_name"] = employee_name 
        handover_data["order_code"] = sales_order_id if sales_order_id else None  
        handover_data["product_code"] = product_code

        result_data.append(handover_data)

    return {
        'status': 'true',
        'message': "Design Handovers Fetched Successfully",
        'data': result_data
    }
