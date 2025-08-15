from typing import List, Optional
from sqlmodel import Session, select,desc
from datetime import datetime
from fastapi import status,HTTPException
from .models import DispatchVendorCreate,DispatchVendor,DispatchVendorRead,VendorUpdateRequest,VendorDeleteRequest
from sqlalchemy import or_

def create(db: Session, vendor: DispatchVendorCreate):
    existing_vendor = db.query(DispatchVendor).filter(
        DispatchVendor.admin_id == vendor.admin_id,
        DispatchVendor.another_contact_number == vendor.another_contact_number
        ).all()
    if existing_vendor:
        return {
            'status': 'false',
            'message': 'Vendor with this another_contact_number already exists for this admin.'
        }
    
    existing_contact_number = db.query(DispatchVendor).filter(
        DispatchVendor.admin_id == vendor.admin_id,
        DispatchVendor.contact_number == vendor.contact_number
        ).all()
    if existing_contact_number:
        return {
            'status': 'false',
            'message': 'Vendor with this contact number already exists for this admin.'
        }
    
    existing_email = db.query(DispatchVendor).filter(
        DispatchVendor.admin_id == vendor.admin_id,
        DispatchVendor.email == vendor.email
        ).all()
    if existing_email:
        return {
            'status': 'false',
            'message': 'Vendor with this email already exists for this admin.'
        }

    # existing_vendor = db.exec(
    #     select(DispatchVendor)
    #     .where(DispatchVendor.admin_id == vendor.admin_id)
    #     .where(
    #         (DispatchVendor.contact_number == vendor.contact_number)
    #         | (DispatchVendor.another_contact_number == vendor.another_contact_number)
    #         | (DispatchVendor.email == vendor.email)
    #     )
    # ).first()


    if vendor.employee_id:
        created_by_type = "employee"
        admin_emp_id = vendor.employee_id
    else:
        created_by_type = "admin"
        admin_emp_id = vendor.admin_id  

    data = vendor.dict()
    data["created_by_type"] = created_by_type
    data["admin_emp_id"] = admin_emp_id


    db_vendor = DispatchVendor(**data)
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    response = {
        'status': 'true',
        'message': "Vendor Details Added Successfully",
        'data': db_vendor
    }
    return response



from src.cre_upd_name import get_creator_updator_info
from src.parameter import get_current_datetime


def get_vendor_list_service(db: Session, admin_id: str, employee_id: Optional[str] = None):
    query = select(DispatchVendor).where(DispatchVendor.admin_id == admin_id)
    if employee_id:
        query = query.where(DispatchVendor.employee_id == employee_id)


    query = query.order_by(desc(DispatchVendor.id))

    vendors = db.execute(query).scalars().all()
    data = []
    for vendor in vendors:
        created_updated_data = get_creator_updator_info(
            admin_emp_id=vendor.admin_emp_id,
            created_by_type=vendor.created_by_type,
            updated_admin_emp_id=vendor.updated_admin_emp_id,
            updated_by_type=vendor.updated_by_type,
          db=db
        )
        ven = vars(vendor.copy())
        data.append({**ven,**created_updated_data})
        
    # vendors = db.exec(query).all()
    return data


def update_vendor_service(db: Session, request: VendorUpdateRequest):
    vendor = db.get(DispatchVendor, request.vendor_id)
    if not vendor:
        return {"status": "false", "message": "Vendor not found"}

    if request.employee_id:
        updated_by_type = "employee"
        updated_admin_emp_id = request.employee_id
    else:
        updated_by_type = "admin"
        updated_admin_emp_id = request.admin_id  

    data = request.dict(exclude_unset=True, exclude={"vendor_id"})
    data["updated_by_type"] = updated_by_type
    data["updated_admin_emp_id"] = updated_admin_emp_id
    data["updated_at"] = get_current_datetime


    for key, value in data.items():
        setattr(vendor, key, value)
    
    db.add(vendor)
    db.commit()
    db.refresh(vendor)
    
    return {"status": "true", "message": "Vendor updated successfully", "data": vendor}




def delete_vendor_service(db: Session, request: VendorDeleteRequest):
    vendor = db.get(DispatchVendor, request.vendor_id)
    if not vendor:
        return {"status": "false", "message": "Vendor not found"}
    
    if vendor.admin_id != request.admin_id:
        return {"status": "false", "message": "Unauthorized to delete this vendor"}
    
    if request.employee_id and vendor.employee_id != request.employee_id:
        return {"status": "false", "message": "Employee ID mismatch"}
    
    db.delete(vendor)
    db.commit()
    
    return {"status": "true", "message": "Vendor deleted successfully"}

