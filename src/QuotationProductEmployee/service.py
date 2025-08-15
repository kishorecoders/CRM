from sqlalchemy.orm import Session
from typing import Dict, List,Optional
from sqlalchemy import select
from sqlalchemy import desc
from src.QuotationProductEmployee.models import QuotationProductEmployeeCreate,QuotationProductEmployee,ReleaseRequest,QuotationProductEmployeeRead,StageUpdateRequest,bookRequest
from src.Inventoryoutward.models import InventoryOutward
from fastapi import APIRouter, Depends, HTTPException, Header
from src.StoreManagerProduct.models import storeManagerProduct
from src.parameter import get_current_datetime




def create_multiple_products(db: Session, products: List[QuotationProductEmployeeCreate]) -> Dict:
    db_products = []
    for product_data in products:
      
        if not product_data.quote_id:
            return {
                'status': 'false',
                'message': 'Quotation ID is required for all products'
            }
        
        db_product = QuotationProductEmployee(
            admin_id=product_data.admin_id,
            employee_id=product_data.employee_id,
            quote_id=product_data.quote_id,
            product_name=product_data.product_name,
            product_code=product_data.product_code,
            hsn_code=product_data.hsn_code,
            rate_per_unit=product_data.rate_per_unit,
            quantity=product_data.quantity,
            total=product_data.total,
            gst_percentage=product_data.gst_percentage,
            gross_total=product_data.gross_total,
            availability=product_data.availability,
            discount_type=product_data.discount_type,
            discount_amount=product_data.discount_amount,
            discount_percent=product_data.discount_percent,

            product_payment_type=product_data.product_payment_type,
            product_cash_balance=product_data.product_cash_balance,
            product_account_balance=product_data.product_account_balance,

            dispatch_status=product_data.dispatch_status,
            give_credit=product_data.give_credit,
            remark=product_data.remark,

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





def get_products_by_admin_and_employee(db: Session, admin_id: str, employee_id: str) -> Dict:
    products = db.query(QuotationProductEmployee).filter(
        QuotationProductEmployee.admin_id == admin_id,
        QuotationProductEmployee.employee_id == employee_id
    ).all()

    if not products:
        return {
            "status": "false",
            "message": "No products found for the given admin_id and employee_id."
        }

    product_list = [{
        "id": product.id,
        "admin_id": product.admin_id,
        "employee_id": product.employee_id,
        "product_name": product.product_name,
        "product_code": product.product_code,
        "hsn_code": product.hsn_code,
        "rate_per_unit": product.rate_per_unit,
        "quantity": product.quantity,
        "total": product.total,
        "gst_percentage": product.gst_percentage,
        "gross_total": product.gross_total,
        "availability": product.availability,
        "created_at": product.created_at,
        "updated_at": product.updated_at,
        "status": product.status,
        "discount_type":product.discount_type,
        "discount_amount":product.discount_amount,
        "discount_percent":product.discount_percent,
        "product_payment_type":product.product_payment_type,
        "product_cash_balance":product.product_cash_balance,
        "product_account_balance":product.product_account_balance,

        "dispatch_status":product.dispatch_status,
        "give_credit":product.give_credit,
        "remark":product.remark,
    } for product in products]

    return {
        "status": "true",
        "message": "Products retrieved successfully",
        "data": product_list
    }


from src.InventoryOutwardRemark.models import InventoryOutwardRemark


def create_release_request(request: ReleaseRequest, db: Session):
    product_details = db.query(QuotationProductEmployee).filter(
        QuotationProductEmployee.id == request.product_id
    ).first()

    if not product_details:
        return {"status": "false", "message": "Product ID does not exist"}
        

    if product_details.status == "Requested":
        return {"status": "false", "message": "This product request has already been sent"}
        
    
    product_details.status = "Requested"

    product_details.updated_at = get_current_datetime()

    product_details.product_release_at = get_current_datetime()

    db.add(product_details)
    db.commit()
    db.refresh(product_details)

    if request.employee_id:
        created_by_type = "employee"
        admin_emp_id = request.employee_id
    else:
        created_by_type = "admin"
        admin_emp_id = request.admin_id  

    if request.type and request.InventoryOutward_id and request.add_remark:
        new_outward_remark = InventoryOutwardRemark(
            admin_id=request.admin_id,
            employee_id=request.employee_id,
            add_remark=request.add_remark,
            type=request.type,
            InventoryOutward_id=request.InventoryOutward_id,
        )
        db.add(new_outward_remark)



    existing = db.query(InventoryOutward).filter(
        InventoryOutward.product_id == request.product_id
    ).first()

    if existing:
        existing.status = request.status
        existing.approve_by = "Dispatch"

        db.add(existing)
        db.commit()
        return {"status": "true", "message": "Inventory Outward updated successfully"}
    else:
        new_outward = InventoryOutward(
            admin_id=request.admin_id,
            emplpoyee_id=request.employee_id,
            product_id=request.product_id,
            released_to_person=request.employee_id,
            ask_qty=str(product_details.quantity),
            given_qty=str(product_details.quantity),
            left="0",
            status=request.status,
            approve_by="Dispatch",
            order_id=request.order_id,
            created_by_type=created_by_type,
            admin_emp_id=admin_emp_id
        )
        db.add(new_outward)
        db.commit()
        db.refresh(new_outward)
        return {"status": "true", "message": "Inventory Outward created successfully"}



def create_booked_request(request: bookRequest, db: Session):
    product_details = db.query(QuotationProductEmployee).filter(
        QuotationProductEmployee.id == request.product_id
    ).first()

    if not product_details:
        return {"status": "false", "message": "Product ID does not exist"}
        

    if product_details.booked_status == "1":
        return {"status": "false", "message": "This product request has already been sent"}
        
    
    product_details.booked_status = "1"
    product_details.updated_at = get_current_datetime()

    db.add(product_details)
    db.commit()
    db.refresh(product_details)

    if request.employee_id:
        created_by_type = "employee"
        admin_emp_id = request.employee_id
    else:
        created_by_type = "admin"
        admin_emp_id = request.admin_id  

    existing = db.query(InventoryOutward).filter(
        InventoryOutward.product_id == request.product_id
    ).first()

    if existing:
        existing.book_status = request.status
        existing.approve_by = "Book"

        db.add(existing)
        db.commit()
        return {"status": "true", "message": "Inventory Outward updated successfully"}
    else:
        new_outward = InventoryOutward(
            admin_id=request.admin_id,
            emplpoyee_id=request.employee_id,
            product_id=request.product_id,
            released_to_person=request.employee_id,
            ask_qty=str(product_details.quantity),
            given_qty=str(product_details.quantity),
            left="0",
            book_status=request.status,
            approve_by = "Book",
            order_id=request.order_id ,
            created_by_type = created_by_type,
            admin_emp_id = admin_emp_id
        )
        db.add(new_outward)
        db.commit()
        db.refresh(new_outward)

        return {"status": "true", "message": "Inventory Outward created successfully"}

    # new_outward = InventoryOutward(
    #     admin_id=request.admin_id,
    #     emplpoyee_id=request.employee_id,
    #     product_id=request.product_id,
    #     released_to_person=request.employee_id,
    #     ask_qty=str(product_details.quantity),
    #     given_qty=str(product_details.quantity),
    #     left="0",
    #     book_status=request.status,
    #     approve_by = "Book",
    #     order_id=request.order_id ,
    #     created_by_type = created_by_type,
    #     admin_emp_id = admin_emp_id
    # )
    # db.add(new_outward)
    # db.commit()
    # db.refresh(new_outward)

    # return {"status": "true", "message": "Inventory Outward created successfully"}





def get_filtered_products(
    db: Session,
    admin_id: str,
    employee_id: Optional[str] = None,
    product_name: Optional[str] = None
) -> List[QuotationProductEmployeeRead]:
    query = select(QuotationProductEmployee).where(QuotationProductEmployee.admin_id == admin_id)
    
    if employee_id:
        query = query.where(QuotationProductEmployee.employee_id == employee_id)
    
    if product_name and len(product_name) >= 3:
        query = query.where(QuotationProductEmployee.product_name.ilike(f"%{product_name}%"))

    query = query.order_by(desc(QuotationProductEmployee.id))
    
    result = db.execute(query)  
    return result.scalars().all()



# def update_product_service(request: StageUpdateRequest, db: Session):
#     try:
#         if request.type == "Lead":
#             stmt = select(QuotationProductEmployee).where(
#                 QuotationProductEmployee.admin_id == request.admin_id,
#                 QuotationProductEmployee.id == request.product_id
#             )
#             result = db.execute(stmt)
#             product = result.scalars().first()

#             if not product:
#                 raise HTTPException(status_code=404, detail="Product not found")

#             product.Stages = request.stages
#             product.updated_at = get_current_datetime()
#         else:
#             stmt = select(storeManagerProduct).where(
#                 storeManagerProduct.admin_id == request.admin_id,
#                 storeManagerProduct.id == request.product_id
#             )
#             result = db.execute(stmt)
#             product = result.scalars().first()

#             if not product:
#                 raise HTTPException(status_code=404, detail="Product not found")

#             product.Stages = request.stages
#             product.updated_at = get_current_datetime()

#         db.commit()
#         return {"status": "true", "message": "Stage updated successfully"}

#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
def update_product_service(requests: List[StageUpdateRequest], db: Session):
    try:
        for request in requests:
            if request.type == "Lead":
                stmt = select(QuotationProductEmployee).where(
                    QuotationProductEmployee.admin_id == request.admin_id,
                    QuotationProductEmployee.id == request.product_id
                )
                result = db.execute(stmt)
                product = result.scalars().first()
            else:
                stmt = select(storeManagerProduct).where(
                    storeManagerProduct.admin_id == request.admin_id,
                    storeManagerProduct.id == request.product_id
                )
                result = db.execute(stmt)
                product = result.scalars().first()

            if not product:
                return {"status": "false", "message": "Product not fount with this id"}

            product.Stages = request.stages
            product.updated_at = get_current_datetime()

        db.commit()
        return {"status": "true", "message": "Stages updated successfully for all products"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
