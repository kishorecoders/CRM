

from .models import ProjectManagerOrder,ProjectManagerOrderCreate,StatusUpdate,UpdateHoldStatus
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status,HTTPException
from sqlalchemy import func,or_
from typing import List, Dict
from src.StoreManagerProduct.models import storeManagerProduct 
from src.Productwisestock.models import ProductWiseStock
from src.Category.models import Category
from src.Inventoryoutward.models import InventoryOutward
from collections import defaultdict
from src.QuotationProductEmployee.models import QuotationProductEmployee
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew
from sqlalchemy.orm import Session
import qrcode # type: ignore
import os
import json
from sqlalchemy.orm import aliased
from src.AdminAddEmployee.models import AdminAddEmployee
from src.ProductStages.models import ProductStages
from src.ProductSteps.models import ProductSteps
from typing import List, Dict
from src.Quotation_stages.models import QuotationStages
from src.InventoryOutwardRemark.models import InventoryOutwardRemark
from src.Inventoryoutward.models import InventoryOutward
from src.Quotation.models import Quotation
from src.StoreManagerPurchase.models import StoreManagerPurchase
from src.DeliveryChallan.models import DeliveryChallan
from src.cre_upd_name import get_creator_updator_info ,get_creator_info

from src.Notifications.models import Notification

def get_all_project_manager_order(db: Session):
    data = db.query(ProjectManagerOrder).order_by(ProjectManagerOrder.id.desc()).all()
    response = {'status': 'true', 'message': "Data Received Successfully", 'data': data}
    return response



def get_project_manager_order_by_order_id(db: Session, admin_id: str, order_id: str):
   
    project_manager_order_data = db.query(ProjectManagerOrder).filter(ProjectManagerOrder.admin_id == admin_id, ProjectManagerOrder.order_id == order_id).first()

    if not project_manager_order_data:
        response = {'status': 'false', 'message': "Order not found", 'data': []}
        return response

    
    product_ids = project_manager_order_data.product_id.split(',')

    
    product_details = []
    for product_id in product_ids:
        store_manager_product_data = db.query(storeManagerProduct).filter(storeManagerProduct.id == product_id).first()
        if store_manager_product_data:
            product_details.append(
                store_manager_product_data
            )

    response = {'status': 'true', 'message': "Data Received Successfully", 'data': {'order_details': project_manager_order_data, 'product_details': product_details}}
    return response


def get_project_manager_order_by_admin(db: Session, admin_id: str, search: str = None, emp_id: str = None):
    array = []
    

    ManagerOrderList = db.query(ProjectManagerOrder).filter(ProjectManagerOrder.admin_id == admin_id)

    if emp_id:
        ManagerOrderList = ManagerOrderList.filter(ProjectManagerOrder.emplpoyee_id == emp_id)
    
    print("Before search filter:", ManagerOrderList.all())
    if search:
        ManagerOrderList = ManagerOrderList.filter(
            or_(
                ProjectManagerOrder.order_id.ilike(f"%{search}%"),
                ProjectManagerOrder.customer_name.ilike(f"%{search}%"),
                ProjectManagerOrder.sales_persone_name.ilike(f"%{search}%")
            )
        )
    print("After search filter:", ManagerOrderList.all())


    ManagerOrderList = ManagerOrderList.order_by(ProjectManagerOrder.id.desc()).all()
    
    
    

    created_updated_data_order = {}

    for ManagerOrder in ManagerOrderList:

        sales_order_id = None
        if ManagerOrder.status == "Manual" :
            sales_order_id = ManagerOrder.manual_sale_order_id if ManagerOrder.status == "Manual" else None

        if ManagerOrder.status == "Won":
            quot = db.query(Quotation).filter(Quotation.id == ManagerOrder.quotation_id).first()
            sales_order_id = quot.pi_number if quot else None




        created_updated_data_order = get_creator_updator_info(
            admin_emp_id=ManagerOrder.admin_emp_id,
            created_by_type=ManagerOrder.created_by_type,
            updated_admin_emp_id=ManagerOrder.updated_admin_emp_id,
            updated_by_type=ManagerOrder.updated_by_type,
          db=db
        )
        product_details = []
        
        quotation_data = db.query(Quotation).filter(Quotation.id == ManagerOrder.quotation_id).first()
        pi_number = quotation_data.pi_number if quotation_data else None

        
        product_ids = str(ManagerOrder.product_id).split(',')
        order_status_list = str(ManagerOrder.status).split(',')
        new_quantity_list = str(ManagerOrder.new_quantity).split(',')

        
        order_status_list += ["Unknown"] * (len(product_ids) - len(order_status_list))
        new_quantity_list += ["0"] * (len(product_ids) - len(new_quantity_list))

        productDetails = []
        if ManagerOrder.status == "Manual":
            productDetails = db.query(storeManagerProduct).filter(
                storeManagerProduct.id.in_(product_ids)
            ).all()
        elif ManagerOrder.status == "Won":
            lead_product_query = db.query(QuotationProductEmployee).filter(
                QuotationProductEmployee.quote_id == ManagerOrder.quotation_id
            ).all()
            for product in lead_product_query:
                product_type = db.query(storeManagerProduct).filter(storeManagerProduct.item_code == product.product_code).first()
                product_details.append({
                    'id': product.id,
                    'product_tital': product.product_name,
                    'item_code': product.product_code,
                    'hsn_sac_code': product.hsn_code,
                    'gst_rate': product.gst_percentage,
                    'discription': product.discription,
                    'price_per_product': product.rate_per_unit,
                    'unit': product.unit,
                    'steps': product.steps,
                    'time_riquired_for_this_process': product.time_riquired_for_this_process,
                    'day': product.day,
                    'availability': product.availability,
                    'Stages': getattr(product, 'Stages', None),
                    'type': product_type.type if product_type else "",
                    'manufacture_quantity': product.manufacture_quantity,
                    'available_quantity': product.available_quantity,
                })

        inventory_outward_entry = db.query(InventoryOutward).filter(
            InventoryOutward.admin_id == admin_id,
            InventoryOutward.order_id == ManagerOrder.order_id
        ).first()

        outward_status = "Requested in Outward"
        left_qty = 0

        if inventory_outward_entry:
            if (
                inventory_outward_entry.ask_qty
                and inventory_outward_entry.given_qty
                and int(inventory_outward_entry.ask_qty) == int(inventory_outward_entry.given_qty)
            ):
                outward_status = "Complete"
                left_qty = 0
            else:
                outward_status = "Partially"
                left_qty = int(inventory_outward_entry.ask_qty) - int(inventory_outward_entry.given_qty)

       
        for idx, product_id in enumerate(product_ids):
            order_status = order_status_list[idx]
            new_quantity = new_quantity_list[idx]

            
            product_detail = next((p for p in productDetails if p.id == int(product_id)), None)

            if product_detail:
                product_stock_data = db.query(ProductWiseStock).filter(
                    ProductWiseStock.product_id == int(product_id)
                ).first()

                if product_stock_data:
                    available_quantity = product_stock_data.total_quantity
                    minimum_required_quantity_for_low_stock = product_detail.minimum_requuired_quantity_for_low_stock
                    buffer_until_low_stock = int(available_quantity) - int(minimum_required_quantity_for_low_stock or 0)

                    if int(available_quantity) <= int(minimum_required_quantity_for_low_stock or 0):
                        status = "LOW STOCK"
                    else:
                        status = "AVAILABLE"
                else:
                    available_quantity = 0
                    minimum_required_quantity_for_low_stock = 0
                    buffer_until_low_stock = 0
                    status = "LOW STOCK"

                category_id = product_detail.categories
                category_details = None
                if category_id:
                    category_details = db.query(Category).filter(
                        Category.id == category_id
                    ).first()

                
                product_details.append({
                    **product_detail.__dict__,
                    'new_quantity': new_quantity,
                    'order_status': order_status,
                    'available_quantity': available_quantity,
                    'stock_status': status,
                    'buffer_until_low_stock': buffer_until_low_stock,
                    'minimum_required_quantity_for_low_stock': minimum_required_quantity_for_low_stock,
                    'category_details': category_details,
                    'outward_status': outward_status
                })

        
        man = vars(ManagerOrder).copy()
        man['order_id'] = sales_order_id if sales_order_id else ""
        
        temp = {
            "Project_manager_order_details": {**man,**created_updated_data_order,"sale_order_id": pi_number},
            "product_details": product_details
        }
        array.append(temp)

    response = {'status': 'true', 'message': "Data Received Successfully", 'data': array}
    return response















from src.Notifications.models import Notification
from src.FCM import sendPush

def create(db: Session, project_manager_order_create: ProjectManagerOrderCreate):
    admin_id = project_manager_order_create.admin_id
    admin_company_name = db.query(SuperAdminUserAddNew.company_name).filter(SuperAdminUserAddNew.id == admin_id).scalar()
    short_name = admin_company_name[:4].upper()
    current_year = datetime.now().year % 100
    next_year = current_year + 1
    
    prefix = f"{short_name}/{current_year:02d}-{next_year:02d}/"
    latest_order = (
        db.query(func.max(ProjectManagerOrder.order_id))
        .filter(ProjectManagerOrder.order_id.like(f"{prefix}%"))
        .scalar()
    )

    existing_order_number = int(latest_order.split('/')[-1]) if latest_order else 0
    new_order_number = existing_order_number + 1
    new_order_id = f"{prefix}{new_order_number:03d}"

    project_manager_order_create.order_id = new_order_id
    project_manager_order_create.order_by = "Admin"

    if project_manager_order_create.emplpoyee_id:
        created_by_type = "employee"
        admin_emp_id = project_manager_order_create.emplpoyee_id
    else:
        created_by_type = "admin"
        admin_emp_id = project_manager_order_create.admin_id  

    product_list_with_qp_id = []

    for product in project_manager_order_create.product_id_and_quantity:
        store = db.query(storeManagerProduct).filter(storeManagerProduct.id == product.product_id).first()

        total = str(int(product.quantity) * int(store.price_per_product))
        gst_percentage = store.gst_rate.replace('%', '').strip()
        gst_amount = int(total) * (int(gst_percentage) / 100)  
        gross_total = str(int(total) + gst_amount )

                
        Quotation_product = QuotationProductEmployee(
            admin_id = project_manager_order_create.admin_id,
            employee_id = project_manager_order_create.emplpoyee_id,
            quote_id = 0,
            lead_id = project_manager_order_create.lead_id,
            product_name = store.product_tital   ,
            product_code = store.item_code   ,
            hsn_code = store.hsn_sac_code   ,
            rate_per_unit = store.price_per_product   ,
            quantity = product.quantity  ,
            total = total,
            gst_percentage = gst_percentage,
            gross_total = gross_total,
            availability = store.availability   ,
            status = None  ,
            steps = None ,
            time_riquired_for_this_process = store.time_riquired_for_this_process   ,
            day = store.day   ,
            discount_type = None   ,
            discount_amount = None   ,
            discount_percent = None   ,
            unit = store.unit   ,
            order_id = None  ,
            discription = store.discription   ,
            product_payment_type = "Percentage"   ,
            product_cash_balance = "0%"   ,
            product_account_balance = "100%"   ,
            dispatch_status = "Pending"   ,
            give_credit = None   ,
            remark = None   ,
            booked_status = 0 ,
            add_dispatch = False   ,
            product_type = store.type   ,
            product_id = store.id   ,
            specification = None   ,
            available_quantity = product.available_quantity   ,
            manufacture_quantity = product.manufacture_quantity  
        )
        db.add(Quotation_product)
        db.commit()
        db.refresh(Quotation_product)

        # ?? Add quotation_product_id to item
        product_with_id = product.dict()
        product_with_id["quotation_product_id"] = Quotation_product.id  # or the whole object if needed
        product_list_with_qp_id.append(product_with_id)

        stages = db.query(ProductStages).filter(ProductStages.product_id == str(store.id)).all()
        if stages:
            for stage in stages:
                q_stages = ProductStages(
                    admin_id = Quotation_product.admin_id,
                    product_id = Quotation_product.id,
                    steps = stage.steps,
                    time_riquired_for_this_process = stage.time_riquired_for_this_process,
                    day = stage.day,
                    #assign_employee = stage.assign_employee,
                    type = stage.type,
                    step_id = stage.step_id,
                    parent_stage_id = stage.id,
                    created_by_type = created_by_type,
                    admin_emp_id = admin_emp_id
                )
                db.add(q_stages)
                db.commit()
                db.refresh(q_stages)

    data = project_manager_order_create.dict()
    data["product_id_and_quantity"] = product_list_with_qp_id
    data["created_by_type"] = created_by_type
    data["admin_emp_id"] = admin_emp_id
    data["request_date"] = str(datetime.now())

    db_project_manager_order_create = ProjectManagerOrder(**data)
    db.add(db_project_manager_order_create)
    db.commit()
    db.refresh(db_project_manager_order_create)

    empname = None
    if db_project_manager_order_create.created_by_type == "employee":
        empname = db.query(AdminAddEmployee.employe_name).filter(AdminAddEmployee.id == db_project_manager_order_create.admin_emp_id).first()
    else:
        empname = db.query(SuperAdminUserAddNew.full_name).filter(SuperAdminUserAddNew.id == db_project_manager_order_create.admin_id).first()
    # Create notification for the admin
    notification = Notification(
        admin_id=db_project_manager_order_create.admin_id,
        title="New ProjectManagerOrder Manual Created",
        description=f"A new ProjectManagerOrder_Manual has been created by {empname}.",
        type="ProjectManagerOrder_Manual",
        object_id=str(db_project_manager_order_create.id),
        created_by_id=db_project_manager_order_create.admin_emp_id,
        created_by_type=db_project_manager_order_create.created_by_type
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)

    if db_project_manager_order_create.created_by_type == "employee":
        token = None
        token = db.query(SuperAdminUserAddNew.device_token).filter(
            SuperAdminUserAddNew.id == db_project_manager_order_create.admin_emp_id
        ).first()
        if token:
            token = token.device_token
        sendPush(
            msg=f"A new ProjectManagerOrder_Manual has been created by {empname}.",
            token=token,
            title="New ProjectManagerOrder_Manual Created",
            data={
                "ProjectManagerOrder_id": str(db_project_manager_order_create.id),
                "action": "ProjectManagerOrder"
            }
        )

    return {
        'status': 'true',
        'message': "Project Manager Order Details Added Successfully",
        'data': db_project_manager_order_create
    }









   
def update(project_manager_id:int, project_manager_order:ProjectManagerOrder,db:Session):
    
    if project_manager_order.emplpoyee_id:
        updated_by_type = "employee"
        updated_admin_emp_id = project_manager_order.emplpoyee_id
    else:
        updated_by_type = "admin"
        updated_admin_emp_id = project_manager_order.admin_id  
    data = project_manager_order.dict(exclude_unset=True)
    data["updated_admin_emp_id"] = updated_admin_emp_id
    data["updated_by_type"] = updated_by_type

    project_manager_order_update = data
        
    db.query(ProjectManagerOrder).filter(ProjectManagerOrder.id == project_manager_id).update(project_manager_order_update)
    db.commit()
    response = {'status': 'true','message':"Project Manager Order Details Updated Successfully",'data':project_manager_order_update}
    return response






def update_status(project_manager_order_id: int, request_data: StatusUpdate, db: Session):
    Order_data = db.query(ProjectManagerOrder).filter(ProjectManagerOrder.id == project_manager_order_id).first()

    if not Order_data:
        return {"status": 'false', 'message': "Project Manager Order not found"}

    
    Order_data.status = request_data.status
    db.commit()

    return {
        'status': 'true',
        'message': "Project Manager Order Status Update Successfully"
    }



def delete_project_manager_order_by_id(id: int, db: Session):
    project_manager_details = db.query(ProjectManagerOrder).filter(ProjectManagerOrder.id == id).first()

    if not project_manager_details:
       {'status': 'false', 'message': "Project Manager Order not found"}

    db.delete(project_manager_details)
    db.commit()

    response = {
        'status': 'true',
        'message': "Project Manager Order Details deleted successfully"
    }
    
    return response

from datetime import datetime, timedelta
from src.Production.models import Production
from src.DesignHandover.models import DesignHandover
from src.ProjectManagerOrder.models import ProjectManagerOrder

from src.DispatchVendor.models import DispatchVendor
from src.vendor.models import Vendor
from src.PurchaseOrderIssue.models import PurchaseOrderIssue
from src.StoreManagerProduct.models import storeManagerProduct
from src.StoreManagerPurchase.models import StoreManagerPurchase
from src.Category.models import Category
from src.ProductionRequest.models import ProductionRequest



def show_all_count(
        db: Session, 
        admin_id: str,
        emp_id: Optional[str] = None
        ):
    seven_days_ago = datetime.utcnow() - timedelta(days=7)

    total_product_count = db.query(storeManagerProduct).filter(storeManagerProduct.admin_id == admin_id).count()
    total_category_count = db.query(Category).filter(Category.admin_id == admin_id).count()
    total_inventory_count = db.query(InventoryOutward).filter(InventoryOutward.admin_id == admin_id).count()

    total_product_low_stock = db.query(storeManagerProduct).filter(
        storeManagerProduct.admin_id == admin_id,
        storeManagerProduct.opening_stock == "0",
        storeManagerProduct.minimum_requuired_quantity_for_low_stock == "0"
        ).count()
    
    total_updated_product = db.query(storeManagerProduct).filter(
        storeManagerProduct.admin_id == admin_id,
        storeManagerProduct.updated_at >= seven_days_ago,
        storeManagerProduct.updated_at != storeManagerProduct.created_at
    ).count()


    job_card = db.query(Production).filter(Production.admin_id == admin_id)
    if emp_id:
        job_card = job_card.filter(Production.from_employee == emp_id)

    job_card_count = job_card.count()


    design = db.query(DesignHandover).filter(DesignHandover.admin_id == admin_id)
    if emp_id:
        design = design.filter(DesignHandover.employee_id == emp_id)

    DesignHandover_count = design.count()


    project_manager = db.query(ProjectManagerOrder).filter(ProjectManagerOrder.admin_id == admin_id)
    if emp_id:
        project_manager = project_manager.filter(ProjectManagerOrder.emplpoyee_id == emp_id)  # fixed typo here

    order_history = project_manager.count()
    upcoming_order_count = project_manager.filter(
        ProjectManagerOrder.status == "Won",
        ProjectManagerOrder.stage_status == "Pending",
    ).count()


    # purchase
    store_purchase = db.query(StoreManagerPurchase).filter(StoreManagerPurchase.admin_id == admin_id)
    if emp_id:
        store_purchase = store_purchase.filter(StoreManagerPurchase.employe_id == emp_id)  # fixed typo

    request_store_count = store_purchase.count()

    inventry = db.query(storeManagerProduct).filter(storeManagerProduct.admin_id == admin_id)
    if emp_id:
        inventry = inventry.filter(storeManagerProduct.emplpoyee_id == emp_id)  # fixed typo and chained filter

    inventry_count = inventry.count()

    order = db.query(PurchaseOrderIssue).filter(PurchaseOrderIssue.admin_id == admin_id)
    if emp_id:
        order = order.filter(PurchaseOrderIssue.emplpoyee_id == emp_id)  # fixed typo and chained filter

    order_history_count = order.count()

    vendor = db.query(Vendor).filter(Vendor.admin_id == admin_id)
    if emp_id:
        vendor = vendor.filter(Vendor.employe_id == emp_id)  # fixed typo and chained filter

    vendor_count = vendor.count()


    #store
    inventry_count = inventry.count()
    orders = inventry.all()
    product_low_stock_count = 0

    for order in orders:
        opening_stock = 0 if order.opening_stock in [None, 'null', ''] else int(order.opening_stock)

        #opening_stock = 0 if store_manager_product.opening_stock is None else int(store_manager_product.opening_stock)
        minimum_required_quantity = 0 if order.minimum_requuired_quantity_for_low_stock in [None, 'null', ''] else int(order.minimum_requuired_quantity_for_low_stock)
        
        buffer_until_low_stock = opening_stock - minimum_required_quantity

        # Determine stock status
        if opening_stock == 0 and minimum_required_quantity == 0:
            status = "LOW STOCK"
            product_low_stock_count += 1
        elif buffer_until_low_stock < minimum_required_quantity:
            status = "LOW STOCK"
            product_low_stock_count += 1
        else:
            status = "AVAILABLE"

    product_updated_count = db.query(storeManagerProduct).filter(
        storeManagerProduct.admin_id == admin_id,
        storeManagerProduct.updated_at > storeManagerProduct.created_at
        )
    if emp_id:
        product_updated_count = product_updated_count.filter(storeManagerProduct.emplpoyee_id == emp_id)
    product_updated_count = product_updated_count.count()
    
    category = db.query(Category).filter(Category.admin_id == admin_id)
    if emp_id:
        category = category.filter(Category.employe_id == emp_id)

    category_count = category.count()

    request_by_team = db.query(ProductionRequest).filter(ProductionRequest.admin_id == admin_id)
    if emp_id:
        request_by_team = request_by_team.filter(ProductionRequest.employe_id == emp_id)

    request_by_team_count = request_by_team.count()



    response = {
        'status': 'true',
        'message': "Data Received Successfully",
        'total_product_count': total_product_count,
        'total_category_count': total_category_count,
        'total_inventory_count': total_inventory_count,
        'total_product_low_stock': total_product_low_stock,
        'total_updated_product': total_updated_product,
        'product_out_of_stock': "15",
        'fast_moving': "55",
        'medium_moving': "35",
        'slow_moving': "40",
        'static_dead_stock': "15",

        'upcoming_order_count': upcoming_order_count,
        'order_history': order_history,
        'DesignHandover_count': DesignHandover_count,
        'job_card_count': job_card_count,
        
        'request_store_count': request_store_count,
        'inventry_count': inventry_count,
        'order_history_count': order_history_count,
        'vendor_count': vendor_count,

        'store_total_product_count': inventry_count,
        'store_product_low_count': product_low_stock_count,
        'store_categories_count': category_count,
        'store_product_updated_count': product_updated_count,

        'store_request_by_team': request_by_team_count,
        'store_request_purchase': request_store_count,



    }

    return response

def get_pending_orders_for_admin(admin_id: int, db: Session):
    
    orders_in_project_manager = db.query(ProjectManagerOrder.order_id).filter_by(admin_id=admin_id).all()
    orders_in_project_manager = {order[0] for order in orders_in_project_manager} 

    
    orders_in_inventory_outward = db.query(InventoryOutward.order_id).filter_by(admin_id=admin_id).all()
    orders_in_inventory_outward = {order[0] for order in orders_in_inventory_outward}  

   
    pending_orders = orders_in_project_manager - orders_in_inventory_outward
    
    response = {
        'status': 'true',
        'message': "Data Received Successfully",
        'data': list(pending_orders),
    }    

    return response






def fetch_full_order_with_products(db: Session, order_id: int) -> dict:
    admin_product = aliased(storeManagerProduct)
    lead_product =aliased(QuotationProductEmployee)
   

    order = db.query(ProjectManagerOrder).filter(ProjectManagerOrder.id == order_id).first()

    if not order:
        return {}

    order_data = {column.name: getattr(order, column.name) for column in order.__table__.columns}
    if order.order_by=="Admin":


        try:


            admin_products = db.query(admin_product).filter(
                admin_product.id == order.product_id
            ).all() if order.order_by == "Admin" else []


            if not admin_products:
                print(f"No Admin products found for order {order.id}. Adding placeholder product.")
                admin_products = [{
                    "id": order.product_id,
                    "product_tital": "Unknown Product",
                    "quantity": 1,
                    "rate_per_unit": 0,
                    "total": 0,
                    "availability": "Not available",
                    "product_code": "N/A",
                    "gst_percentage": 0,
                    "created_at": order.created_at,
                    "updated_at": order.updated_at,
                }]

            order_data["products"] = []

            for product in admin_products:
                product_data = {
                    "id": product["id"] if isinstance(product, dict) else product.id,
                    "product_name": product["product_tital"] if isinstance(product, dict) else product.product_tital,
                    "quantity": product["quantity"] if isinstance(product, dict) else product.opening_stock,
                    "rate_per_unit": product["rate_per_unit"] if isinstance(product, dict) else product.price_per_product,
                    "total": product["total"] if isinstance(product, dict) else (
                        float(product.opening_stock or 1) * float(product.price_per_product or 0)
                    ),
                    "availability": product["availability"] if isinstance(product, dict) else product.availability,
                    "product_code": product["product_code"] if isinstance(product, dict) else product.item_code,
                    "gst_percentage": product["gst_percentage"] if isinstance(product, dict) else product.gst_rate,
                    "created_at": product["created_at"] if isinstance(product, dict) else product.created_at,
                    "updated_at": product["updated_at"] if isinstance(product, dict) else product.updated_at,
                }

                # Filter stages based on type
                stage_type = "Admin" if order.order_by == "Admin" else "Lead"


                stages = db.query(ProductStages).filter(
                    ProductStages.product_id == product_data["id"],
                    ProductStages.type == stage_type
                ).all()

                product_data["stage"] = [
                    {
                        "id": stage.id,
                        "admin_id": stage.admin_id,
                        "product_id": stage.product_id,
                        "assign_employee": stage.assign_employee or "Unknown",
                        "steps": stage.steps,
                        "time_riquired_for_this_process": stage.time_riquired_for_this_process,
                        "day": stage.day,
                        "type": stage.type,
                        "created_at": stage.created_at,
                        "updated_at": stage.updated_at,
                    }
                    for stage in stages
                ] if stages else [{
                    "id": None,
                    "assign_employee": "None",
                    "steps": "No stages",
                    "day": "N/A",
                    "created_at": order.created_at,
                    "updated_at": order.updated_at,
                }]

                order_data["products"].append(product_data)

                return order_data


        except Exception as e:
            print(f"Product fetch error: {str(e)}")
            admin_products = []
    else:
        try:


            lead_products = db.query(lead_product).filter(
                lead_product.lead_id == order.product_id
            ).all() if order.order_by == "Lead" else []


            if not lead_products:
                print(f"No Admin products found for order {order.id}. Adding placeholder product.")
                lead_products = [{
                    "id": order.product_id,
                    "product_tital": "Unknown Product",
                    "quantity": 1,
                    "rate_per_unit": 0,
                    "total": 0,
                    "availability": "Not available",
                    "product_code": "N/A",
                    "gst_percentage": 0,
                    "created_at": order.created_at,
                    "updated_at": order.updated_at,
                }]

            order_data["products"] = []

            for product in lead_products:
                print("productid",product)
                product_data = {
                    "id": product["id"] if isinstance(product, dict) else product.id,
                    "admin_id": product["admin_id"] if isinstance(product, dict) else product.admin_id,
                    "employee_id": product["employee_id"] if isinstance(product, dict) else product.employee_id,
                    "quote_id": product["quote_id"] if isinstance(product, dict) else product.quote_id,
                    "lead_id": product["lead_id"] if isinstance(product, dict) else product.lead_id,
                    "product_name": product["product_name"] if isinstance(product, dict) else product.product_name,
                    "product_code": product["product_code"] if isinstance(product, dict) else product.product_code,
                    "hsn_code": product["hsn_code"] if isinstance(product, dict) else product.hsn_code,
                    "rate_per_unit": product["rate_per_unit"] if isinstance(product, dict) else product.rate_per_unit,
                    "quantity": product["quantity"] if isinstance(product, dict) else product.quantity,
                    "total": product["total"] if isinstance(product, dict) else product.total,
                    "gst_percentage": product["gst_percentage"] if isinstance(product, dict) else product.gst_percentage,
                    "gross_total": product["gross_total"] if isinstance(product, dict) else product.gross_total,
                    "availability": product["availability"] if isinstance(product, dict) else product.availability,
                    "status": product["status"] if isinstance(product, dict) else product.status,
                    "steps": product["steps"] if isinstance(product, dict) else product.steps,
                    "time_riquired_for_this_process": product["time_riquired_for_this_process"] if isinstance(product, dict) else product.time_riquired_for_this_process,
                    "day": product["day"] if isinstance(product, dict) else product.day,
                    "Stages": product["Stages"] if isinstance(product, dict) else product.Stages,
                    "discount_type": product["discount_type"] if isinstance(product, dict) else product.discount_type,
                    "discount_amount": product["discount_amount"] if isinstance(product, dict) else product.discount_amount,
                    "discount_percent": product["discount_percent"] if isinstance(product, dict) else product.discount_percent,
                    "unit": product["unit"] if isinstance(product, dict) else product.unit,
                    "created_at": product["created_at"] if isinstance(product, dict) else product.created_at,
                    "updated_at": product["updated_at"] if isinstance(product, dict) else product.updated_at,

                }
                print("product_data",product_data)

                
                
                stage_type = "Lead" if order.order_by == "Lead" else "Admin"

                print("stage_type",stage_type)


                stages = db.query(ProductStages).filter(
                    ProductStages.product_id == str(product_data["id"]),
                    ProductStages.type == stage_type
                ).all()
                print("stagestages_type",stages)

                product_data["stage"] = [
                    {
                        "id": stage.id,
                        "admin_id": stage.admin_id,
                        "product_id": stage.product_id,
                        "assign_employee": stage.assign_employee or "Unknown",
                        "steps": stage.steps,
                        "time_riquired_for_this_process": stage.time_riquired_for_this_process,
                        "day": stage.day,
                        "type": stage.type,
                        "created_at": stage.created_at,
                        "updated_at": stage.updated_at,
                    }
                    for stage in stages
                ] if stages else [{
                    "id": None,
                    "assign_employee": "None",
                    "steps": "No stages",
                    "day": "N/A",
                    "created_at": order.created_at,
                    "updated_at": order.updated_at,
                }]

                order_data["products"].append(product_data)

                return order_data


        except Exception as e:
            print(f"Product fetch error: {str(e)}")
            admin_products = []
    


def generate_lead_order_qr(order: ProjectManagerOrder, db: Session) -> str:
    full_order_details = fetch_full_order_with_products(db, order.id)

    if not full_order_details.get("products"):
        print(f"No Lead products found for order {order.id}. QR generation skipped.")
        return ""

    qr_payload = {
        "status": "true",
        "message": "Lead Order fetched successfully",
        "data": [full_order_details]
    }

    qr_data = json.dumps(qr_payload, ensure_ascii=False, default=str)

    if order.qr_code and os.path.exists(order.qr_code):
        os.remove(order.qr_code)

    qr_code = qrcode.make(qr_data)

    if not os.path.exists("uploads/qrcodes"):
        os.makedirs("uploads/qrcodes")

    qr_path = f"uploads/qrcodes/lead_order_{order.id}.png"
    qr_code.save(qr_path)

    order.qr_code = qr_path
    db.add(order)
    db.commit()
    db.refresh(order)

    return qr_path





def generate_admin_order_qr(order: ProjectManagerOrder, db: Session) -> str:
    full_order_details = fetch_full_order_with_products(db, order.id)

    qr_payload = {
        "status": "true",
        "message": "Admin Order fetched successfully",
        "data": [full_order_details]
    }

    qr_data = json.dumps(qr_payload, ensure_ascii=False, default=str)

    if order.qr_code and os.path.exists(order.qr_code):
        os.remove(order.qr_code)

    qr_code = qrcode.make(qr_data)

    if not os.path.exists("uploads/qrcodes"):
        os.makedirs("uploads/qrcodes")

    qr_path = f"uploads/qrcodes/admin_order_{order.id}.png"
    qr_code.save(qr_path)

    order.qr_code = qr_path
    db.add(order)
    db.commit()
    db.refresh(order)

    return qr_path

def generate_and_store_qr(order: ProjectManagerOrder, db: Session) -> str:
    if order.order_by == "Lead":
        return generate_lead_order_qr(order, db)
    elif order.order_by == "Admin":
        return generate_admin_order_qr(order, db)
    else:
        print(f"Unknown order type for order {order.id}. QR generation skipped.")
        return ""
    
def regenerate_qr(order: ProjectManagerOrder, db: Session):
    try:
        qr_path = generate_and_store_qr(order, db)
        if not qr_path:
            print(f"QR Generation skipped for order {order.id} (No products).")
    except Exception as e:
        print(f"QR Generation Error for Order {order.id}: {str(e)}")



from src.DispatchVendor.models import DispatchVendor


# old function
def fetch_by_admin_and_employee(
    db: Session, 
    admin_id: str, 
    employee_id: str = None, 
    availability: str = None, 
    order_id: str = None, 
    is_stage_clear: bool = None, 
    status: str = None,
    product_type:str = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    dispatch_at: Optional[str] = None,

    
    
) -> List[Dict]:
    query = db.query(ProjectManagerOrder).filter(
        ProjectManagerOrder.admin_id == admin_id, 
        #ProjectManagerOrder.status == "Won"
        ProjectManagerOrder.status.in_(["Won", "Manual"])
    )
    
    if employee_id:
        query = query.filter(ProjectManagerOrder.emplpoyee_id == employee_id)
    
    if order_id:
        query = query.filter(ProjectManagerOrder.id == order_id)

    if from_date and to_date:
        start_datetime = datetime.combine(from_date, datetime.min.time())
        end_datetime = datetime.combine(to_date, datetime.max.time())
        query = query.where(
            ProjectManagerOrder.dispatch_at.between(start_datetime, end_datetime)
        )
        
    if dispatch_at:
        start_datetime = datetime.combine(dispatch_at, datetime.min.time())
        end_datetime = datetime.combine(dispatch_at, datetime.max.time())
        query = query.where(
            ProjectManagerOrder.dispatch_at.between(start_datetime, end_datetime)
        )

    query = query.order_by(ProjectManagerOrder.id.desc())
    orders = query.all()

    result = []
    created_updated_data_order = []
    chalan_data = {}
    created_updated_data_chalan = {}
    created_dispatch_data_order = []
    created_hold_by_data_order = []

    vendor_dict = {}

    #store_product_quantity = None

    for order in orders:
        regenerate_qr(order, db)
        order_data = order.dict()
        print("order stage status",order_data["stage_status"])
        print("req status",status)

        created_updated_data_order = get_creator_updator_info(
            admin_emp_id=order.admin_emp_id,
            created_by_type=order.created_by_type,
            updated_admin_emp_id=order.updated_admin_emp_id,
            updated_by_type=order.updated_by_type,
          db=db
        )

        created_dispatch_data_order = get_creator_info(order.dispatch_admin_emp_id, order.dispatch_by_type, db)
        created_dispatch_data_order['dispatch_at'] = order.dispatch_at

        created_hold_by_data_order = get_creator_info(order.hold_admin_emp_id, order.hold_by_type, db)
        created_hold_by_data_order['hold_at'] = order.hold_at



        chalan_order = (
            db.query(DeliveryChallan)
            .filter(DeliveryChallan.order_id == str(order.id))
            .first()
        )
        
        

        
        
        vendor_dict = {}  # ?? reset inside loop to avoid stale data

        if chalan_order and chalan_order.vendor_id:
            vendor_data = db.query(DispatchVendor).filter(DispatchVendor.id == chalan_order.vendor_id).first()
            if vendor_data:
                vendor_dict =  vendor_data.dict()
        
            # Convert SQLAlchemy object to dictionary safely
            chalan_data = vars(chalan_order).copy()
            chalan_data.pop("_sa_instance_state", None)

            created_updated_data_chalan = get_creator_updator_info(
                admin_emp_id=chalan_order.admin_emp_id,
                created_by_type=chalan_order.created_by_type,
                updated_admin_emp_id=chalan_order.updated_admin_emp_id,
                updated_by_type=chalan_order.updated_by_type,
                db=db
            )

            created_updated_data_chalan["creator_info"]["created_at"] = chalan_order.created_at
            created_updated_data_chalan["updater_info"]["updated_at"] = chalan_order.updated_at

        
        product_ids = order.product_id.split(",") if "," in order.product_id else [order.product_id]
        new_quantities = order.new_quantity.split(",") if "," in order.new_quantity else [order.new_quantity]
        product_list = []

        total_stages = 0
        completed_stages = 0

        all_stages_completed = True  
        all_quotation_stages_complited = True
        
        sale_order_id =None
        delivery_address=None
        po_number=None
        share_by_email=None
        share_by_whatsapp=None
        
        if order.quotation_id:
            try:
                quotation_id = int(order.quotation_id)
                sale_order = db.query(Quotation).filter(Quotation.id == quotation_id).first()
                if sale_order:
                    sale_order_id = sale_order.pi_number
                    delivery_address = sale_order.delevery_address
                    po_number = sale_order.po_number
                    share_by_email = sale_order.share_by_email
                    share_by_whatsapp = sale_order.share_by_whatsapp
            except (ValueError, TypeError):
                pass

        for index, product_id in enumerate(product_ids):
            product_data = {}  # Reset for each product
            product_stages = []
            all_stages_completed = True  # Assume true initially
            all_quotation_stages_complited = True
            
            if order.order_by == "Lead":
                lead_product_query = db.query(QuotationProductEmployee).filter(
                    QuotationProductEmployee.quote_id == order.quotation_id
                )

                if availability and product_type:
                    # Apply the filter
                    lead_product_query = lead_product_query.filter(
                        QuotationProductEmployee.availability == availability,
                        db.query(storeManagerProduct.type).filter(storeManagerProduct.item_code == QuotationProductEmployee.product_code).first()==product_type
                    )




                lead_products = lead_product_query.all()
                store_product_quantity = None
     
                for lead_product in lead_products:
                    procure_status = None
                    request_status = None
                    purchase_id = None
                    created_updated_data = {}
                                
                    if lead_product:
                        does_list = db.query(StoreManagerPurchase).filter(
                            StoreManagerPurchase.product_id == lead_product.id
                        ).all()
                    else:
                        does_list = []
                
                    # Iterate through the list to find the first relevant one (not "0")
                    for does in does_list:
                        procure_status = does.procure_status
                        request_status = does.request_status
                        purchase_id = does.id
                        created_updated_data = get_creator_updator_info(
                            admin_emp_id=does.admin_emp_id,
                            created_by_type=does.created_by_type,
                            updated_admin_emp_id=does.updated_admin_emp_id,
                            updated_by_type=does.updated_by_type,
                            db=db
                        )
                        update = does.updated_at
                        create = does.created_at
                        # Inject timestamps
                        created_updated_data["creator_info"]["created_at"] = create
                        created_updated_data["updater_info"]["updated_at"] = update

                    if lead_product:
                        prod = db.query(storeManagerProduct).filter(
                            storeManagerProduct.id == lead_product.product_id
                        ).all()
                    else:
                        prod = []
                    
                    for pr in prod:
                        store_product_quantity = pr.opening_stock

                


                    product_data = lead_product.dict()  # Reset for each product

                    store_product_type = db.query(storeManagerProduct).filter(
                        storeManagerProduct.item_code == lead_product.product_code
                    ).first()  # or .first()[0] if using .first()
                    product_data["product_type"] = store_product_type.type
                    
                    product_stages = []  # Reset for each product's stages
                    all_stages_completed = True  # Assume true for each product

                    lead_stages = db.query(ProductStages).filter(
                        ProductStages.product_id == lead_product.id,  
                        ProductStages.type == "Lead"
                    ).all()
                    
                    inventory = db.query(InventoryOutward).filter(
                        InventoryOutward.product_id == lead_product.id
                    ).first()
                    
                    remark_list = []
                    if inventory:
                        remarks = db.query(InventoryOutwardRemark).filter(
                            InventoryOutwardRemark.InventoryOutward_id == inventory.id
                        ).all()
                        for r in remarks:
                            remark_data = r.dict()
                            if r.emplpoyee_id:
                                employee = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == r.employee_id).first()
                                if employee:
                                    remark_data["admin_emp_short_name"] = f"{employee.employe_name.split()[0]}({employee.employee_id})"
                            else:
                                admin = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == r.admin_id).first()
                                if admin:
                                    remark_data["admin_emp_short_name"] = f"{admin.full_name} (Admin)"
                            remark_list.append(remark_data)
                    else:
                        remark_list = []

                    if not lead_stages:
                        all_stages_completed = True
                        
                    quotation_Product = db.query(QuotationStages).filter(QuotationStages.product_id == lead_product.id).all()
                    for qstage in quotation_Product:
                        product_stage=db.query(ProductStages).filter(ProductStages.id== f'{qstage.stage_id}').first()
                        if product_stage :
                           if qstage.status not in ["Completed", "Expired"]:
                                all_quotation_stages_complited = False

                    for stage in lead_stages:
                        product_step = db.query(ProductSteps).filter(ProductSteps.id == stage.step_id).first()
                        parent_product_stage = db.query(ProductStages).filter(ProductStages.id == stage.parent_stage_id).first()
                        file_path = parent_product_stage.file_path if parent_product_stage else None
                        serial_number =  str(parent_product_stage.serial_number) if parent_product_stage else "0"

                        stage_data = {
                            "id": stage.id,
                            "admin_id": stage.admin_id,
                            "product_id": stage.product_id,
                            "assign_employee": stage.assign_employee,
                            "steps": stage.steps,
                            "step_id": stage.step_id,
                            "position": str(product_step.position) if product_step else "",
                            "time_riquired_for_this_process": stage.time_riquired_for_this_process,
                            "day": stage.day,
                            "type": stage.type,
                            "remark": stage.remark,
                            "parent_stage_id": stage.parent_stage_id,
                            "file_path": file_path,
                            "serial_number": serial_number,
                            "created_at": stage.created_at,
                            "updated_at": stage.updated_at,
                            "date_time": stage.date_time,
                            "assign_date_time": stage.assign_date_time,
                            "previous_date_time": stage.previous_date_time,
                            "previous_employee": stage.previous_employee,
                            "status": stage.status,
                            "selected_product_ids": [] if stage.selected_product_ids is None else list(map(int, stage.selected_product_ids.split(","))),
                            "employee_name": "Unknown",
                            "employee_id": "Unknown",
                            "previous_employee_name": "Unknown",
                            "previous_employee_id": "Unknown"
                        }
                        product_stages.append(stage_data)
                        total_stages += 1

                        if stage_data["status"] not in ["Completed", "Expired"]:
                            all_stages_completed = False
                            
                        if stage_data["status"] == "Completed":
                            completed_stages += 1

                        if lead_product.manufacture_quantity == "0" and lead_product.status == "Approved":
                            all_stages_completed = True

                    sorted_stages = sorted(product_stages, key=lambda x: int(x["serial_number"]) if x["serial_number"].isdigit() else float('inf'))
                    product_data["store_product_quantity"] = store_product_quantity if store_product_quantity is not None else "0"

                    #product_data["store_product_quantity"] = store_product_quantity if store_product_quantity else "0"
                    product_data["stage"] = sorted_stages
                    product_data["stage_status"] = "Completed" if all_stages_completed else "Pending"
                    
                    product_data["inventory_remark"] = remark_list if remark_list else []
                    
                    product_data["quotation_stage_status"] = "Completed" if all_quotation_stages_complited else "Pending"

                    product_data["booked_status"] = lead_product.booked_status
                    product_data["procure_status"] = procure_status if procure_status else "0"
                    product_data["request_status"] = request_status if request_status else "0"
                    product_data["purchase_id"] = str(purchase_id) if purchase_id else ""

                    # **Ensure the product is only appended once**
                    #product_list.append(product_data)
                    product_list.append({**product_data, **created_updated_data})
                # ? Order-level progress
                order_progress_percentage = int((completed_stages / total_stages) * 100) if total_stages > 0 else 0

                #order_data["products"] = product_list
                order_data["progress"] = f"{order_progress_percentage}%"
                order_data["sale_order_id"] = sale_order_id if order.status == "Won" else order.manual_sale_order_id
                order_data["delivery_address"] = delivery_address
                order_data["po_number"] = po_number
                order_data["share_by_email"] = share_by_email
                order_data["share_by_whatsapp"] = share_by_whatsapp


                #result.append(order_data)
                
            elif order.order_by == "Admin":

                store_product = db.query(storeManagerProduct).filter(
                    storeManagerProduct.id == product_id
                ).first()

                quotation_pro = []


                for pro in (order.product_id_and_quantity or []):
                    if pro.get('product_id') == str(store_product.id):
                        quotation_product_id = pro.get('quotation_product_id')
                        if quotation_product_id:
                            q = db.query(QuotationProductEmployee).filter(
                                QuotationProductEmployee.id == quotation_product_id
                            ).first()
                            if q:
                                quotation_pro.append(q)


                procure_status = None
                request_status = None
                purchase_id = None
                created_updated_data = {}

                if store_product:
                    does_list = db.query(StoreManagerPurchase).filter(
                        StoreManagerPurchase.product_id == store_product.id,
                        StoreManagerPurchase.product_manager_id == str(order.id)
                    ).all()
                else:
                    does_list = []
            
                # Iterate through the list to find the first relevant one (not "0")
                for does in does_list:

                    procure_status = does.procure_status
                    request_status = does.request_status
                    purchase_id = does.id
                    created_updated_data = get_creator_updator_info(
                            admin_emp_id=does.admin_emp_id,
                            created_by_type=does.created_by_type,
                            updated_admin_emp_id=does.updated_admin_emp_id,
                            updated_by_type=does.updated_by_type,
                            db=db
                        )
      
                    update = does.updated_at
                    create = does.created_at
                    # Inject timestamps
                    created_updated_data["creator_info"]["created_at"] = create
                    created_updated_data["updater_info"]["updated_at"] = update

                if quotation_pro:
                    for q_pro in quotation_pro:

                        product_data = q_pro.dict()
                        product_stages = []
                        all_stages_completed = True  # Reset before looping

                        admin_stages = db.query(ProductStages).filter(
                            ProductStages.product_id == str(q_pro.id),
                            ProductStages.type == "Admin"
                        ).all()

                        if not admin_stages:
                            all_stages_completed = True

                        quotation_Product = db.query(QuotationStages).filter(QuotationStages.product_id == str(product_id)).all()
                        for qstage in quotation_Product:
                            product_stage=db.query(ProductStages).filter(ProductStages.id== f'{qstage.stage_id}').first()
                            if product_stage :
                                if qstage.status not in ["Completed", "Expired"]:
                                        all_quotation_stages_complited = False


                        for stage in admin_stages:
                            product_step = db.query(ProductSteps).filter(ProductSteps.id == stage.step_id).first()
                            stage_data = {
                                "id": stage.id,
                                "admin_id": stage.admin_id,
                                "product_id": stage.product_id,
                                "assign_employee": stage.assign_employee,
                                "steps": stage.steps,
                                "step_id": stage.step_id,
                                "position": str(product_step.position) if product_step else "",
                                "time_riquired_for_this_process": stage.time_riquired_for_this_process,
                                "day": stage.day,
                                "type": stage.type,
                                "remark": stage.remark,
                                "created_at": stage.created_at,
                                "updated_at": stage.updated_at,
                                "date_time": stage.date_time,
                                "assign_date_time": stage.assign_date_time,
                                "previous_date_time": stage.previous_date_time,
                                "previous_employee": stage.previous_employee,
                                "status": stage.status,
                                "selected_product_ids": [] if stage.selected_product_ids is None else list(map(int, stage.selected_product_ids.split(","))),
                                "employee_name": "Unknown",
                                "employee_id": "Unknown",
                                "previous_employee_name": "Unknown",
                                "previous_employee_id": "Unknown"
                            }
                            product_stages.append(stage_data)
                            total_stages += 1

                            if stage_data["status"] not in ["Completed", "Expired"]:
                                all_stages_completed = False
                                
                            if stage_data["status"] == "Completed":
                                completed_stages += 1
                                
                            if q_pro.manufacture_quantity == "0" and q_pro.status == "Approved":
                                all_stages_completed = True
                                
                        sorted_stages = sorted(product_stages, key=lambda x: int(x["position"]) if x["position"].isdigit() else float('inf'))
                        product_data["stage"] = sorted_stages
                        product_data["stage_status"] = "Completed" if all_stages_completed else "Pending"

                        product_data["quotation_stage_status"] = "Completed" if all_quotation_stages_complited else "Pending"
                        product_data["procure_status"] = procure_status if procure_status else "0"
                        product_data["request_status"] = request_status if request_status else "0"
                        product_data["purchase_id"] = str(purchase_id) if purchase_id else ""
                        product_data["store_product_quantity"] = store_product.opening_stock 

                        product_list.append({**product_data, **created_updated_data})

                    order_progress_percentage = int((completed_stages / total_stages) * 100) if total_stages > 0 else 0

                    order_data["progress"] = f"{order_progress_percentage}%"
                
        #order_data["Delhivery_Chalan"] = chalan_order.dict() if chalan_order else {}
        order_data["vendor"] = vendor_dict if vendor_dict else {}

        order_data["Delhivery_Chalan"] = {**chalan_data, **created_updated_data_chalan}
        order_data["sale_order_id"] = sale_order_id if order.status == "Won" else order.manual_sale_order_id


        order_data["products"] = product_list

        order_data["is_stage_clear"] = all_stages_completed 
        

        

        if status:
            if order_data.get("stage_status") == status:
                result.append({**order_data, **created_updated_data_order,"dispatch_info":created_dispatch_data_order, "hold_info": created_hold_by_data_order})
        else:
            result.append({**order_data, **created_updated_data_order,"dispatch_info":created_dispatch_data_order, "hold_info": created_hold_by_data_order})


    return result




def fetch_by_admin(
    db: Session, order_id: str
) -> List[Dict]:

    query = db.query(ProjectManagerOrder).filter(
        ProjectManagerOrder.id == order_id, ProjectManagerOrder.status == "Won"
    )

    query = query.order_by(ProjectManagerOrder.id.desc())

    orders = query.all()

    result = []
    for order in orders:
        order_data = order.dict()

        if order.order_by == "Lead":
            lead_products_query = db.query(QuotationProductEmployee).filter(
                QuotationProductEmployee.lead_id == order.product_id
            )
            lead_products = lead_products_query.all()
            order_data["products"] = [product.dict() for product in lead_products]

        elif order.order_by == "Admin":
            store_product_query = db.query(storeManagerProduct).filter(
                storeManagerProduct.id == order.product_id
            )
            store_product = store_product_query.first()
            order_data["products"] = [store_product.dict()] if store_product else []

        else:
            order_data["products"] = []

        result.append(order_data)

    return result

from src.AdminAddEmployee.models import AdminAddEmployee
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew

def update_hold_status(request_data: UpdateHoldStatus, db: Session):
    query = db.query(ProjectManagerOrder).filter(
        ProjectManagerOrder.admin_id == request_data.admin_id,
        ProjectManagerOrder.id == request_data.id
    )

    if request_data.employee_id:
        query = query.filter(ProjectManagerOrder.emplpoyee_id == request_data.employee_id)

    order = query.first()

    if not order:
        return {"status": 'false', 'message': "Project Manager Order not found"}

    order.hold_re_status = request_data.hold_re_status
    
    # Set hold_by_name
    if request_data.employee_id:
        employee = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == request_data.employee_id).first()
        order.hold_by_name = employee.employe_name if employee else None
    else:
        admin = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == request_data.admin_id).first()
        order.hold_by_name = admin.full_name if admin else None


    if request_data.hold_remark:
        order.hold_remark = request_data.hold_remark
    if request_data.date_of_hold:
        order.date_of_hold = request_data.date_of_hold

    db.commit()

    return {
        'status': 'true',
        'message': "Project Manager Hold Status Updated Successfully"
    }


