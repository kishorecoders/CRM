from typing import List,Optional
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from src.Activity.models import ActivityCenter,ActivityCenterCreate,DashboardOverview ,SalesDashboardOverview
from src.Activity.service import create,get_activity_details,update,delete_activity,get_activity_by_employee
from src.parameter import get_token
from src.ProjectManagerOrder.models import ProjectManagerOrder
from src.PurchaseOrderIssue.models import PurchaseOrderIssue
from src.PurchaseOrderProduct.models import PurchaseOrderProduct
from src.ProductStages.models import ProductStages
from src.QuotationProductEmployee.models import QuotationProductEmployee
from src.AddPayment.models import PaymentRequest
from sqlalchemy import func
from src.Quotation.models import Quotation
from datetime import datetime
from src.AdminSales.models import AdminSales
from sqlalchemy import or_

router = APIRouter()


@router.post("/")
def create_activity_center_details(activity_center: ActivityCenterCreate,
                auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return create(db=db, activity_center=activity_center)
    
    return inner_get_plan(auth_token)
    

@router.get("/ShowActivity/{lead_id}")
def read_activity_center_details(lead_id: int, employee_id: Optional[str] = None, name: Optional[str] = None, 
                                 auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), 
                                 db: Session = Depends(get_db)):
    
   
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    
    return get_activity_details(lead_id=lead_id, employee_id=employee_id, name=name, db=db)        
        
    
@router.get("/ShowActivityByEmployee/{employee_id}")
def read_activity_by_employee(employee_id: str, name: Optional[str] = None, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
        def inner_get_plan(auth_token: str):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return get_activity_by_employee(employee_id=employee_id, name=name, db=db)
    
        return inner_get_plan(auth_token)    
     
@router.put("/UpdateActivity/{id}")
def update_reffral_details(id:int,activity_center:ActivityCenterCreate,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db:Session=Depends(get_db)):
       def inner_get_plan(auth_token: str):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return update(activity_id=id,activity_center=activity_center,db=db)
    
       return inner_get_plan(auth_token)
   

@router.delete("/DeleteActivity/{id}")
def delete_activity_details(
    id: int,
    employe_id: Optional[str] = None,
    created_by_type: Optional[str] = None,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
   
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized request")

    created_by_type_new = created_by_type
    response = delete_activity(id=id, employe_id=employe_id, created_by_type= created_by_type_new , db=db)
    return response

from src.AdminSales.models import AdminSales


@router.post("/dashboard_overview")
def dashboard_overview(
    request: DashboardOverview,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {
            'status': 'true',
            'message': "Unauthorized request",
        }

    query = db.query(Quotation).filter(Quotation.admin_id == request.admin_id)

    #if not query.first():
    #    return {
    #        'status': 'true',
    #        'message': "Account not found",
    #    }

    if request.emp_id:
        query = query.filter(Quotation.employe_id == request.emp_id)

    from_date = datetime.strptime(request.from_date, "%Y-%m-%d") if request.from_date else None
    to_date = datetime.strptime(request.to_date, "%Y-%m-%d") if request.to_date else datetime.now()

    if from_date:
        query = query.filter(Quotation.created_at >= from_date)
    if to_date:
        query = query.filter(Quotation.created_at <= to_date)

    lead = db.query(AdminSales).filter(AdminSales.admin_id == request.admin_id)
    if request.emp_id:
        lead = db.query(AdminSales).filter(AdminSales.allocated_emplyee_id == request.emp_id)
    
    total_count = lead.count()

    sales_data = {
        "total_leads": total_count,
        "total_sales": query.with_entities(func.sum(Quotation.total_amount - Quotation.gst)).scalar() or 0,
        "sent": query.filter(Quotation.quotation_status == 1).count(),
        "pending": query.filter(Quotation.quotation_status == 0).count(),
        "rejected": query.filter(Quotation.quotation_status == 2).count(),
        "approved": query.filter(Quotation.quotation_status == 3).count(),
        "converted": query.filter(Quotation.quotation_status == 5).count(),
    }

    total_sale_query = db.query(func.sum(Quotation.total_amount - Quotation.gst)).filter(Quotation.admin_id == request.admin_id)
    total_received_query = db.query(func.sum(PaymentRequest.rcvd_amt)).filter(PaymentRequest.admin_id == request.admin_id)

    if request.emp_id:
        total_sale_query = total_sale_query.filter(Quotation.employe_id == request.emp_id)
        total_received_query = total_received_query.filter(PaymentRequest.emp_id == request.emp_id)

    if from_date:
        total_sale_query = total_sale_query.filter(Quotation.created_at >= from_date)
        total_received_query = total_received_query.filter(PaymentRequest.created_at >= from_date)
    if to_date:
        total_sale_query = total_sale_query.filter(Quotation.created_at <= to_date)
        total_received_query = total_received_query.filter(PaymentRequest.created_at <= to_date)

    total_sale = total_sale_query.scalar() or 0
    total_received = total_received_query.scalar() or 0

    accounts_data = {
        "total_sale": total_sale,
        "total_received": total_received,
        "total_receivable": total_sale - total_received,
    }



    query = db.query(ProjectManagerOrder).filter(ProjectManagerOrder.admin_id == request.admin_id)
    if request.emp_id:
        query = query.filter(ProjectManagerOrder.emplpoyee_id == request.emp_id)

    from_date = datetime.strptime(request.from_date, "%Y-%m-%d") if request.from_date else None
    to_date = datetime.strptime(request.to_date, "%Y-%m-%d") if request.to_date else datetime.now()

    if from_date:
        query = query.filter(ProjectManagerOrder.created_at >= from_date)
    if to_date:
        query = query.filter(ProjectManagerOrder.created_at <= to_date)
     
    total_project_count = query.count()
    ongoing_count = query.filter(ProjectManagerOrder.stage_status == "Pending").count()
    complited_count = query.filter(ProjectManagerOrder.stage_status == "Completed").count()
    dispatch_complited_count = query.filter(ProjectManagerOrder.stage_status == "Dispatch Completed").count()

    orders = query.all()
    ready_to_dispatch_count = 0
    order_in_amount_count = 0

    order_pending_amount_count = 0
    order_complete_amount_count = 0
    

    for order in orders:
        all_stages_completed = True


        if order.stage_status =="Pending":
            lead_products = db.query(QuotationProductEmployee).filter(
                QuotationProductEmployee.quote_id == order.quotation_id
            ).all()
            for lead_product_pending in lead_products:
                product_total = lead_product_pending.gross_total
                order_pending_amount_count += int(product_total)

        if order.stage_status =="Completed":
            lead_products = db.query(QuotationProductEmployee).filter(
                QuotationProductEmployee.quote_id == order.quotation_id
            ).all()
            for lead_product_completed in lead_products:
                product_total = lead_product_completed.gross_total
                order_complete_amount_count += int(product_total)



        if order.order_by == "Lead":
            lead_products = db.query(QuotationProductEmployee).filter(
                QuotationProductEmployee.quote_id == order.quotation_id
            ).all()

            for lead_product in lead_products:
                product_total = lead_product.gross_total
                order_in_amount_count += int(product_total)
                
                lead_stages = db.query(ProductStages).filter(
                    ProductStages.product_id == lead_product.id,
                    ProductStages.type == "Lead"
                ).all()

                if not lead_stages:
                    continue  # no stages to check

                for stage in lead_stages:
                    if stage.status not in ["Completed", "Expired"]:
                        all_stages_completed = False
                        break  # no need to check further

        stage_status = "Completed" if all_stages_completed else "Pending"

        if getattr(order, "stage_status", None) == "Completed" and stage_status == "Completed":
            ready_to_dispatch_count += 1


    order_data = {
        "total_project_count": total_project_count,
        "ongoing_count": ongoing_count,
        "ready_to_dispatch_count": ready_to_dispatch_count,
        "completed_count": complited_count,
        "order_pending_amount_count": order_pending_amount_count,
        "order_complete_amount_count": order_complete_amount_count
    }

    dispatch_data = {
        "ready_to_dispatch_count": ready_to_dispatch_count,
        "dispatch_completed_count": dispatch_complited_count,
        "dispatch_rejected_count": 0,
        "order_in_amount_count": order_in_amount_count
    }



    query = db.query(PurchaseOrderIssue).filter(PurchaseOrderIssue.admin_id == request.admin_id)
    if request.emp_id:
        query = query.filter(PurchaseOrderIssue.emplpoyee_id == request.emp_id)

    from_date = datetime.strptime(request.from_date, "%Y-%m-%d") if request.from_date else None
    to_date = datetime.strptime(request.to_date, "%Y-%m-%d") if request.to_date else datetime.now()

    if from_date:
        query = query.filter(PurchaseOrderIssue.created_at >= from_date)
    if to_date:
        query = query.filter(PurchaseOrderIssue.created_at <= to_date)

    total_project_count = query.count()
    total_ongoing_count = query.filter(PurchaseOrderIssue.last_status == "Pending").count()

    total_amount_of_issues_count = 0
    order_issues = query.all()

    for order_issue in order_issues:
        product = db.query(PurchaseOrderProduct).filter(PurchaseOrderProduct.purchase_order_id == order_issue.id).all()
        for product_item in product:
            product_total = product_item.gross_total
            total_amount_of_issues_count += int(product_total)

    purchase_issue_data = {
        "total_issue_count": total_project_count,
        "total_ongoing_count": total_ongoing_count,
        "total_amount_of_issues_count": total_amount_of_issues_count,
    }

    lead = db.query(AdminSales).filter(AdminSales.admin_id == request.admin_id)
    if request.emp_id:
        lead = db.query(AdminSales).filter(AdminSales.allocated_emplyee_id == request.emp_id)
    
    total_count = lead.count()
    total_hot_count = lead.filter(AdminSales.status == "Won").count()

    lead_data = {
        "total_count": total_count,
        "total_hot_count": total_hot_count,
    }

    return {
        'status': 'true',
        'message': "Data Received Successfully",
        "sales": sales_data,
        "accounts": accounts_data,
        "orders": order_data,
        "dispatch": dispatch_data,
        "purchase_issues": purchase_issue_data,
        "lead_data": lead_data

    }



@router.post("/Sales_dashboard_overview")
def dashboard_overview(
    request: SalesDashboardOverview,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db),
):
    if auth_token != get_token():
        return {
            "status": "false",
            "message": "Unauthorized request",
        }

    admin_sales = db.query(AdminSales).filter(AdminSales.admin_id == request.admin_id).first()
    if not admin_sales:
        data = {
            "leads": {
                "total_leads": 0,
                "total_sales": 0,  
                "warm_count": 0,
                "cold_count": 0,
                "hot_count":0,
                "won_count": 0,
            },
            "quotations": {
                "total_quotations": 0,
                "total_sales": 0,
                "sent": 0,
                "pending": 0,
                "rejected": 0,
                "approved": 0,
            }
        }

        return {
            "status": "true",
            "message": "Sales Dashboard data",
            "data": data
        }


    quotation_query = db.query(Quotation).filter(Quotation.admin_id == request.admin_id)
    if request.allocated_emplyee_id:
        quotation_query = quotation_query.filter(Quotation.employe_id == request.allocated_emplyee_id)

    query = db.query(AdminSales).filter(AdminSales.admin_id == request.admin_id)
    if request.allocated_emplyee_id:
        query = query.filter(AdminSales.allocated_emplyee_id == request.allocated_emplyee_id)

    data = {
        "leads": {
            "total_leads": query.count(),
            "total_sales": 0,  
            "warm_count": query.filter(AdminSales.status == "Warm").count(),
            "cold_count": query.filter(AdminSales.status == "Cold").count(),
            "hot_count": query.filter(AdminSales.status == "Hot").count(),
            "won_count": query.filter(AdminSales.status == "Won").count(),
        },
        "quotations": {
            "total_quotations": quotation_query.count(),
            "total_sales": quotation_query.with_entities(func.sum(Quotation.total_amount - Quotation.gst)).scalar() or 0,
            "sent": quotation_query.filter(Quotation.quotation_status == 1).count(),
            "pending": quotation_query.filter(Quotation.quotation_status == 4).count(),
            "rejected": quotation_query.filter(Quotation.quotation_status == 2).count(),
            "approved": quotation_query.filter(Quotation.quotation_status == 3).count(),
            "converted": quotation_query.filter(Quotation.quotation_status == 5).count(),
        }
    }

    return {
        "status": "true",
        "message": "Sales Dashboard data",
        "data": data
    }

    
    
    