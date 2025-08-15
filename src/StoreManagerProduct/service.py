from .models import storeManagerProduct, storeManagerProductCreate,StoreManagerProductBatchCreate,storeManagerProductRead,ProductDetailsBycode
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status, HTTPException
from src.Productwisestock.models import ProductWiseStock
from src.Category.models import Category
from src.SubCategory.models import SubCategory
import string
import random
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew
from src.AdminAddEmployee.models import AdminAddEmployee
from pydantic import UUID4, ValidationError, validator
from sqlalchemy import select
from sqlalchemy import desc
from src.ProductStages.models import ProductStages
from src.cre_upd_name import get_creator_updator_info
from src.QuotationProductEmployee.models import QuotationProductEmployee
from src.AdminAddEmployee.models import AdminAddEmployee
from src.Notifications.models import Notification
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew
from src.ProductQuantityDetails.models import ProductQuantity

def get_all_product(db: Session):
    data = db.query(storeManagerProduct).order_by(storeManagerProduct.id.desc()).all()
    response = {'status': 'true', 'message': "Data Received Successfully", 'data': data}
    return response





def get_product_by_admin(db: Session, admin_id: str, search: str = None, categories: Optional[str] = None,
                         sub_categories: Optional[str] = None , emp_id: Optional[str] = None, 
                         Product_code: Optional[str] = None, 
                         product_type: Optional[str] = None, 
                         admin_emp_id: Optional[str] = None, created_by_type: Optional[str] = None,is_visible: Optional[bool] = None):
    
    
    store_manager_products_query = db.query(storeManagerProduct).filter(storeManagerProduct.admin_id == admin_id)
    
    if emp_id:
        store_manager_products_query = store_manager_products_query.filter(
            storeManagerProduct.emplpoyee_id == emp_id
        )
        
    if Product_code:
        store_manager_products_query = store_manager_products_query.filter(
            storeManagerProduct.item_code == Product_code
        )    

    if is_visible is not None:
        store_manager_products_query = store_manager_products_query.filter(
            storeManagerProduct.is_visible == is_visible
        )

    if search:
        store_manager_products_query = store_manager_products_query.filter(
            (storeManagerProduct.product_tital.ilike(f"%{search}%")) |
            (storeManagerProduct.item_code.ilike(f"%{search}%")) |
            (storeManagerProduct.categories.ilike(f"%{search}%"))
        )

    if categories:
        store_manager_products_query = store_manager_products_query.filter(
            storeManagerProduct.categories == categories
        )

    if sub_categories:
        store_manager_products_query = store_manager_products_query.filter(
            storeManagerProduct.sub_categories == sub_categories
        )

    if product_type:
        store_manager_products_query = store_manager_products_query.filter(
            storeManagerProduct.type == product_type
        )

    store_manager_products = store_manager_products_query.order_by(storeManagerProduct.id.desc()).all()

    response_data = []

    for store_manager_product in store_manager_products:
        product_stock_data = db.query(ProductWiseStock).filter(
            ProductWiseStock.product_id == store_manager_product.id
        ).first()

        # Updated calculation of buffer_until_low_stock
        opening_stock = 0 if store_manager_product.opening_stock in [None, 'null', ''] else int(store_manager_product.opening_stock)

        #opening_stock = 0 if store_manager_product.opening_stock is None else int(store_manager_product.opening_stock)
        minimum_required_quantity = 0 if store_manager_product.minimum_requuired_quantity_for_low_stock in [None, 'null', ''] else int(store_manager_product.minimum_requuired_quantity_for_low_stock)
        
        buffer_until_low_stock = opening_stock - minimum_required_quantity

        # Determine stock status
        if opening_stock == 0 and minimum_required_quantity == 0:
            status = "LOW STOCK"
        elif buffer_until_low_stock < minimum_required_quantity:
            status = "LOW STOCK"
        else:
            status = "AVAILABLE"

        # Category and Subcategory details
        category_details = db.query(Category).filter(Category.id == store_manager_product.categories).first()
        sub_category_details = db.query(SubCategory).filter(SubCategory.id == store_manager_product.sub_categories).first()

        # Convert store manager product to dictionary
        store_manager_product_dict = store_manager_product.dict()

        # Fetch product stages
        product_stages = db.query(ProductStages).filter(
            ProductStages.product_id == store_manager_product.id,
            ProductStages.type == "Admin"  , ProductStages.is_from_product == True 
        ).all()

        # Stage details
        stages_data = [
            {
                "id": stage.id,
                "admin_id": stage.admin_id,
                "product_id": stage.product_id,
                "assign_employee": stage.assign_employee,
                "steps": stage.steps,
                "time_riquired_for_this_process": stage.time_riquired_for_this_process,
                "day": stage.day,
                "type": stage.type,
                "selected_product_ids":[] if stage.selected_product_ids is None else list(map(int, stage.selected_product_ids.split(","))),
                "step_id": stage.step_id,
                "step_item": stage.step_item,
                "serial_number": stage.serial_number,
                "file_path": stage.file_path,
                "created_at": stage.created_at,
                "updated_at": stage.updated_at
            }
            for stage in product_stages
        ]

        qty_details_raw = db.query(ProductQuantity).filter(ProductQuantity.product_id == store_manager_product.id).all()
        stock_updator_list = []

        for qty in qty_details_raw:
            qty_admin_emp_name = ''
            if qty.admin_emp_id:
                if qty.created_by_type == 'employee':
                    emp = db.query(AdminAddEmployee).filter(
                        AdminAddEmployee.id == int(qty.admin_emp_id)
                    ).first()
                    if emp:
                        qty_admin_emp_name = f"{emp.employe_name}({emp.employee_id})"
                elif qty.created_by_type == 'admin':
                    admin = db.query(SuperAdminUserAddNew).filter(
                        SuperAdminUserAddNew.id == int(qty.admin_emp_id)
                    ).first()
                    if admin:
                        qty_admin_emp_name = f"{admin.full_name}(Admin)"
            
            stock_updator_list.append({
                **qty.__dict__,
                "qty_admin_emp_name": qty_admin_emp_name
            })

        admin_emp_name = ''
        if store_manager_product.admin_emp_id:
            if store_manager_product.created_by_type == 'employee':
                emp = db.query(AdminAddEmployee).filter(
                    AdminAddEmployee.id == int(store_manager_product.admin_emp_id)
                ).first()
                if emp:
                    admin_emp_name = f"{emp.employe_name}({emp.employee_id})"
            elif store_manager_product.created_by_type == 'admin':
                admin = db.query(SuperAdminUserAddNew).filter(
                    SuperAdminUserAddNew.id == int(store_manager_product.admin_emp_id)
                ).first()
                if admin:
                    admin_emp_name = f"{admin.full_name}(Admin)"


        # Add calculated data to the product dictionary
        all_data = {
            'available_quantity': opening_stock,
            #'availability': "Out of Stock" if status == "LOW STOCK" else "In Stock",
            'status': status,
            'buffer_until_low_stock': buffer_until_low_stock,
            'minimum_required_quantity_for_low_stock': str(minimum_required_quantity),
            'category_details': category_details.dict() if category_details else None,
            'sub_category_details': sub_category_details.dict() if sub_category_details else None,
            'stage': stages_data,
            'type': store_manager_product.type.strip() if store_manager_product.type else None,  
            'admin_emp_name': admin_emp_name,
            'stock_updator_list': stock_updator_list,
        }
        created_updated_data = get_creator_updator_info(
            admin_emp_id=store_manager_product.admin_emp_id,
            created_by_type=store_manager_product.created_by_type,
            updated_admin_emp_id=store_manager_product.updated_admin_emp_id,
            updated_by_type=store_manager_product.updated_by_type,
          db=db
        )


        store_manager_product_dict.update({**all_data, **created_updated_data})

        # Process details
        process_details = []
        if store_manager_product.time_riquired_for_this_process:
            for time_required, unit, step in zip(store_manager_product.time_riquired_for_this_process.split(','),
                                                 store_manager_product.unit.split(','),
                                                 store_manager_product.steps.split(',')):
                process_details.append({'time_required': time_required, 'unit': unit, 'step': step})

        store_manager_product_dict['process_details'] = process_details

        response_data.append(store_manager_product_dict)

    response = {'status': 'true', 'message': "Data Received Successfully", 'data': response_data}
    return response



    
def create(db: Session, product_create: storeManagerProductCreate):
    admin_id = product_create.admin_id
    user_form = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == admin_id).first()

    if user_form:
        company_name = user_form.company_name
        item_code = generate_item_code(company_name, db)
        opening_stock = product_create.opening_stock
        minimum_required_quantity = product_create.minimum_requuired_quantity_for_low_stock

        availability = "In Stock" if opening_stock and float(opening_stock) >= float(minimum_required_quantity or 0) else "Out of Stock"
        


        
        product_create_dict = product_create.dict(exclude={'item_code'})
        product_create_dict['availability'] = availability

       
        db_product_create = storeManagerProduct(**product_create_dict, item_code=item_code)
        db.add(db_product_create)
        db.commit()
        db.refresh(db_product_create)

        empname = None
        if db_product_create.created_by_type == "employee":
            empname = db.query(AdminAddEmployee.employe_name).filter(AdminAddEmployee.id == db_product_create.admin_emp_id).first()
        else:
            empname = db.query(SuperAdminUserAddNew.full_name).filter(SuperAdminUserAddNew.id == db_product_create.admin_id).first()
        # Create notification for the admin
        notification = Notification(
            admin_id=db_product_create.admin_id,
            title="New store manager Product Created",
            description=f"A new store manager Product has been created by {empname}.",
            type="storemanagerProduct",
            object_id=str(db_product_create.id),
            created_by_id=db_product_create.admin_emp_id,
            created_by_type=db_product_create.created_by_type
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)

        for stage in product_create.stage:
            product_stage_entry = ProductStages(
                admin_id=admin_id,
                product_id=db_product_create.id,
                steps=stage.steps,
                time_riquired_for_this_process=stage.time_riquired_for_this_process,
                day=stage.day,
                assign_employee=stage.assign_employee,
                type=stage.type,
                step_id=stage.step_id,
                step_item=stage.step_item,
                serial_number =stage.serial_number,
                file_path =stage.file_path,
                selected_product_ids=(",".join(map(str, stage.selected_product_ids)) if stage.selected_product_ids else None),
                is_from_product=True,

            )
            db.add(product_stage_entry)
            db.commit()

        response = {
            'status': 'true',
            'message': "Product Details Added Successfully"
           
        }
        return response
    else:
        return {'status': 'false', 'message': 'Admin ID not found'}



def generate_item_code(company_name: str, db: Session):
    
    company_prefix = company_name[:3].upper()

    
    random_number = ''.join(random.choices(string.digits, k=5))

    
    item_code = f"{company_prefix}{random_number}"

   
    while db.query(storeManagerProduct).filter(storeManagerProduct.item_code == item_code).first():
        random_number = ''.join(random.choices(string.digits, k=5))
        item_code = f"{company_prefix}{random_number}"

    return item_code


def update(product_id: int, product_details: storeManagerProduct, db: Session):
    product_details_update = product_details.dict(exclude_unset=True)
    db.query(storeManagerProduct).filter(storeManagerProduct.id == product_id).update(product_details_update)
    db.commit()
    
    opening_stock = product_details_update.get('opening_stock')

    if opening_stock is not None:
        
        product_stock_entry = db.query(ProductWiseStock).filter(ProductWiseStock.product_id == product_id).first()

        if product_stock_entry:
            
            product_stock_entry.total_quantity = opening_stock
            product_stock_entry.updated_at = datetime.now()
        else:
            
            new_product_stock_entry = ProductWiseStock(
                admin_id=product_details.admin_id,  
                product_id=product_id,
                total_quantity=opening_stock,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            db.add(new_product_stock_entry)
        
        db.commit()
    response = {'status': 'true', 'message': "Product Details Updated Successfully", 'data': product_details_update}
    return response


def delete_product_by_product_id(id: int, db: Session):
    product_details = db.query(storeManagerProduct).filter(storeManagerProduct.id == id).first()

    if not product_details:
        {'status': 'false', 'message': "Product not found"}
    code = product_details.item_code

    exist = db.query(QuotationProductEmployee).filter(QuotationProductEmployee.product_code == code).first()
    if exist:
        return {'status': 'false', 'message': "Product is linked to a quotation and cannot be deleted"}

    db.delete(product_details)
    db.commit()

    response = {
        'status': 'true',
        'message': "Product Details deleted successfully"
    }

    return response


def create_multiple_products(db: Session, products: List[storeManagerProductCreate]):
    for product_create in products:
        product_create_dict = product_create.dict()
        admin_id = product_create.admin_id

        user_form = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == admin_id).first()

        if user_form:
            company_name = user_form.company_name
            item_code = generate_item_code(company_name, db)

            opening_stock = product_create.opening_stock
            minimum_required_quantity = product_create.minimum_requuired_quantity_for_low_stock

            availability = "Out of Stock"
            if opening_stock and minimum_required_quantity:
                try:
                    opening_stock = float(opening_stock)
                    minimum_required_quantity = float(minimum_required_quantity)
                    availability = (
                        "In Stock" if opening_stock >= minimum_required_quantity else "Out of Stock"
                    )
                except ValueError:
                    pass

            product_create_dict = product_create.dict(exclude={'item_code', 'stage'})
            product_create_dict['availability'] = availability

            db_product_create = storeManagerProduct(**product_create_dict, item_code=item_code)
            db.add(db_product_create)
            db.commit()
            db.refresh(db_product_create)

            for stage in product_create.stage:
                product_stage_entry = ProductStages(
                    admin_id=admin_id,
                    product_id=db_product_create.id,
                    steps=stage.steps,
                    time_riquired_for_this_process=stage.time_riquired_for_this_process,
                    day=stage.day,
                    assign_employee=stage.assign_employee,
                    type=stage.type,
                    selected_product_ids=(",".join(map(str, stage.selected_product_ids)) if stage.selected_product_ids else None),
                    is_from_product=True,

                )
                db.add(product_stage_entry)
                db.commit()

            product_stock_entry = ProductWiseStock(
                admin_id=admin_id,
                emplpoyee_id=product_create.emplpoyee_id,
                product_id=db_product_create.id,
                total_quantity=opening_stock,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            db.add(product_stock_entry)
            db.commit()

    return {"status": "true", "message": "All products added successfully"}
    
    
def get_filtered_products(
    db: Session,
    admin_id: str,
    employee_id: Optional[str] = None,
    product_name: Optional[str] = None,
    is_visible: Optional[bool] = None
) -> List[dict]:
    query = select(storeManagerProduct).where(storeManagerProduct.admin_id == admin_id)
    
    if employee_id:
        query = query.where(storeManagerProduct.emplpoyee_id == employee_id)
    
    if is_visible is not None:
        query = query.where(storeManagerProduct.is_visible == is_visible)
    
    if product_name and len(product_name) >= 3:
        query = query.where(storeManagerProduct.product_tital.ilike(f"%{product_name}%"))

    query = query.order_by(desc(storeManagerProduct.id))
    
    result = db.execute(query)
    products = result.scalars().all()

    response_data = []
    status = None

    for product in products:

        # Updated calculation of buffer_until_low_stock
        opening_stock = 0 if product.opening_stock in [None, 'null', ''] else int(product.opening_stock)

        #opening_stock = 0 if store_manager_product.opening_stock is None else int(store_manager_product.opening_stock)
        minimum_required_quantity = 0 if product.minimum_requuired_quantity_for_low_stock in [None, 'null', ''] else int(product.minimum_requuired_quantity_for_low_stock)
        
        buffer_until_low_stock = opening_stock - minimum_required_quantity

        # Determine stock status
        if opening_stock == 0 and minimum_required_quantity == 0:
            status = "LOW STOCK"
        elif buffer_until_low_stock < minimum_required_quantity:
            status = "LOW STOCK"
        else:
            status = "AVAILABLE"    

        # Fetch stages for the product
        stages = db.query(ProductStages).filter(
            ProductStages.product_id == product.id,
            ProductStages.type == "Admin",
            ProductStages.parent_stage_id == None 
        ).all()

        # Format stages as a list of dictionaries
        stages_data = [
            {
                "id": stage.id,
                "admin_id": stage.admin_id,
                "product_id": stage.product_id,
                "assign_employee": stage.assign_employee,
                "steps": stage.steps,
                "step_id":stage.step_id,
                "time_riquired_for_this_process": stage.time_riquired_for_this_process,
                "day": stage.day,
                "type": stage.type,
                "selected_product_ids": [] if stage.selected_product_ids is None else list(map(int, stage.selected_product_ids.split(","))),
                "created_at": stage.created_at,
                "updated_at": stage.updated_at
            }
            for stage in stages
        ]

        # Determine availability
        opening_stock = int(product.opening_stock or 0)
        minimum_required_quantity = int(product.minimum_requuired_quantity_for_low_stock or 0)

        if opening_stock == 0 and minimum_required_quantity == 0:
            availability = "Low Stock"
        elif float(opening_stock) >= float(minimum_required_quantity):
            availability = "In Stock"
        else:
            availability = "Out of Stock"

        # Create the response dictionary for the product
        product_data = product.dict()
        product_data["availability"] = availability  # Update availability
        product_data["status"] = status  # Update availability
        product_data["stages"] = stages_data  # Add stages to the product data
        response_data.append(product_data)

    return response_data
    
    
    
    
    

def get_product_details(
    db: Session,
    admin_id: str,
    product_id: int,
    employee_id: Optional[str] = None
) -> dict:
    # Query to fetch the product by product ID and admin ID
    query = select(storeManagerProduct).where(
        storeManagerProduct.admin_id == admin_id,
        storeManagerProduct.id == product_id
    )

    # Filter by employee ID if provided
    if employee_id:
        query = query.where(storeManagerProduct.emplpoyee_id == employee_id)

    # Execute the query
    result = db.execute(query)
    product = result.scalars().first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # Fetch associated stages for the product
    stages = db.query(ProductStages).filter(
        ProductStages.product_id == product.id
    ).all()

    # Format stages as a list of dictionaries
    stages_data = [
        {
            "id": stage.id,
            "admin_id": stage.admin_id,
            "product_id": stage.product_id,
            "assign_employee": stage.assign_employee,
            "steps": stage.steps,
            "time_riquired_for_this_process": stage.time_riquired_for_this_process,
            "day": stage.day,
            "type": stage.type,
            "selected_product_ids": [] if stage.selected_product_ids is None else list(map(int, stage.selected_product_ids.split(","))), 
            "created_at": stage.created_at,
            "updated_at": stage.updated_at
        }
        for stage in stages
    ]

    # Create the response dictionary
    product_data = product.dict()
    product_data["stages"] = stages_data  # Add stages to the product data

    return product_data
    


def get_products_by_code(request: ProductDetailsBycode, db: Session):
    result = []
    for pro in request.product_code:
        product = db.query(storeManagerProduct).filter(
            storeManagerProduct.admin_id == request.admin_id,
            storeManagerProduct.item_code == pro
            ).first()
        if product:
            result.append(product)
    return {
        "status": "true",
        "message": "All products added successfully",
        "data":result
    }