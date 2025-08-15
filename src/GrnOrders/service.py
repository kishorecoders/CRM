from .models import GrnOrderIssueCreate , GrnOrderIssue ,GrnOrderIssueUpdate ,GrnOrderProductGet , GrnOrderProductDelete
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from src.GrnOrderProduct.models import GrnOrderProduct
from src.GrnInvoice.models import GrnInvoice
from sqlalchemy import desc
from sqlalchemy import asc 

from src.PurchaseOrderIssue.models import PurchaseOrderIssue
from src.PurchaseOrderProduct.models import PurchaseOrderProduct
from src.vendor.models import Vendor
from src.cre_upd_name import get_creator_updator_info
from sqlalchemy import func, cast, Integer

from src.StoreManagerProduct.models import storeManagerProduct
from src.Notifications.models import Notification
from src.AdminAddEmployee.models import AdminAddEmployee
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew

    
def create_order_with_products(db: Session, request: GrnOrderIssueCreate):
    if request.employee_id:
        created_by_type = "employee"
        admin_emp_id = request.employee_id
    else:
        created_by_type = "admin"
        admin_emp_id = request.admin_id  

    data = request.dict(exclude={"products"})
    data["created_by_type"] = created_by_type
    data["admin_emp_id"] = admin_emp_id

    new_order = GrnOrderIssue(**data)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    empname = None
    if new_order.created_by_type == "employee":
        empname = db.query(AdminAddEmployee.employe_name).filter(AdminAddEmployee.id == new_order.admin_emp_id).first()
    else:
        empname = db.query(SuperAdminUserAddNew.full_name).filter(SuperAdminUserAddNew.id == new_order.admin_id).first()
    # Create notification for the admin
    notification = Notification(
        admin_id=new_order.admin_id,
        title="New GRN Order Created",
        description=f"A new GRN Order has been created by {empname}.",
        type="GRNOrder",
        object_id=str(new_order.id),
        created_by_id=new_order.admin_emp_id,
        created_by_type=new_order.created_by_type,
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)

    for product in request.products:
        product_dict = product.dict()
        product_dict["created_by_type"] = created_by_type
        product_dict["admin_emp_id"] = admin_emp_id
        product_dict["admin_id"] = request.admin_id
        product_dict["grn_order_id"] = new_order.id
        product_dict["employee_id"] = request.employee_id

        # Add GRN Product Entry
        db_product = GrnOrderProduct(**product_dict)
        db.add(db_product)
        db.commit()

        # ? Update `prev_accept` and `prev_received` in PurchaseOrderProduct
        prev_data = (
            db.query(
                func.coalesce(func.sum(cast(GrnOrderProduct.accepted_quantity, Integer)), 0).label("total_accept"),
                func.coalesce(func.sum(cast(GrnOrderProduct.recived_quantity, Integer)), 0).label("total_received")
            )
            .join(GrnOrderIssue, GrnOrderProduct.grn_order_id == GrnOrderIssue.id)
            .filter(
                GrnOrderIssue.purchase_order_id == request.purchase_order_id,
                GrnOrderProduct.product_id == product.product_id
            )
            .first()
        )

        # Find and update the PurchaseOrderProduct
        pop = db.query(PurchaseOrderProduct).filter(
            PurchaseOrderProduct.id == int(product.product_id)
        ).first()

        if pop:
            pop.prev_accept = str(prev_data.total_accept)
            pop.prev_received = str(prev_data.total_received)
            db.add(pop)
            db.commit()

            code = pop.product_code 

            store = db.query(storeManagerProduct).filter(
                storeManagerProduct.item_code == code
            ).first()
            if store:
                store.opening_stock = str(int(product.accepted_quantity) + int(store.opening_stock)) if product.accepted_quantity else store.opening_stock
                db.add(store)
                db.commit()

    return {
        "status": "true",
        "message": "Grn Order with Products created successfully",
    }    
    
    
    


def update_old(db: Session, request: GrnOrderIssueUpdate):

    # Fetch existing order
    existing_order = db.query(GrnOrderIssue).filter(
        GrnOrderIssue.id == int(request.grn_order_issue_id)
        ).first()
    
    if not existing_order:
        return {
            "status": "false",
            "message": "Grn Order not found",
        }

    if request.employee_id:
        updated_by_type = "employee"
        updated_admin_emp_id = request.employee_id
    else:
        updated_by_type = "admin"
        updated_admin_emp_id = request.admin_id  
    
    # Update order fields (correctly exclude products)
    update_data = request.dict(exclude={"products","grn_order_issue_id"}, exclude_unset=True)
    update_data["updated_by_type"] = updated_by_type
    update_data["updated_admin_emp_id"] = updated_admin_emp_id

    for key, value in update_data.items():
        setattr(existing_order, key, value)

    db.commit()
    db.refresh(existing_order)

    db.query(GrnOrderProduct).filter(GrnOrderProduct.grn_order_id == existing_order.id).delete()
    db.commit()

    for product in request.products:
        product_dict = product.dict()
        product_dict["updated_admin_emp_id"] = existing_order.updated_admin_emp_id
        product_dict["updated_by_type"] = existing_order.updated_by_type
        product_dict["admin_id"] = request.admin_id
        product_dict["employee_id"] = request.employee_id
        product_dict["grn_order_id"] = existing_order.id
        db_product = GrnOrderProduct(**product_dict)
        db.add(db_product)

    db.commit()

    return {
        "status": "true",
        "message": "Order and products updated successfully",
    }
    
    
    
    
    
    
    
def update(db: Session, request: GrnOrderIssueUpdate):
    # Fetch existing order
    existing_order = db.query(GrnOrderIssue).filter(
        GrnOrderIssue.id == int(request.grn_order_issue_id)
    ).first()
    
    if not existing_order:
        return {
            "status": "false",
            "message": "Grn Order not found",
        }

    # Determine who is updating
    if request.employee_id:
        updated_by_type = "employee"
        updated_admin_emp_id = request.employee_id
    else:
        updated_by_type = "admin"
        updated_admin_emp_id = request.admin_id  

    # Update main GRN order fields
    update_data = request.dict(exclude={"products", "grn_order_issue_id"}, exclude_unset=True)
    update_data["updated_by_type"] = updated_by_type
    update_data["updated_admin_emp_id"] = updated_admin_emp_id

    for key, value in update_data.items():
        setattr(existing_order, key, value)

    db.commit()
    db.refresh(existing_order)

    # Delete old GRN products
    db.query(GrnOrderProduct).filter(GrnOrderProduct.grn_order_id == existing_order.id).delete()
    db.commit()

    # Add new GRN products
    for product in request.products:
        product_dict = product.dict()
        product_dict["updated_admin_emp_id"] = updated_admin_emp_id
        product_dict["updated_by_type"] = updated_by_type
        product_dict["admin_id"] = request.admin_id
        product_dict["employee_id"] = request.employee_id
        product_dict["grn_order_id"] = existing_order.id

        db_product = GrnOrderProduct(**product_dict)
        db.add(db_product)

    db.commit()

    # ? Update prev_accept and prev_received in PurchaseOrderProduct
    product_ids = [product.product_id for product in request.products if product.product_id]

    for product_id in product_ids:

        pop = db.query(PurchaseOrderProduct).filter(
            PurchaseOrderProduct.id == int(product_id)
        ).first()
     


        if  pop and  int(pop.quantity) > int(product.accepted_quantity) and int(pop.quantity) - int(pop.prev_accept) >=int(product.accepted_quantity):
            
            pop.prev_accept = str(int(pop.prev_accept) + int(product.accepted_quantity))
            pop.prev_received = str(int(pop.prev_received)  + int(product.recived_quantity))
            db_product.accepted_quantity = pop.prev_accept
            db_product.recived_quantity =pop.prev_received


            db.add(pop)


    db.commit()

    return {
        "status": "true",
        "message": "Order and products updated successfully",
    }

    

def get_all_grn_order_issue(db: Session):
    data = db.query(GrnOrderIssue).order_by(GrnOrderIssue.id.desc()).all()
    response = {'status': 'true', 'message': "Data Received Successfully", 'data': data}
    return response



def get_grn_order_issue_by_admin_old(db: Session, request: GrnOrderProductGet):
    array = []

    query = db.query(GrnOrderIssue).filter(GrnOrderIssue.admin_id == request.admin_id)

    if request.employee_id:
        query = query.filter(GrnOrderIssue.employee_id == request.employee_id)

    #if request.grn_status:
    #    query = query.filter(GrnOrderIssue.grn_status == request.grn_status) 
    if request.grn_status == "Invoiced":
        query = query.filter(GrnOrderIssue.grn_status == "Invoiced")
    elif request.grn_status == "":
        query = query.filter(GrnOrderIssue.grn_status != "Invoiced") 
        
        
    query1 = query.order_by(GrnOrderIssue.id.desc())    

    GrnOrderList = query1.all()

    for GrnOrder in GrnOrderList:
        # Enrich productDetails with product_name and discription
        rawProducts = db.query(GrnOrderProduct).filter(
            GrnOrderProduct.grn_order_id == GrnOrder.id
        ).all()

        productDetails = []
        for prod in rawProducts:
            purchase_product = db.query(PurchaseOrderProduct).filter(
                PurchaseOrderProduct.id == int(prod.product_id)
            ).first()

            prod_dict = prod.__dict__.copy()
            prod_dict["product_name"] = purchase_product.product_name if purchase_product else ""
            prod_dict["discription"] = purchase_product.discription if purchase_product else ""
            prod_dict.pop("_sa_instance_state", None)

            productDetails.append(prod_dict)
            
        created_updated_data = {}
        grn_invoice = db.query(GrnInvoice).filter(
            GrnInvoice.grn_id == str(GrnOrder.id)
        ).first()
        if grn_invoice:
            created_updated_data = get_creator_updator_info(
                admin_emp_id=grn_invoice.admin_emp_id,
                created_by_type=grn_invoice.created_by_type,
                updated_admin_emp_id=grn_invoice.updated_admin_emp_id,
                updated_by_type=grn_invoice.updated_by_type,
                db=db
            )
        grn_invoice_data = grn_invoice.dict() if grn_invoice else {}

        purchase_order_data = db.query(PurchaseOrderIssue).filter(
            PurchaseOrderIssue.id == int(GrnOrder.purchase_order_id)
        ).first()

        vendor_data = db.query(Vendor).filter(
            Vendor.id == int(GrnOrder.vendor_id)
        ).first()

        temp = {
            "Grn_order_details": GrnOrder,
            "Product_details": productDetails,
            "grn_invoice": {**grn_invoice_data, **created_updated_data},
            "purchase_order": purchase_order_data,
            "vendor_details": vendor_data
        }
        array.append(temp)

    return {
        'status': 'true',
        'message': "Data Received Successfully",
        'data': array
    }
  
  
  
  

def safe_float(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0


def get_grn_order_issue_by_admin(db: Session, request):
    array = []

    query = db.query(GrnOrderIssue).filter(GrnOrderIssue.admin_id == request.admin_id)

    if request.employee_id:
        query = query.filter(GrnOrderIssue.employee_id == request.employee_id)

    if request.grn_status == "Invoiced":
        query = query.filter(GrnOrderIssue.grn_status == "Invoiced")
    elif request.grn_status == "":
        query = query.filter(GrnOrderIssue.grn_status != "Invoiced")

    GrnOrderList = query.order_by(GrnOrderIssue.id.desc()).all()

    for GrnOrder in GrnOrderList:
        rawProducts = db.query(GrnOrderProduct).filter(
            GrnOrderProduct.grn_order_id == GrnOrder.id
        ).all()

        productDetails = []

        for prod in rawProducts:
            purchase_product = db.query(PurchaseOrderProduct).filter(
                PurchaseOrderProduct.id == int(prod.product_id)
            ).first()

            # Get previous accepted & received quantities from other GRNs of same purchase order
            previous_data = (
                db.query(
                    func.coalesce(func.sum(cast(GrnOrderProduct.accepted_quantity, Integer)), 0).label("prev_accept"),
                    func.coalesce(func.sum(cast(GrnOrderProduct.recived_quantity, Integer)), 0).label("prev_received")
                )
                .join(GrnOrderIssue, GrnOrderProduct.grn_order_id == GrnOrderIssue.id)
                .filter(
                    GrnOrderIssue.purchase_order_id == GrnOrder.purchase_order_id,
                    GrnOrderProduct.product_id == prod.product_id,
                    GrnOrderProduct.grn_order_id != GrnOrder.id
                )
                .first()
            )

            prev_accept = previous_data.prev_accept
            prev_received = previous_data.prev_received

            prod_dict = prod.__dict__.copy()
            prod_dict["product_name"] = purchase_product.product_name if purchase_product else ""
            prod_dict["discription"] = purchase_product.discription if purchase_product else ""
            prod_dict["prev_accept"] = str(prev_accept)
            prod_dict["prev_received"] = str(prev_received)
            prod_dict.pop("_sa_instance_state", None)

            productDetails.append(prod_dict)

        created_updated_data = {}
        grn_invoice = db.query(GrnInvoice).filter(
            GrnInvoice.grn_id == str(GrnOrder.id)
        ).first()

        if grn_invoice:
            created_updated_data = get_creator_updator_info(
                admin_emp_id=grn_invoice.admin_emp_id,
                created_by_type=grn_invoice.created_by_type,
                updated_admin_emp_id=grn_invoice.updated_admin_emp_id,
                updated_by_type=grn_invoice.updated_by_type,
                db=db
            )

        grn_invoice_data = grn_invoice.dict() if grn_invoice else {}

        purchase_order_data = db.query(PurchaseOrderIssue).filter(
            PurchaseOrderIssue.id == int(GrnOrder.purchase_order_id)
        ).first()

        vendor_data = db.query(Vendor).filter(
            Vendor.id == int(GrnOrder.vendor_id)
        ).first()

        array.append({
            "Grn_order_details": GrnOrder,
            "Product_details": productDetails,
            "grn_invoice": {**grn_invoice_data, **created_updated_data},
            "purchase_order": purchase_order_data,
            "vendor_details": vendor_data
        })

    return {
        "status": "true",
        "message": "Data Received Successfully",
        "data": array
    }
    
    

def delete_grn_order_issue_by_admin(db: Session, request: GrnOrderProductDelete):
    if not request.admin_id or not request.grn_id:
        return {"status": "false", "message": "admin_id and grn_id are required"}

    query = db.query(GrnOrderIssue).filter(
        GrnOrderIssue.admin_id == request.admin_id,
        GrnOrderIssue.id == int(request.grn_id)
    )
    if request.employee_id:
        query = query.filter(GrnOrderIssue.employee_id == request.employee_id)

    GrnOrder = query.first()

    if not GrnOrder:
        return {"status": "false", "message": "Task not found to delete"}

    # Delete associated products first
    db.query(GrnOrderProduct).filter(GrnOrderProduct.grn_order_id == GrnOrder.id).delete()
    db.delete(GrnOrder)
    db.commit()

    return {"status": "true", "message": "Grn Order and associated products deleted successfully"}




