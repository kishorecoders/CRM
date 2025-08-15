from .models import Category,CategoryCreate
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status,HTTPException
from src.SubCategory.models import SubCategory
from src.StoreManagerProduct.models import storeManagerProduct
from src.Productwisestock.models import ProductWiseStock
from sqlalchemy import func,cast, Integer

def get_all_category(db: Session):
    data = db.query(Category).order_by(Category.id.desc()).all()
    response = {'status': 'true', 'message': "Data Received Successfully", 'data': data}
    return response

# def create(db: Session, catagory: CategoryCreate):
#     admin_id = catagory.admin_id
#     name = catagory.category_name
    
#     existing_catagory_name = db.query(Category).filter(Category.admin_id == admin_id, Category.category_name == name).first()
#     if existing_catagory_name:
#         return {'status': 'false', 'message': 'This category name is already available.'}
    
#     db_catagory = Category(**catagory.dict())
#     db.add(db_catagory)
#     db.commit()
#     db.refresh(db_catagory)
#     response = {'status': 'true','message':"Category Details Added Successfully",'data':db_catagory}
#     return response

def create(db: Session, catagory: CategoryCreate):
    admin_id = catagory.admin_id
    name = catagory.category_name
    
    
    existing_catagory_name = db.query(Category).filter(Category.admin_id == admin_id, Category.category_name == name).first()
    if existing_catagory_name:
        return {'status': 'false', 'message': 'This category name is already available.'}
    
    if catagory.employe_id:
        created_by_type = "employee"
        admin_emp_id = catagory.employe_id
    else:
        created_by_type = "admin"
        admin_emp_id = catagory.admin_id

    data = catagory.dict()
    data["created_by_type"] = created_by_type
    data["admin_emp_id"] = admin_emp_id

    db_catagory = Category(**data)
    db.add(db_catagory)
    db.commit()
    db.refresh(db_catagory)
    
   
    response = {
        'status': 'true',
        'message': "Category Details Added Successfully",
        'data': db_catagory
    }
    return response



# def get_category_by_admin_id(admin_id: int, type: str, db: Session):
    
#     categories = db.query(Category).filter(Category.admin_id == admin_id, Category.type == type).order_by(Category.id.desc()).all()

    
#     response_data = []
#     for category in categories:
        
#         subcategories = db.query(SubCategory).filter(SubCategory.category_id == category.id).all()

       
#         total_quantity = db.query(func.sum(ProductWiseStock.total_quantity)) \
#             .filter(cast(ProductWiseStock.product_id, Integer) == storeManagerProduct.id) \
#             .filter(cast(storeManagerProduct.categories, Integer) == category.id) \
#             .join(storeManagerProduct, ProductWiseStock.product_id == storeManagerProduct.id) \
#             .scalar() or 0

#         category_data = {
#             'category_id': category.id,
#             'admin_id': category.admin_id,
#             'employe_id': category.employe_id,
#             'category_name': category.category_name,
#             'type': category.type,
#             'created_at': category.created_at,
#             'updated_at': category.updated_at,
#             'quantity': total_quantity,
#             'subcategories': []
#         }

       
#         for subcategory in subcategories:
#             subcategory_data = {
#                 'subcategory_id': subcategory.id,
#                 'admin_id': subcategory.admin_id,
#                 'employe_id': subcategory.employe_id,
#                 'category_id': subcategory.category_id,
#                 'sub_category_name': subcategory.sub_category_name,
#                 'created_at': subcategory.created_at,
#                 'updated_at': subcategory.updated_at
#             }
#             category_data['subcategories'].append(subcategory_data)

#         response_data.append(category_data)

#     response = {'status': 'true',
#                 'message': "Data Received Successfully",
#                 'data': response_data}
#     return response

from src.cre_upd_name import get_creator_updator_info


def get_category_by_admin_id(admin_id: int, type: str, emp_id: Optional[str], db: Session):
    # categories = db.query(Category).filter(Category.admin_id == admin_id, Category.type == type).order_by(Category.id.desc()).all()

    query = db.query(Category).filter(Category.admin_id == admin_id, Category.type == type)

    # Add optional employee filter
    if emp_id:
        query = query.filter(Category.employe_id == emp_id)

    categories = query.order_by(Category.id.desc()).all()

    response_data = []
    for category in categories:
        subcategories = db.query(SubCategory).filter(SubCategory.category_id == category.id).all()

        total_quantity = db.query(func.sum(ProductWiseStock.total_quantity)) \
            .filter(cast(ProductWiseStock.product_id, Integer) == storeManagerProduct.id) \
            .filter(cast(storeManagerProduct.categories, Integer) == category.id) \
            .join(storeManagerProduct, ProductWiseStock.product_id == storeManagerProduct.id) \
            .scalar() or 0

        created_updated_data = get_creator_updator_info(
            admin_emp_id=category.admin_emp_id,
            created_by_type=category.created_by_type,
            updated_admin_emp_id=category.updated_admin_emp_id,
            updated_by_type=category.updated_by_type,
          db=db
        )

        category_data = {
            'category_id': category.id,
            'admin_id': category.admin_id,
            'employe_id': category.employe_id,
            'category_name': category.category_name,
            'type': category.type,
            'created_at': category.ccreated_at,  
            'updated_at': category.updated_at,
            'quantity': total_quantity,
            'subcategories': []
        }

        for subcategory in subcategories:
            subcategory_data = {
                'subcategory_id': subcategory.id,
                'admin_id': subcategory.admin_id,
                'employe_id': subcategory.employe_id,
                'category_id': subcategory.category_id,
                'sub_category_name': subcategory.sub_category_name,
                'created_at': subcategory.created_at,
                'updated_at': subcategory.updated_at
            }
            category_data['subcategories'].append(subcategory_data)

        response_data.append({**category_data ,**created_updated_data})

    response = {'status': 'true',
                'message': "Data Received Successfully",
                'data': response_data}
    return response   


# def update(category_id:int,catagory:Category,db:Session):
#     catagory_update = catagory.dict(exclude_unset=True)
#     db.query(Category).filter(Category.id == category_id).update(catagory_update)
#     db.commit()
#     response = {'status': 'true','message':"Category Details Updated Successfully",'data':catagory_update}
#     return response



def update(category_id: int, catagory: CategoryCreate, db: Session):
    # Determine who is updating
    if catagory.employe_id:
        created_by_type = "employee"
        admin_emp_id = catagory.employe_id
    else:
        created_by_type = "admin"
        admin_emp_id = catagory.admin_id

    # Get only fields that are being updated
    catagory_update = catagory.dict(exclude_unset=True)

    # Add tracking info
    catagory_update["updated_by_type"] = created_by_type
    catagory_update["updated_admin_emp_id"] = admin_emp_id
    catagory_update["updated_at"] = datetime.now()


    # Perform update
    db.query(Category).filter(Category.id == category_id).update(catagory_update)
    db.commit()

    response = {
        'status': 'true',
        'message': "Category Details Updated Successfully",
        'data': catagory_update
    }
    return response

# def delete_category_id(category_id: int, db: Session):
#     category = db.query(Category).filter(Category.id == category_id).first()
#     if category:
#         db.delete(category)
#         db.commit()
#         return {'status':'true', 'message':"Category deleted successfully", 'data':category}
#     return {"status":'false',  'message':"Category not found"}

def delete_category_id(id: int, db: Session):
    category = db.query(Category).filter(Category.id == id).first()

    if not category:
        return {'status': 'false', 'message': "Category not found"}

    
    db.query(SubCategory).filter(SubCategory.category_id == id).delete()

    
    db.delete(category)
    db.commit()

    response = {
        'status': 'true',
        'message': "Category and associated Subcategories deleted successfully"
    }

    return response