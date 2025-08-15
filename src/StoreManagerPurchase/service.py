from src.StoreManagerPurchase.models import StoreManagerPurchase,StoreManagerPurchaseCreate,RequestStatusUpdate,StoreManagerPurchaseUpdate
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status,HTTPException
from sqlalchemy import func,cast, Integer, and_, or_
from src.StoreManagerProduct.models import storeManagerProduct
from src.Category.models import Category
from src.Productwisestock.models import ProductWiseStock
from src.PurchaseManager.models import PurchaseManger

from src.StoreManagerProduct.models import storeManagerProduct
from src.Notifications.models import Notification
from src.AdminAddEmployee.models import AdminAddEmployee
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew


def get_all_store_manger_purcahse(db: Session):
    data = db.query(StoreManagerPurchase).order_by(StoreManagerPurchase.id.desc()).all()
    response = {'status': 'true', 'message': "Data Received Successfully", 'data': data}
    return response

# def create(db: Session, store_manger_purcahse: StoreManagerPurchaseCreate):
#     db_super_admin_reffral_plan = StoreManagerPurchase(**store_manger_purcahse.dict())
#     db.add(db_super_admin_reffral_plan)
#     db.commit()
#     db.refresh(db_super_admin_reffral_plan)
#     response = {'status': 'true','message':"Store Manager Purchase Details Added Successfully",'data':db_super_admin_reffral_plan}
#     return response

def create(db: Session, store_manger_purcahse_create: StoreManagerPurchaseCreate):

    if store_manger_purcahse_create.request_type == "Order" and store_manger_purcahse_create.product_manager_type == "Manual":
        pass
    else:
        existing_purchase = db.query(StoreManagerPurchase).filter(
            StoreManagerPurchase.admin_id == store_manger_purcahse_create.admin_id,
            StoreManagerPurchase.product_id == store_manger_purcahse_create.product_id,
            StoreManagerPurchase.request_status.notin_(["1", "3"])
        ).first()

        if existing_purchase:
            return {
                "status": "false",
                "message": f"Cannot create a new purchase for product {store_manger_purcahse_create.product_id} as an existing request is still active (not in allowed statuses 1 or 3)."
            }


    # Get the latest order_id for the given admin_id
    latest_request_id = (
        db.query(func.max(StoreManagerPurchase.request_id))
        .filter(StoreManagerPurchase.admin_id == store_manger_purcahse_create.admin_id)
        .scalar()
    )

    if store_manger_purcahse_create.employe_id:
        created_by_type = "employee"
        admin_emp_id = store_manger_purcahse_create.employe_id
    else:
        created_by_type = "admin"
        admin_emp_id = store_manger_purcahse_create.admin_id  


    # Extract the existing order number or set it to 0 if not present
    existing_request_id = int(latest_request_id.split('-')[1]) if (latest_request_id and '-' in latest_request_id) else 0

    # Increment the order_id
    new_request_number = existing_request_id + 1
    new_request_id = f"RI-{new_request_number:04d}"

    # Update the order_id in the input data
    store_manger_purcahse_create.request_id = new_request_id

    data = store_manger_purcahse_create.dict()
    data["created_by_type"]= created_by_type
    data["admin_emp_id"]= admin_emp_id

    # Create and add the new StoreManagerPurchase
    db_store_manger_purcahse_create = StoreManagerPurchase(**data)
    db.add(db_store_manger_purcahse_create)
    db.commit()
    db.refresh(db_store_manger_purcahse_create)

    empname = None
    if db_store_manger_purcahse_create.created_by_type == "employee":
        empname = db.query(AdminAddEmployee.employe_name).filter(AdminAddEmployee.id == db_store_manger_purcahse_create.admin_emp_id).first()
    else:
        empname = db.query(SuperAdminUserAddNew.full_name).filter(SuperAdminUserAddNew.id == db_store_manger_purcahse_create.admin_id).first()
    # Create notification for the admin
    notification = Notification(
        admin_id=db_store_manger_purcahse_create.admin_id,
        title="New Store Manager Purchase Created",
        description=f"A new Store Manager Purchase has been created by {empname}.",
        type="StoreManagerPurchase",
        object_id=str(db_store_manger_purcahse_create.id),
        created_by_id=db_store_manger_purcahse_create.admin_emp_id,
        created_by_type=db_store_manger_purcahse_create.created_by_type
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)

    response = {'status': 'true', 'message': "Store Manager Purchase Details Added Successfully", 'data': db_store_manger_purcahse_create}
    return response

def create_multiple(db: Session, store_manger_purcahse_create_list: list[StoreManagerPurchaseCreate]):
    create = []
    skip = []


    for purchase_data in store_manger_purcahse_create_list:
        existing_purchase = db.query(StoreManagerPurchase).filter(
            StoreManagerPurchase.admin_id == purchase_data.admin_id,
            StoreManagerPurchase.product_id == purchase_data.product_id,
            StoreManagerPurchase.request_status.notin_(["1", "3"])
        ).first()

        if existing_purchase:
            skip.append(purchase_data.product_id)
            continue

        latest_request_id = (
            db.query(func.max(StoreManagerPurchase.request_id))
            .filter(StoreManagerPurchase.admin_id == purchase_data.admin_id)
            .scalar()
        )

        if purchase_data.employe_id:
            created_by_type = "employee"
            admin_emp_id = purchase_data.employe_id
        else:
            created_by_type = "admin"
            admin_emp_id = purchase_data.admin_id

        existing_request_id = int(latest_request_id.split('-')[1]) if (latest_request_id and '-' in latest_request_id) else 0
        new_request_number = existing_request_id + 1
        new_request_id = f"RI-{new_request_number:04d}"
        purchase_data.request_id = new_request_id

        data = purchase_data.dict()
        data["created_by_type"] = created_by_type
        data["admin_emp_id"] = admin_emp_id

        db_store_purchase = StoreManagerPurchase(**data)
        db.add(db_store_purchase)
        db.commit()
        db.refresh(db_store_purchase)
        
        empname = None
        if db_store_purchase.created_by_type == "employee":
            empname = db.query(AdminAddEmployee.employe_name).filter(AdminAddEmployee.id == db_store_purchase.admin_emp_id).first()
        else:
            empname = db.query(SuperAdminUserAddNew.full_name).filter(SuperAdminUserAddNew.id == db_store_purchase.admin_id).first()
        # Create notification for the admin
        notification = Notification(
            admin_id=db_store_purchase.admin_id,
            title="New Store Manager Purchase Created",
            description=f"A new Store Manager Purchase has been created by {empname}.",
            type="StoreManagerPurchase",
            object_id=str(db_store_purchase.id),
            created_by_id=db_store_purchase.admin_emp_id,
            created_by_type=db_store_purchase.created_by_type
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)

        create.append(purchase_data.product_id)

    return {
        'status': 'false' if len(create) == 0 else 'true',
        'message': (
            f"Cannot create new purchase for product {','.join(map(str, skip))} due to active request."
            if len(create) == 0 else
            "Store Manager Purchase Details Added Successfully"
        ),
        'message1': (
            f"Store Manager Purchase Details for product {','.join(map(str, create))} added Successfully. , "
            f"Cannot create new purchase for product {','.join(map(str, skip))} due to active request."
        )
    }


from src.AdminAddEmployee.models import AdminAddEmployee
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew
from src.cre_upd_name import get_creator_updator_info
from src.QuotationProductEmployee.models import QuotationProductEmployee


def get_store_manger_purcahse_by_admin_id(db: Session, admin_id: str, search: Optional[str] = None):
    array = []

    purchase_query = db.query(StoreManagerPurchase).filter(
        StoreManagerPurchase.admin_id == admin_id
    ).order_by(StoreManagerPurchase.id.desc())

    if search:
        purchase_query = purchase_query.join(storeManagerProduct, StoreManagerPurchase.product_id.contains(storeManagerProduct.id), isouter=True).filter(
            or_(
                StoreManagerPurchase.request_id.like(f"%{search}%"),
                storeManagerProduct.product_tital.like(f"%{search}%"),
                storeManagerProduct.item_code.like(f"%{search}%")
            )
        )

    purchase_list = purchase_query.all()

    for purchase in purchase_list:
        # Split the request_purchase_quantity string into a list of integers
        request_quantities = list(map(int, filter(None, purchase.request_purchase_quntity.split(','))))

        #request_quantities = list(map(int, purchase.request_purchase_quntity.split(',')))
        product_ids = [int(pid) for pid in purchase.product_id.split(',') if pid.strip()]

        #product_ids = [int(pid) for pid in purchase.product_id.split(',')]

        # Extract product IDs from request_status
        request_status = purchase.request_status
        excluded_product_ids = [int(pid) for pid in request_status.split(',') if pid.isdigit()]

        process_details = list(zip(request_quantities, product_ids))



        created_updated_data = get_creator_updator_info(
            admin_emp_id=purchase.admin_emp_id,
            created_by_type=purchase.created_by_type,
            updated_admin_emp_id=purchase.updated_admin_emp_id,
            updated_by_type=purchase.updated_by_type,
          db=db
        )


        for request_quantity, product_id in process_details:
            # Exclude product IDs based on request_status
            # if product_id in excluded_product_ids:
            #     continue


            product = db.query(storeManagerProduct).filter(storeManagerProduct.id == product_id).first()

            if not product:
                prod = db.query(QuotationProductEmployee).filter(QuotationProductEmployee.id == product_id).first()
                if prod is not None:
                    code = prod.product_code
                    product = db.query(storeManagerProduct).filter(storeManagerProduct.item_code == code).first()

                


            if product:
                product_stock_data = db.query(ProductWiseStock).filter(ProductWiseStock.product_id == product.id).first()

                opening_stock = int(product.opening_stock or 0)
                minimum_required_quantity = int(product.minimum_requuired_quantity_for_low_stock or 0)
                buffer_until_low_stock = opening_stock - minimum_required_quantity

                
                if opening_stock == 0 and minimum_required_quantity == 0:
                    status = "LOW STOCK"
                elif buffer_until_low_stock < minimum_required_quantity:
                    status = "LOW STOCK"
                else:
                    status = "AVAILABLE"

                category_id = product.categories
                category_details = None
                if category_id:
                    category_details = db.query(Category).filter(Category.id == category_id).first()

                product_detail = {
                    **product.__dict__,
                    'request_quantity': request_quantity,
                    'available_quantity': opening_stock,
                    'status': status,
                    'buffer_until_low_stock': buffer_until_low_stock,
                    'minimum_required_quantity_for_low_stock': minimum_required_quantity,
                    'category_details': category_details,
                    'request_status': request_status

                }

                array.append({
                    'purchase_details': purchase,**created_updated_data,
                    'product_details': product_detail

                })

    response = {
        'status': 'true', 
        'message': "Data Received Successfully", 
        'count': len(array),
        'data': array

        }
    return response
   

def update(store_purchase_id:int,store_manager_purchase:StoreManagerPurchaseUpdate,db:Session):
    store_manager_purchase_update = store_manager_purchase.dict(exclude_unset=True)
    db.query(StoreManagerPurchase).filter(StoreManagerPurchase.id == store_purchase_id).update(store_manager_purchase_update)
    db.commit()
    response = {'status': 'true','message':"Store Manager Purchase Details Updated Successfully",'data':store_manager_purchase_update}
    return response


# def delete_store_manger_purcahse_by_id(store_purchase_id: int, db: Session):
#     plan = db.query(StoreManagerPurchase).filter(StoreManagerPurchase.id == store_purchase_id).first()
#     if plan:
#         db.delete(plan)
#         db.commit()
#         return {'status':'true', 'message':"Store Manager Purchase Details deleted successfully", 'data':plan}
#     return {"status":'false',  'message':"Store Manager Purchase Details not found"}

def delete_store_manger_purcahse_by_id(store_purchase_id: int, db: Session):
    plan = db.query(StoreManagerPurchase).filter(StoreManagerPurchase.id == store_purchase_id).first()

    if not plan:
        return {
            "status": 'false',
            "message": "Store Manager Purchase Details not found"
        }

    if plan.request_status != "0":
        return {
            "status": 'false',
            "message": "Cannot delete. Purchase request is already processed."
        }

    db.delete(plan)
    db.commit()

    return {
        "status": 'true',
        "message": "Store Manager Purchase Details deleted successfully",
        "data": plan
    }


from src.parameter import get_current_datetime


def update_request_status(store_manager_purchase_id: int, request_data: RequestStatusUpdate, db: Session):
    Order_data = db.query(StoreManagerPurchase).filter(StoreManagerPurchase.id == store_manager_purchase_id).first()

    if not Order_data:
        return {"status": 'false', 'message': "Store Manager Purchase Details not found"}

    if request_data.employe_id:
        updated_by_type = "employee"
        updated_admin_emp_id = request_data.employe_id
    else:
        updated_by_type = "admin"
        updated_admin_emp_id = request_data.admin_id  


    Order_data.updated_admin_emp_id = updated_admin_emp_id
    Order_data.updated_by_type = updated_by_type
    Order_data.updated_at = get_current_datetime()


    # Assuming SmartGridCreate has an attribute on_off
    Order_data.request_status = request_data.request_status
    db.commit()

    return {
        'status': 'true',
        'message': "Store Manager Purchase Request Update Successfully"
    }