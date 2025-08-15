from src.StoreManagerService.models import storeManagerService,storeManagerServiceCreate
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status,HTTPException
from src.Category.models import Category
import string
import random
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew
from src.SubCategory.models import SubCategory

def get_all_service(db: Session):
    data = db.query(storeManagerService).order_by(storeManagerService.id.desc()).all()
    response = {'status': 'true', 'message': "Data Received Successfully", 'data': data}
    return response

# def get_service_by_admin(admin_id: str, db: Session):
#     data = db.query(storeManagerService).filter(storeManagerService.admin_id == admin_id).all()
#     response = {'status': 'true', 'message': "Data Received Successfully", 'data': data}
#     return response

# def get_service_by_admin(admin_id: str, db: Session):
#     data = db.query(storeManagerService).filter(storeManagerService.admin_id == admin_id).order_by(storeManagerService.id.desc()).all()

#     response_data = []

#     for service in data:
        
#         category_id = service.categories
#         category_details = None
#         if category_id:
#             category_details = db.query(Category).filter(Category.id == category_id).first()
#         # Combine milestone, time_required, and unit into process_details array
#         process_details = []
#         for milestone, time_required, unit in zip(service.milestone.split(','),
#                                                  service.time_required.split(','),
#                                                  service.unit.split(',')):
#             process_details.append({'milestone': milestone, 'time_required': time_required, 'unit': unit})

#         service_dict = service.dict()
#         service_dict['process_details'] = process_details
#         service_dict['category_details'] = category_details

#         response_data.append(service_dict)

#     response = {'status': 'true', 'message': "Data Received Successfully", 'data': response_data}
#     return response

def get_service_by_admin(db: Session, admin_id: str, search: Optional[str] = None, categories: Optional[str] = None, sub_categories: Optional[str] = None):
    # Query the storeManagerService table for the provided admin_id
    services_query = db.query(storeManagerService).filter(storeManagerService.admin_id == admin_id)

    # Apply search filter if search parameter is provided
    if search:
        services_query = services_query.filter(
            (storeManagerService.service_tital.ilike(f"%{search}%")) |
            (storeManagerService.service_code.ilike(f"%{search}%")) |
            (storeManagerService.categories.ilike(f"%{search}%"))

        )
    if categories:
        services_query = services_query.filter(
            (storeManagerService.categories==categories)
        )
        
    if sub_categories:
        services_query = services_query.filter(
            (storeManagerService.sub_categories==sub_categories)
        )    

    # Fetch the filtered services
    data = services_query.order_by(storeManagerService.id.desc()).all()

    response_data = []

    for service in data:
        category_id = service.categories
        category_details = None
        if category_id:
            category_details = db.query(Category).filter(Category.id == category_id).first()
            
        sub_category_id = service.sub_categories
        sub_category_details = None
        if sub_category_id:
            sub_category_details = db.query(SubCategory).filter(SubCategory.id == sub_category_id).first()      

        # Combine milestone, time_required, and unit into process_details array
        process_details = []
        for milestone, time_required, unit in zip(service.milestone.split(','),
                                                 service.time_required.split(','),
                                                 service.unit.split(',')):
            process_details.append({'milestone': milestone, 'time_required': time_required, 'unit': unit})

        service_dict = service.dict()
        service_dict['process_details'] = process_details
        service_dict['category_details'] = category_details
        service_dict['sub_category_details'] = sub_category_details

        response_data.append(service_dict)

    response = {'status': 'true', 'message': "Data Received Successfully", 'data': response_data}
    return response

# def create(db: Session, service_create: storeManagerServiceCreate):
#     db_service_create = storeManagerService(**service_create.dict())
#     db.add(db_service_create)
#     db.commit()
#     db.refresh(db_service_create)
#     response = {'status': 'true','message':"Service Details Added Successfully",'data':db_service_create}
#     return response

def create(db: Session, service_create: storeManagerServiceCreate):
    admin_id = service_create.admin_id

    # Query the UserAddNewForm table to get the company_name based on admin_id
    user_form = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == admin_id).first()

    if user_form:
        company_name = user_form.company_name

        # Generate a unique service_code
        service_code = generate_service_code(company_name, db)

        # Proceed with creating the service
        service_create_dict = service_create.dict(exclude={'service_code'})  # Exclude service_code
        db_service_create = storeManagerService(**service_create_dict, service_code=service_code)
        db.add(db_service_create)
        db.commit()
        db.refresh(db_service_create)

        response = {'status': 'true', 'message': "Service Details Added Successfully", 'data': db_service_create}
        return response
    else:
        return {'status': 'false', 'message': 'Admin ID not found'}

def generate_service_code(company_name: str, db: Session):
    # Extract the first 3 characters from company_name
    company_prefix = company_name[:3].upper()

    # Generate a random 5-digit number
    random_number = ''.join(random.choices(string.digits, k=5))

    # Combine admin_id, company_prefix, and random_number to form service_code
    service_code = f"{company_prefix}{random_number}"

    # Check if the generated service_code already exists
    while db.query(storeManagerService).filter(storeManagerService.service_code == service_code).first():
        random_number = ''.join(random.choices(string.digits, k=5))
        service_code = f"{company_prefix}{random_number}"

    return service_code
   
def update(service_id:int, service_details:storeManagerService,db:Session):
    service_details_update = service_details.dict(exclude_unset=True)
    db.query(storeManagerService).filter(storeManagerService.id == service_id).update(service_details_update)
    db.commit()
    response = {'status': 'true','message':"Service Details Updated Successfully",'data':service_details_update}
    return response

# def delete_service_by_service_id(service_id: int, db: Session):
#     service_details = db.query(storeManagerService).filter(storeManagerService.id == service_id).first()
#     if service_details:
#         db.delete(service_details)
#         db.commit()
#         return {'status':'true', 'message':"Service Details deleted successfully", 'data':service_details}
#     return {"status":'false',  'message':"Service not found"}

def delete_service_by_service_id(id: int, db: Session):
    service_details = db.query(Category).filter(Category.id == id).first()

    if not service_details:
       {'status': 'false', 'message': "Service not found"}

    db.delete(service_details)
    db.commit()

    response = {
        'status': 'true',
        'message': "Service Details deleted successfully"
    }
    
    return response