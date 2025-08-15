from sqlalchemy.orm import Session
from typing import Dict, List, Union
from sqlalchemy.future import select
from src.QuotationProduct.models import QuotationProductCreate,QuotationProduct,QuotationProductUpdate
from src.parameter import get_current_datetime
from fastapi import APIRouter, Depends, HTTPException, Header
from src.ProductStages.models import ProductStages

from src.QuotationTemplate.models import QuotationTemplate

from src.cre_upd_name import get_creator_updator_info
from src.StoreManagerProduct.models import storeManagerProduct



def create(db: Session, quotation_product_create: QuotationProductCreate) -> Dict:
    admin_id = quotation_product_create.admin_id
    template_id = quotation_product_create.template_id
    product_name = quotation_product_create.product_name

    # Check for existing product name in the same template
    existing_product = db.query(QuotationProduct).filter(
        QuotationProduct.admin_id == admin_id,
        QuotationProduct.template_id == template_id,
        QuotationProduct.product_name == product_name
    ).first()

    if existing_product:
        return {
            'status': 'false',
            'message': f"Product '{product_name}' already exists in this template.",
            'data': None
        }

    # If not exists, proceed to create
    db_quotation_product = QuotationProduct(
        admin_id=admin_id,
        template_id=template_id,
        product_name=product_name,
        product_code=quotation_product_create.product_code,
        hsn_code=quotation_product_create.hsn_code,
        rate_per_unit=quotation_product_create.rate_per_unit,
        quantity=quotation_product_create.quantity,
        total=quotation_product_create.total,
        gst_percentage=quotation_product_create.gst_percentage,
        gross_total=quotation_product_create.gross_total,
        availability=quotation_product_create.availability,
    )

    db.add(db_quotation_product)
    db.commit()
    db.refresh(db_quotation_product)

    response = {
        'status': 'true',
        'message': "Quotation Product Added Successfully",
        'data': db_quotation_product
    }

    return response

from src.StoreManagerProduct.models import storeManagerProduct


def get_products_by_admin_and_template(db: Session, admin_id: str, template_id: str) -> Dict:
    products = db.query(QuotationProduct).filter(
        QuotationProduct.admin_id == admin_id,
        QuotationProduct.template_id == template_id
    ).all()

    if not products:
        return {
            "status": "false",
            "message": "No products found for the given admin_id and template_id."
        }

    if template_id:
        dt = db.query(QuotationTemplate).filter(QuotationTemplate.id == int(template_id)).first()
        created_updated_data = get_creator_updator_info(
            admin_emp_id=dt.admin_emp_id,
            created_by_type=dt.created_by_type,
            updated_admin_emp_id=dt.updated_admin_emp_id,
            updated_by_type=dt.updated_by_type,
            db=db
        )
        
        update = dt.updated_at
        create = dt.created_at
        # Inject timestamps
        created_updated_data["creator_info"]["created_at"] = create
        created_updated_data["updater_info"]["updated_at"] = update  

    product_list = []
    for product in products:
        pro = db.query(storeManagerProduct).filter(storeManagerProduct.id == int(product.product_id)).first()
        if pro is not None:
            product_type = pro.type

        if pro.is_visible == False:
            if product.product_code == pro.item_code:
                continue

        stages = db.query(ProductStages).filter(
            ProductStages.product_id == product.product_id,
            ProductStages.type == "Admin"
        ).all()

        stage_list = [{
            "id": stage.id,
            "admin_id":stage.admin_id,
            "product_id":stage.product_id,
            "assign_employee": stage.assign_employee,
            "steps": stage.steps,
            "time_riquired_for_this_process": stage.time_riquired_for_this_process,
            "day": stage.day,
            "type": stage.type,
            "step_id": stage.step_id,
            "created_at": stage.created_at,
            "updated_at": stage.updated_at
        } for stage in stages]


        all_data = {
            "id": product.id,
            "admin_id": product.admin_id,
            "template_id": product.template_id,
            "product_name": product.product_name,
            "product_code": product.product_code,
            "product_id": product.product_id,
            "hsn_code": product.hsn_code,
            "rate_per_unit": product.rate_per_unit,
            "quantity": product.quantity,
            "total": product.total,
            "gst_percentage": product.gst_percentage,
            "gross_total": product.gross_total,
            "availability": product.availability,
            "discription": product.discription,
            "unit":product.unit,
            "product_type": product_type,
            "created_at": product.created_at,
            "updated_at": product.updated_at,
            "stage": stage_list
        }
        product_list.append(all_data)

    return {
        "status": "true",
        "message": "Products retrieved successfully",
        "data": product_list,
        **created_updated_data
    }


def create_multiple_products(db: Session, products: List[QuotationProductCreate]) -> Dict:
    db_products = []
    for product_data in products:
    
        if product_data.product_id and product_data.template_id:
            # Check for existing product in same template
            exist = db.query(QuotationProduct).filter(
                QuotationProduct.product_id == product_data.product_id,
                QuotationProduct.template_id == product_data.template_id
            ).first()
            
            if exist:
                continue

        if product_data.template_id:
            dt = db.query(QuotationTemplate).filter(QuotationTemplate.id == product_data.template_id).first()
            if product_data.employee_id:
                updated_by_type = "employee"
                updated_admin_emp_id = product_data.employee_id
            else:
                updated_by_type = "admin"
                updated_admin_emp_id = product_data.admin_id  
                
            dt.updated_admin_emp_id =updated_admin_emp_id
            dt.updated_by_type =updated_by_type
            dt.updated_at =get_current_datetime()
            db.commit()

        db_product = QuotationProduct(
            admin_id=product_data.admin_id,
            template_id=product_data.template_id,
            product_name=product_data.product_name,
            product_code=product_data.product_code,
            hsn_code=product_data.hsn_code,
            rate_per_unit=product_data.rate_per_unit,
            quantity=product_data.quantity,
            total=product_data.total,
            gst_percentage=product_data.gst_percentage,
            gross_total=product_data.gross_total,
            availability=product_data.availability,
            product_id=product_data.product_id,
            discription=product_data.discription,
            unit=product_data.unit,
        )
        db_products.append(db_product)
    
   
    db.add_all(db_products)
    db.commit()

   
    for product in db_products:
        db.refresh(product)

    response = {
        'status': 'true',
        'message': f"{len(db_products)} Quotation Products Added Successfully",
        'data': db_products
    }

    return response


def update_quotation_product(
    update_data: QuotationProductUpdate, db: Session,
) -> Union[dict, QuotationProduct]:
    query = select(QuotationProduct).where(
        QuotationProduct.id == update_data.product_id,
        QuotationProduct.admin_id == update_data.admin_id,
        QuotationProduct.template_id == update_data.template_id
    )
    result = db.execute(query)
    product = result.scalar_one_or_none()

    if not product:
        return {"status": "false", "message": "Product not found"}

    # Check against opening stock
    store_pro = db.query(storeManagerProduct).filter(
        storeManagerProduct.id == product.product_id
    ).first()
    
    if store_pro:
        stock = int(store_pro.opening_stock)
    
        try:
            requested_qty = int(update_data.quantity)
        except ValueError:
            return {
                "status": "false",
                "message": "Availability must be a number."
            }
    
        if requested_qty > stock:
            return {
                "status": "false",
                "message": "Requested quantity must be less than or equal to opening stock."
            }

    # Exclude non-updatable fields
    update_fields = update_data.dict(exclude_unset=True, exclude={"product_id", "admin_id", "template_id"})

    for key, value in update_fields.items():
        setattr(product, key, value)

    product.updated_at = get_current_datetime()
    db.add(product)
    db.commit()
    db.refresh(product)

    return product