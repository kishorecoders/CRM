from .models import Vendor,VendorCreate , VendorDelete
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status,HTTPException
from src.PurchaseOrderIssue.models import PurchaseOrderIssue
from src.PurchaseManager.models import PurchaseManger
from src.StoreManagerProduct.models import storeManagerProduct
from src.AdminAddEmployee.models import AdminAddEmployee
from src.Notifications.models import Notification
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew


def get_all_vendor(db: Session):
    data = db.query(Vendor).order_by(Vendor.id.desc()).all()
    response = {'status': 'true', 'message': "Data Received Successfully", 'data': data}
    return response


def create(db: Session, vendor: VendorCreate):
    if vendor.employe_id:
        created_by_type = "employee"
        admin_emp_id = vendor.employe_id
    else:
        created_by_type = "admin"
        admin_emp_id = vendor.admin_id

    # Prepare vendor dict with additional fields
    vendor_data = vendor.dict()
    vendor_data['created_by_type'] = created_by_type
    vendor_data['admin_emp_id'] = admin_emp_id

    db_vendor = Vendor(**vendor_data)
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)

    empname = None
    if db_vendor.created_by_type == 'employee':
        empname = db.query(AdminAddEmployee.employe_name).filter(AdminAddEmployee.id == db_vendor.admin_emp_id).first()
    else:
        empname = db.query(SuperAdminUserAddNew.full_name).filter(SuperAdminUserAddNew.id == db_vendor.admin_emp_id).first()
    # Create notification for the admin
    notification = Notification(
        admin_id=db_vendor.admin_emp_id,
        title="New Vendor Created",
        description=f"A new Vendor has been created by {empname}.",
        type="Vendor",
        object_id=str(db_vendor.id),
        created_by_id=db_vendor.admin_emp_id,
        created_by_type=db_vendor.created_by_type
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)

    response = {
        'status': 'true',
        'message': "Vendor Details Added Successfully",
        'data': db_vendor
    }
    return response


# def create(db: Session, vendor: VendorCreate):
#     db_vendor = Vendor(**vendor.dict())
#     db.add(db_vendor)
#     db.commit()
#     db.refresh(db_vendor)
#     response = {'status': 'true','message':"Vendor Details Added Successfully",'data':db_vendor}
#     return response


# def get_vendor_by_admin_id(admin_id: int, db: Session):
#     data = db.query(Vendor).filter(Vendor.admin_id == admin_id).order_by(Vendor.id.desc()).all()
#     response = {'status': 'true','message':"Data Recived Successfully",'data':data}
#     return response


from src.AdminAddEmployee.models import AdminAddEmployee
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew


def get_vendor_by_admin_id(admin_id: int, db: Session):
    data = db.query(Vendor).filter(Vendor.admin_id == admin_id).order_by(Vendor.id.desc()).all()

    response_data = []

    for vendor in data:
        grand_total = 0.0  # Initialize grand_total for each vendor

        purchase_order_issue_data = db.query(PurchaseOrderIssue).filter(PurchaseOrderIssue.vendor_id == str(vendor.id)).all()

        for issue_data in purchase_order_issue_data:
            # Fetch the corresponding data from PurchaseManager
            purchase_manager_data = db.query(PurchaseManger).filter(
                PurchaseManger.request_id == issue_data.purchase_request_id,
                PurchaseManger.product_id == issue_data.product_id
            ).first()

            if purchase_manager_data:
                # Access the product_id from the PurchaseManager data
                product_id = purchase_manager_data.product_id

                # Fetch data from StoreManagerProduct using the product_id
                store_manager_product_data = db.query(storeManagerProduct).filter(
                    storeManagerProduct.id == product_id
                ).first()

                if store_manager_product_data:
                    # Converting character_varying values to appropriate numeric types
                    price_per_product = float(store_manager_product_data.price_per_product)
                    gst_rate = float(store_manager_product_data.gst_rate.replace('%', '')) / 100

                    # Calculating total_amount by adding price_per_product and gst_rate
                    total_amount = price_per_product + (price_per_product * gst_rate)

                    # Adding total_amount to the grand total
                    grand_total += total_amount

        # Create a dictionary representation of the vendor without modifying the model
        vendor_data = {k: v for k, v in vendor.__dict__.items() if not k.startswith('')}

        # Creator details
        creator_info = {
            "name": "",
            "admin_emp_name":"",
            "id": None,
            "employee_id": ""
        }
        if vendor.admin_emp_id:
            if vendor.created_by_type == 'employee':
                empd = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == int(vendor.admin_emp_id)).first()
                if empd:
                    creator_info = {
                        "name": empd.employe_name,
                        "admin_emp_name":f"{empd.employe_name}({empd.employee_id})",
                        "id": empd.id,
                        "employee_id": empd.employee_id
                    }
            elif vendor.created_by_type == 'admin':
                empd = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == int(vendor.admin_emp_id)).first()
                if empd:
                    creator_info = {
                        "name": empd.full_name,
                        "admin_emp_name":f"{empd.full_name}(Admin)",
                        "id": empd.id,
                        "employee_id": "Admin"
                    }

        # Approver details
        updater_info = {
            "name": "",
            "admin_emp_name":"",
            "id": None,
            "employee_id": ""
        }
        if vendor.updated_admin_emp_id:
            if vendor.updated_by_type == 'employee':
                empd = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == int(vendor.updated_admin_emp_id)).first()
                if empd:
                    updater_info = {
                        "name": empd.employe_name,
                        "admin_emp_name":f"{empd.employe_name}({empd.employee_id})",
                        "id": empd.id,
                        "employee_id": empd.employee_id
                    }
            elif vendor.updated_by_type == 'admin':
                empd = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == int(vendor.updated_admin_emp_id)).first()
                if empd:
                    updater_info = {
                        "name": empd.full_name,
                        "admin_emp_name":f"{empd.full_name}(Admin)",
                        "id": empd.id,
                        "employee_id": "Admin"
                    }


        # Add the grand_total to the vendor_data dictionary
        vendor_data['creator_info'] = creator_info
        vendor_data['updater_info'] = updater_info
        vendor_data['grand_total'] = grand_total

        # Append the vendor_data to the response_data list
        response_data.append({'vendor':vendor, 'grand_total':grand_total,'updater_info':updater_info,'creator_info':creator_info})

    response = {'status': 'true', 'message': "Data Received Successfully", 'data': response_data}
    return response
   
   

def update(vendor_id: int, vendor: Vendor, db: Session):
    # Extract data safely depending on who updated
    if vendor.employe_id:
        updated_by_type = "employee"
        updated_admin_emp_id = vendor.employe_id
    else:
        updated_by_type = "admin"
        updated_admin_emp_id = vendor.admin_id

    # Assuming 'vendor' is a Pydantic model; if not, adjust accordingly
    vendor_update = vendor.dict(exclude_unset=True)
    
    # Add updater info to update dict
    vendor_update["updated_by_type"] = updated_by_type  # Or name it clearly like updated_by_id
    vendor_update["updated_admin_emp_id"] = updated_admin_emp_id

    # Perform the update
    db.query(Vendor).filter(Vendor.id == vendor_id).update(vendor_update)
    db.commit()

    response = {
        'status': 'true',
        'message': "Vendor Details Updated Successfully",
        'data': vendor_update
    }
    return response
   

# def update(vendor_id:int,vendor:Vendor,db:Session):
#     vendor_update = vendor.dict(exclude_unset=True)
#     db.query(Vendor).filter(Vendor.id == vendor_id).update(vendor_update)
#     db.commit()
#     response = {'status': 'true','message':"Vendor Details Updated Successfully",'data':vendor_update}
#     return response



# def delete_vendor_id(vendor_id: int, db: Session):
#     vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
#     if vendor:
#         db.delete(vendor)
#         db.commit()
#         return {'status':'true', 'message':"Vendor deleted successfully", 'data':vendor}
#     return {"status":'false',  'message':"Vendor not found"}

def delete_vendor_id(request: VendorDelete, db: Session):
    vendor = db.query(Vendor).filter(Vendor.id == request.id).first()

    if not vendor:
        return {'status': 'false', 'message': "Vendor not found"}

    db.delete(vendor)
    db.commit()

    return {'status': 'true', 'message': "Vendor deleted successfully"}
    
    
    