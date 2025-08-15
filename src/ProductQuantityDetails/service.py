from .models import ProductQuantityRead , ProductQuantity
from sqlmodel import Session
from sqlalchemy import desc
from src.ProductStages.models import ProductStages
from src.AdminAddEmployee.models import AdminAddEmployee
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew


from src.StoreManagerProduct.models import storeManagerProduct
def get_filtered_products_details(db: Session,qtydetails:ProductQuantityRead):
    query = db.query(ProductQuantity).filter(ProductQuantity.admin_id == qtydetails.admin_id)
    
    if qtydetails.employee_id:
        query = db.query(ProductQuantity).filter(ProductQuantity.emplpoyee_id == qtydetails.employee_id)
    
    if qtydetails.product_id:
        query = db.query(ProductQuantity).filter(ProductQuantity.product_id == qtydetails.product_id)

    query = query.order_by(desc(ProductQuantity.id))
    
    products = db.execute(query).scalars().all()

    response_data = []

    for product in products:
        product_data = product.dict()

        pro_t = db.query(storeManagerProduct).filter(storeManagerProduct.id == product.id).first()
        if pro_t:
            product_type = pro_t.type

        # Creator details
        creator_info = {
            "name": "",
            "id": None,
            "employee_id": ""
        }

        if product.admin_emp_id:
            if product.created_by_type == 'employee':
                empd = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == int(product.admin_emp_id)).first()
                if empd:
                    creator_info = {
                        "name": empd.employe_name,
                        "id": empd.id,
                        "employee_id": empd.employee_id
                    }
            elif product.created_by_type == 'admin':
                empd = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == int(product.admin_emp_id)).first()
                if empd:
                    creator_info = {
                        "name": empd.full_name,
                        "id": empd.id,
                        "employee_id": "Admin"
                    }

        # Attach creator_info to product_data

        product_data["product_type"] = product_type
        product_data["quantity_updator_info"] = creator_info

        # Append to response list
        response_data.append(product_data)

    return {
        "status": "true",
        "message": "Product fetched successfully",
        "data": response_data
    }

