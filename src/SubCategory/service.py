from .models import SubCategory,SubCategoryCreate
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status,HTTPException
from src.Category.models import Category

def get_all_sub_category(db: Session):
    data = db.query(SubCategory).order_by(SubCategory.id.desc()).all()
    response = {'status': 'true', 'message': "Data Received Successfully", 'data': data}
    return response

def create(db: Session, sub_category: SubCategoryCreate):
    admin_id = sub_category.admin_id
    name = sub_category.sub_category_name
    category_id = sub_category.category_id
    
    main_category = db.query(Category).filter(Category.id == category_id).first()
    category_name = main_category.category_name
    if category_name == name:  
        return {'status': 'false', 'message':f'The sub category name "{name}" already exists under the category "{category_name}". Please choose a different sub category name.'}
   
    db_sub_category = SubCategory(**sub_category.dict())
    db.add(db_sub_category)
    db.commit()
    db.refresh(db_sub_category)
    response = {'status': 'true','message':"Sub Category Details Added Successfully",'data':db_sub_category}
    return response

def get_sub_category_by_admin_id( db: Session, admin_id: int, category_id:Optional[int] = None):
    sub_category_query = db.query(SubCategory).filter(SubCategory.admin_id == admin_id)
    if category_id is not None:
        sub_category_query = sub_category_query.filter(SubCategory.category_id == category_id)
    sub_category = sub_category_query.order_by(SubCategory.id.desc()).all()
    response = {'status': 'true','message':"Data Recived Successfully",'data':sub_category}
    return response


def get_sub_category_list_by_admin(db: Session, admin_id: int, category_id: Optional[int] = None):
    sub_category_query = db.query(SubCategory)

    # Filter by admin_id
    sub_category_query = sub_category_query.filter(SubCategory.admin_id == admin_id)

    # Filter by category_id if provided
    if category_id is not None:
        sub_category_query = sub_category_query.filter(SubCategory.category_id == category_id)

    # Get subcategories
    sub_categories = sub_category_query.order_by(SubCategory.id.desc()).all()

    response_data = []

    # Include category details if category_id is provided
    if category_id is not None:
        category_details = db.query(Category).filter(Category.id == category_id).first()

        if category_details:
            response_data.append({
                "category_details": {
                    "id": category_details.id,
                    "category_name": category_details.category_name,
                    "admin_id": category_details.admin_id,
                    "employe_id": category_details.employe_id,
                    "type": category_details.type,
                    "created_at": str(category_details.ccreated_at),
                    "updated_at": str(category_details.updated_at)
                },
                "sub_category_details": [{
                    "sub_category_name": sub.sub_category_name,
                    "admin_id": sub.admin_id,
                    "created_at": str(sub.created_at),
                    "employe_id": sub.employe_id,
                    "category_id": sub.category_id,
                    "id": sub.id,
                    "updated_at": str(sub.updated_at)
                } for sub in sub_categories]
            })
    else:
        # If category_id is not provided, return only sub_category_details
        response_data.append({
            "sub_category_details": [{
                "sub_category_name": sub.sub_category_name,
                "admin_id": sub.admin_id,
                "created_at": str(sub.created_at),
                "employe_id": sub.employe_id,
                "category_id": sub.category_id,
                "id": sub.id,
                "updated_at": str(sub.updated_at)
            } for sub in sub_categories]
        })

    response = {'status': 'true', 'message': "Data Received Successfully", 'data': response_data}
    return response
   
def update(sub_category_id:int, sub_category:SubCategory,db:Session):
    sub_category_update = sub_category.dict(exclude_unset=True)
    db.query(SubCategory).filter(SubCategory.id == sub_category_id).update(sub_category_update)
    db.commit()
    response = {'status': 'true','message':"Sub Category Details Updated Successfully",'data':sub_category_update}
    return response

# def delete_sub_category_id(sub_category_id: int, db: Session):
#     sub_category = db.query(SubCategory).filter(SubCategory.id == sub_category_id).first()
#     if sub_category:
#         db.delete(sub_category)
#         db.commit()
#         return {'status':'true', 'message':"Sub Category deleted successfully", 'data':sub_category}
#     return {"status":'false',  'message':"Sub Category not found"}

def delete_sub_category_id(id: int, db: Session):
    sub_category = db.query(SubCategory).filter(SubCategory.id == id).first()

    if not sub_category:
       {'status': 'false', 'message': "Sub Category not found"}

    db.delete(sub_category)
    db.commit()

    response = {
        'status': 'true',
        'message': "Sub Category deleted successfully"
    }
    
    return response