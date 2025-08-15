from .models import DeliveryChallan,DeliveryChallanBase,UpdateChallanRequest,updatestatus,GetDispatch
from sqlmodel import Session, select
from sqlalchemy import cast
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy.types import String
from sqlalchemy import desc
from typing import List, Optional, Dict
from src.QuotationProductEmployee.models import QuotationProductEmployee
from src.DispatchVendor.models import DispatchVendor
from datetime import datetime
import os
import base64
from sqlalchemy.sql.expression import func
from src.Inventoryoutward.models import InventoryOutward
import re
from src.ProjectManagerOrder.models import ProjectManagerOrder

from datetime import datetime

def get_current_datetime():
    return datetime.now()



    
def create(db: Session, delivery_create: DeliveryChallanBase):
    # Check for required fields
    missing_fields = []
    if not delivery_create.admin_id:
        missing_fields.append("admin_id")
    # if not delivery_create.product_id:
    #     missing_fields.append("product_id")
    if not delivery_create.vendor_id:
        missing_fields.append("vendor_id")
    # if not delivery_create.inventryoutword_id:
    #     missing_fields.append("inventryoutword_id")  # Ensure this exists

    if missing_fields:
        return {
            'status': 'false',
            'message': f"The {', '.join(missing_fields)} field is required."
        }

    if delivery_create.employee_id:
        created_by_type = "employee"
        admin_emp_id = delivery_create.employee_id
    else:
        created_by_type = "admin"
        admin_emp_id = delivery_create.admin_id  


    try:
        data = delivery_create.dict()
        data["created_by_type"] = created_by_type
        data["admin_emp_id"] = admin_emp_id

        db_delivery = DeliveryChallan(**data)
        db.add(db_delivery)
        db.commit()
        db.refresh(db_delivery)

        if delivery_create.inventryoutword_id:
            # Update InventoryOutward.challan_status = 1
            invent = db.query(InventoryOutward).filter(
                InventoryOutward.id == delivery_create.inventryoutword_id
            ).first()

            if invent:
                invent.challan_status = 1
                invent.updated_at = get_current_datetime()  # optional: force update timestamp
                db.commit()
            #else:
            #    return {
             #       'status': 'false',
              #      'message': "InventoryOutward entry not found"
             #   }
        if delivery_create.order_id:
            # Update ProjectManagerOrder.challan_status = 1
            order = db.query(ProjectManagerOrder).filter(
                ProjectManagerOrder.id == delivery_create.order_id
            ).first()

            if order:
                order.challan_status = 1
                # order.updated_at = get_current_datetime()  # optional: force update timestamp
                db.commit()
            #else:
             #   return {
              #      'status': 'false',
               #     'message': "ProjectManagerOrder entry not found"
               # }

        return {
            'status': 'true',
            'message': "Delivery Challan Added Successfully",
            'data': db_delivery
        }



    except Exception as e:
        db.rollback()
        return {
            'status': 'false',
            'message': f"Failed to create delivery challan: {str(e)}"
        }

    
    
    


def fetch_delivery_challans(
    db: Session, admin_id: int, employee_id: Optional[str] = None, date: Optional[str] = None
):
    query = db.query(DeliveryChallan).filter(DeliveryChallan.admin_id == admin_id)
    
    if employee_id:
        query = query.filter(DeliveryChallan.employee_id == employee_id)
    
    if date:
        try:
            date_obj = datetime.strptime(date, "%d/%m/%Y").date()
            query = query.filter(func.date(DeliveryChallan.created_at) == date_obj)
        except ValueError:
            return {"status": "false", "message": "Invalid date format. Use DD/MM/YYYY."}

    challans = query.all()
    
    results = []
    for challan in challans:
        product = db.query(QuotationProductEmployee).filter_by(id=challan.product_id).first()
        vendor = db.query(DispatchVendor).filter_by(id=challan.vendor_id).first()
        
        results.append({
            **challan.__dict__,
            "product_detail": product.__dict__ if product else None,
            "vendor_detail": vendor.__dict__ if vendor else None
        })
    
    return results



def save_base64_file(base64_str: str, filename: str) -> str:
    import base64
    import os

    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    
    # ? Strip Data URI prefix if present
    match = re.match(r'data:.*?;base64,(.*)', base64_str)
    if match:
        base64_str = match.group(1)

    try:
        file_data = base64.b64decode(base64_str)
    except Exception as e:
        raise ValueError(f"Invalid base64 data: {e}")

    file_path = os.path.join("uploads", filename)
    with open(file_path, "wb") as file:
        file.write(file_data)

    return file_path

from src.parameter import get_current_datetime


def update_challan_service(
    db: Session, request: UpdateChallanRequest, request_obj: Request
) -> Dict:
    challan = db.query(DeliveryChallan).filter(
        DeliveryChallan.id == request.delivery_challan_id,
        DeliveryChallan.admin_id == request.admin_id
    ).first()

    if not challan:
        return {
            "status": "false",
            "message": "Delivery challan not found",
        }

    # ? Update values only if they are provided in the request
    if request.employee_id is not None:
        challan.employee_id = request.employee_id
    if request.vehicle_number is not None:
        challan.vehicle_number = request.vehicle_number
    if request.mobile_number is not None:
        challan.mobile_number = request.mobile_number
    if request.address is not None:
        challan.address = request.address
    if request.kindely_atention is not None:
        challan.kindely_atention = request.kindely_atention
    if request.company_name is not None:
        challan.company_name = request.company_name
    if request.comment_mark is not None:
        challan.comment_mark = request.comment_mark
        challan.status = "Complete"  # Auto-mark as complete if comment is added

    if request.employee_id:
        updated_by_type = "employee"
        updated_admin_emp_id = request.employee_id
    else:
        updated_by_type = "admin"
        updated_admin_emp_id = request.admin_id  


    # ? Update file if provided
    if request.file_path and request.file_ext:
        current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{current_datetime}_challan_{request.delivery_challan_id}.{request.file_ext}"
        save_base64_file(request.file_path, filename)
        challan.file_path = f"/uploads/{filename}"
        challan.file_ext = request.file_ext
    else:
        challan.file_path = ""
        challan.file_ext = ""

    challan.updated_at = get_current_datetime()
    challan.updated_admin_emp_id = updated_admin_emp_id
    challan.updated_by_type = updated_by_type



    db.add(challan)
    db.commit()
    db.refresh(challan)

    return {
        "status": "true",
        "message": "Delivery challan updated successfully",
        "data": challan.__dict__,
    }

    

from src.QuotationProductEmployee.models import QuotationProductEmployee
from src.Inventoryoutward.models import InventoryOutward

def product_status(db: Session, request: updatestatus):
    basequery = db.query(InventoryOutward).filter(
        InventoryOutward.id == request.inventryoutword_id,
        InventoryOutward.admin_id == request.admin_id,
        InventoryOutward.product_id == request.product_id,
    )

    # Add optional filter for employee_id if provided
    if request.employee_id:
        basequery = basequery.filter(
            InventoryOutward.emplpoyee_id == request.employee_id
        )

    # Execute the query
    inventry = basequery.first()

    if not inventry:
        return {
            "status": "false",
            "message": "Inventory Outward not found"
        }

    prod = db.query(QuotationProductEmployee).filter(
        QuotationProductEmployee.id == request.product_id,
        QuotationProductEmployee.admin_id == request.admin_id
    ).first()

    if not prod:
        return {
            "status": "false",
            "message": "Product not found"
        }

    try:
        # Update product status
        prod.status = request.status
        db.commit()
        db.refresh(prod)

        return {
            "status": "true",
            "message": "Delivery challan updated successfully"
        }

    except Exception as e:
        db.rollback()
        return {
            "status": "false",
            "message": f"Failed to update status: {str(e)}"
        }
        
        
from src.AdminAddEmployee.models import AdminAddEmployee
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew    
from sqlalchemy.orm import joinedload

def get_dispatch_complited(db: Session, request: GetDispatch):
    # Start by joining InventoryOutward with QuotationProductEmployee
    basequery = db.query(InventoryOutward).join(
        QuotationProductEmployee,
        InventoryOutward.product_id == QuotationProductEmployee.id
    ).filter(
        InventoryOutward.admin_id == request.admin_id,
        InventoryOutward.status == "Approved",
        QuotationProductEmployee.status == "Complete"  # Filter for products with status 'Complete'
    )

    # Apply additional filters if provided
    if request.product_id:
        basequery = basequery.filter(InventoryOutward.product_id == request.product_id)

    if request.employee_id:
        basequery = basequery.filter(InventoryOutward.emplpoyee_id == request.employee_id)

    # Execute the query and order the results
    inventory_list = basequery.order_by(InventoryOutward.created_at.desc()).all()

    if not inventory_list:
        return {"status": "false", "message": "No records found"}

    response_data = []
    for inventory in inventory_list:
        # Fetch product details
        product_details = db.query(QuotationProductEmployee).filter(
            QuotationProductEmployee.id == inventory.product_id
        ).first()

        # Creator details
        creator_info = {
            "name": "",
            "id": None,
            "employee_id": ""
        }
        if inventory.admin_emp_id:
            if inventory.created_by_type == 'employee':
                empd = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == int(inventory.admin_emp_id)).first()
                if empd:
                    creator_info = {
                        "name": empd.employe_name,
                        "id": empd.id,
                        "employee_id": empd.employee_id
                    }
            elif inventory.created_by_type == 'admin':
                empd = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == int(inventory.admin_emp_id)).first()
                if empd:
                    creator_info = {
                        "name": empd.full_name,
                        "id": empd.id,
                        "employee_id": "Admin"
                    }

        # Approver details
        approver_info = {
            "name": "",
            "id": None,
            "employee_id": ""
        }
        if inventory.approve_by_id:
            if inventory.approve_by_type == 'employee':
                empd = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == int(inventory.approve_by_id)).first()
                if empd:
                    approver_info = {
                        "name": empd.employe_name,
                        "id": empd.id,
                        "employee_id": empd.employee_id
                    }
            elif inventory.approve_by_type == 'admin':
                empd = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == int(inventory.approve_by_id)).first()
                if empd:
                    approver_info = {
                        "name": empd.full_name,
                        "id": empd.id,
                        "employee_id": "Admin"
                    }

        inventory_dict = inventory.__dict__

        response_data.append({
            "inventory": inventory_dict,
            "Created_by": creator_info,
            "approved_by": approver_info,
            "product_details": product_details or {}
        })

    return {"status": "true", "message": "Data Retrieved Successfully", "data": response_data}


        
        

        
        
        
        
        