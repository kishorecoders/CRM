from .models import PurchaseOrderIssue,PurchaseOrderIssueCreate,PurchaseOrderIssueCreateWithProducts,PurchaseOrderIssueLastStatusUpdate,PurchaseOrderIssueRequest,PurchaseOrderProductBase
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status,HTTPException
from sqlalchemy import func,cast,String,Integer
from src.ProjectManagerOrder.models import ProjectManagerOrder
from src.Productwisestock.models import ProductWiseStock
from src.Category.models import Category
from src.StoreManagerProduct.models import storeManagerProduct
from src.vendor.models import Vendor
from src.StoreManagerPurchase.models import StoreManagerPurchase
from src.PurchaseOrderProduct.models import PurchaseOrderProduct
from src.PaymentTerm.models import PaymentTerm

from src.AdminAddEmployee.models import AdminAddEmployee
from src.Notifications.models import Notification
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew

def get_all_purchase_order_issue(db: Session):
    data = db.query(PurchaseOrderIssue).order_by(PurchaseOrderIssue.id.desc()).all()
    response = {'status': 'true', 'message': "Data Received Successfully", 'data': data}
    return response



def get_purchase_order_issue_history_by_admin(db: Session, admin_id: str, search: Optional[str] = None , order_id: Optional[str] = None):
    array = []

    
    purchase_order_query = db.query(PurchaseOrderIssue).filter(PurchaseOrderIssue.admin_id == admin_id)
    if order_id:
        purchase_order_query = purchase_order_query.filter(PurchaseOrderIssue.id == order_id)
    

    if search:
        purchase_order_query = (
            purchase_order_query
            .join(Vendor, cast(PurchaseOrderIssue.vendor_id, Integer) == Vendor.id)
            .filter(
                (Vendor.vendor_name.ilike(f"%{search}%")) |
                PurchaseOrderIssue.po_number.ilike(f"%{search}%")
            )
        )

    # Order by descending id
    purchase_order_query = purchase_order_query.order_by(PurchaseOrderIssue.id.desc())

    PurchaseOrderList = purchase_order_query.all()
    term_and_condition_details = {}
    payment_term_details = []

    for PurchaseOrder in PurchaseOrderList:
    

        termAndConditions = db.query(PaymentTerm).filter(PaymentTerm.id == PurchaseOrder.term_and_condition).first()
        if termAndConditions is not None:
            term_and_condition_details = {
                'id': termAndConditions.id,
                'admin_id': termAndConditions.admin_id,
                'type': termAndConditions.type,
                'file_path': termAndConditions.file_path,
                'content': termAndConditions.content
            }

        payment_term_details = []
        
        if PurchaseOrder.payment_term:
            for id in PurchaseOrder.payment_term.split(","):
                id = int(id.strip())
                payment = db.query(PaymentTerm).filter(PaymentTerm.id == id).first()
                if payment is not None:
                    payment_term_details.append({
                        'id': payment.id,
                        'admin_id': payment.admin_id,
                        'type': payment.type,
                        'file_path': payment.file_path,
                        'content': payment.content
                    })
                        
        pur_data = vars(PurchaseOrder).copy()
        pur_data["term_and_condition_details"] = term_and_condition_details
        pur_data["payment_term_details"] = payment_term_details
        productDetails = db.query(PurchaseOrderProduct).filter(PurchaseOrderProduct.purchase_order_id == PurchaseOrder.id).all()

        vendorDetails = db.query(Vendor).filter(Vendor.id == PurchaseOrder.vendor_id).all()
        temp = {"Purchase_order_details": pur_data, "vendor_details": vendorDetails,"product_details": productDetails}
        array.append(temp)

    response = {'status': status.HTTP_200_OK, 'message': "Data Received Successfully", 'data': array}
    return response




def get_purchase_order_issue_by_admin(db: Session, admin_id: str):
    array = []
    PurchaseOrderList = db.query(PurchaseOrderIssue).filter(PurchaseOrderIssue.admin_id == admin_id).all()

    for PurchaseOrder in PurchaseOrderList:
        orderDetails = db.query(ProjectManagerOrder).filter(
            ProjectManagerOrder.admin_id == PurchaseOrder.admin_id,
        ).all()

        for orderDetail in orderDetails:
            productDetails = db.query(storeManagerProduct).filter(storeManagerProduct.id == orderDetail.product_id).all()

            for productDetail in productDetails:
                product_stock_data = db.query(ProductWiseStock).filter(ProductWiseStock.product_id == productDetail.id).first()

                if product_stock_data:
                    available_quantity = product_stock_data.total_quantity
                    minimum_required_quantity_for_low_stock = productDetail.minimum_requuired_quantity_for_low_stock
                    buffer_until_low_stock = int(available_quantity) - int(minimum_required_quantity_for_low_stock)

                    if int(available_quantity) <= int(minimum_required_quantity_for_low_stock):
                        status = "LOW STOCK"
                    else:
                        status = "AVAILABLE"
                else:
                    available_quantity = 0
                    minimum_required_quantity_for_low_stock = 0
                    buffer_until_low_stock = 0
                    status = "LOW STOCK"

                
                category_id = productDetail.categories
                category_details = None
                if category_id:
                    category_details = db.query(Category).filter(Category.id == category_id).first()

                product_detail_dict = productDetail.dict()
                product_detail_dict.update({
                    'available_quantity': available_quantity,
                    'status': status,
                    'buffer_until_low_stock': buffer_until_low_stock,
                    'minimum_required_quantity_for_low_stock': minimum_required_quantity_for_low_stock
                })

                temp = {"Purchase_order_details": PurchaseOrder, "order_details": orderDetail, "product_details": product_detail_dict}
                array.append(temp)

    response = {'status': 'true', 'message': "Data Received Successfully", 'data': array}
    return response



def get_financial_year():
    current_year = datetime.now().year
    if datetime.now().month >= 4:  
        return f"{current_year}-{current_year + 1}"
    else:
        return f"{current_year - 1}-{current_year}"
    


def create_order_with_products(db: Session, request: PurchaseOrderIssueRequest):
    order_data = request.order_data
    products = order_data.products

    financial_year = get_financial_year()  
    admin_id = order_data.admin_id
    employee_id = order_data.emplpoyee_id

    # Generate PO number
    if order_data.po_number:
        if not order_data.po_number.startswith(f'PO-{financial_year}/'):
            return {"status": "false", "message": f"Invalid PO number format. Should start with 'PO-{financial_year}/'"}
        existing = db.query(PurchaseOrderIssue).filter(
            PurchaseOrderIssue.po_number == order_data.po_number
        ).first()
        if existing:
            return {"status": "false", "message": f"PO number already exists."}
    else:
        last_bill_number = db.query(func.max(PurchaseOrderIssue.po_number)).filter(
            PurchaseOrderIssue.admin_id == admin_id,
            PurchaseOrderIssue.po_number.like(f'PO-{financial_year}/%')
        ).scalar()
        if last_bill_number:
            _, last_number = last_bill_number.split('/')
            next_number = int(last_number) + 1
        else:
            next_number = 1
        order_data.po_number = f'PO-{financial_year}/{next_number}'

    # Save Order
    order_dict = order_data.dict(exclude={"products"})
    new_order = PurchaseOrderIssue(**order_dict)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)


    empname = None
    if new_order.emplpoyee_id:
        empname = db.query(AdminAddEmployee.employe_name).filter(AdminAddEmployee.id == new_order.emplpoyee_id).first()
    else:
        empname = db.query(SuperAdminUserAddNew.full_name).filter(SuperAdminUserAddNew.id == new_order.admin_id).first()
    # Create notification for the admin
    notification = Notification(
        admin_id=new_order.admin_id,
        title="New Purchase Order Created",
        description=f"A new Purchase Order has been created by {empname}.",
        type="PurchaseOrder",
        object_id=str(new_order.id),
        created_by_id=new_order.emplpoyee_id if new_order.emplpoyee_id not in [None, ""] else new_order.admin_id,
        created_by_type="employee" if new_order.emplpoyee_id not in [None, ""] else "admin",
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)

    # Save each product (auto-filling admin_id, employee_id, order_id)
    for product in products:
        product_dict = product.dict()
        product_dict["admin_id"] = admin_id
        product_dict["purchase_order_id"] = new_order.id
        product_dict["employee_id"] = employee_id
        product_dict["order_id"] = new_order.po_number

        db_product = PurchaseOrderProduct(**product_dict)
        db.add(db_product)

    db.commit()
    orders = get_purchase_order_issue_history_by_admin(admin_id = admin_id ,search = "" ,order_id = new_order.id , db = db)

    return {
        "status": "true",
        "message": "Purchase Order with Products created successfully",
        "data":orders 
        
    }





   

def update(purchase_order_issue_id: int, db: Session, request: PurchaseOrderIssueRequest):
    order_data = request.order_data
    products_data = order_data.products

    # Fetch existing order
    existing_order = db.query(PurchaseOrderIssue).filter(PurchaseOrderIssue.id == purchase_order_issue_id).first()
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Validate PO number format
    financial_year = get_financial_year()
    if order_data.po_number and not order_data.po_number.startswith(f"PO-{financial_year}/"):
        raise HTTPException(status_code=400, detail=f"PO number must start with PO-{financial_year}/")

    # Update fields
    for key, value in order_data.dict(exclude={"products"}, exclude_unset=True).items():
        setattr(existing_order, key, value)

    db.commit()
    db.refresh(existing_order)

    # Delete old products
    db.query(PurchaseOrderProduct).filter(PurchaseOrderProduct.order_id == existing_order.po_number).delete()
    db.commit()

    # Add new products
    for product in products_data:
        product_dict = product.dict()
        product_dict["admin_id"] = order_data.admin_id
        product_dict["employee_id"] = order_data.emplpoyee_id
        product_dict["order_id"] = existing_order.po_number
        db_product = PurchaseOrderProduct(**product_dict)
        db.add(db_product)

    db.commit()

    return {
        "status": "true",
        "message": "Order and products updated successfully",
        "po_number": existing_order.po_number
    }



def show_all_count(db: Session, admin_id: str):

    total_purchase_request_count = db.query(StoreManagerPurchase).filter(StoreManagerPurchase.admin_id == admin_id).count()
    total_order_issue_count = db.query(PurchaseOrderIssue).filter(PurchaseOrderIssue.admin_id == admin_id).count()
    total_vendor_count = db.query(Vendor).filter(Vendor.admin_id == admin_id).count()

    response = {
        'status': 'true',
        'message': "Data Received Successfully",
        'total_purchase_request_count': total_purchase_request_count,
        'total_order_issue_count': total_order_issue_count,
        'total_vendor_count': total_vendor_count,
        'max_product_movment': "45%",
        'medium_product_movment': "30%",
        'min_dead_stock_product_movment': "35"
    }

    return response

def update_status(purchase_order_issue_id: int, request_data: PurchaseOrderIssueLastStatusUpdate, db: Session):
    Purchase_order_data = db.query(PurchaseOrderIssue).filter(PurchaseOrderIssue.id == purchase_order_issue_id).first()

    if not Purchase_order_data:
        return {"status": 'false', 'message': "Purchase Order Issue not found"}

    
    Purchase_order_data.last_status = request_data.last_status
    db.commit()

    return {
        'status': 'true',
        'message': "Purchase Order Issue Last Status Update Successfully"
    }

def delete_purchase_order_issue_by_id(id: int, db: Session):
    product_details = db.query(PurchaseOrderIssue).filter(PurchaseOrderIssue.id == id).first()

    if not product_details:
        return {'status': 'false', 'message': "Purchase Order Issue not found"}

    db.delete(product_details)
    db.commit()

    response = {
        'status': 'true',
        'message': "Purchase Order Issue Details deleted successfully"
    }
    
    return response