from typing import List,Optional
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from src.StoreManagerProduct.models import storeManagerProduct,storeManagerProductCreate,StoreManagerProductBatchCreate,ProductFilterQuery,ProductDetailsRequest,UpdateProductQuantity,ProductUnableDisabled,UnableDisabled_id,ProductDetailsBycode
from src.StoreManagerProduct.service import create,get_all_product,update,delete_product_by_product_id,get_product_by_admin,create_multiple_products,get_filtered_products,get_product_details,get_products_by_code
from src.parameter import get_token
from datetime import datetime

router = APIRouter()

@router.get("/showAllProduct")
def read_all_product_details(auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_all_product(db=db)
        
@router.get("/showProductByAdmin/{admin_id}")
def read_product_by_admin(admin_id:str, search:Optional[str] = None, emp_id:Optional[str] = None, 
                          categories: Optional[str] = None, sub_categories: Optional[str] = None, 
                          Product_code: Optional[str] = None,
                          admin_emp_id: Optional[str] = None,  
                          created_by_type: Optional[str] = None ,
                          product_type : Optional[str] = None ,
                          is_visible: Optional[bool] = None ,
                          auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_product_by_admin(db=db, admin_id=admin_id,emp_id = emp_id, 
                                        search=search, categories=categories, 
                                        sub_categories=sub_categories,admin_emp_id = admin_emp_id , 
                                        Product_code = Product_code,
                                        product_type = product_type,
                                        is_visible = is_visible,
                                        created_by_type = created_by_type)

        
@router.post("/createProduct")
def create_product_details(product_create: storeManagerProductCreate, 
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    return create(db=db, product_create=product_create)


@router.put("/updateProduct/{product_id}")
def update_product(
    product_id: int,
    product_details: storeManagerProduct,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    # Validate authentication
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    # Fetch existing product
    product = db.query(storeManagerProduct).filter(storeManagerProduct.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product_details.emplpoyee_id:
        updated_by_type = "employee"
        updated_admin_emp_id = product_details.emplpoyee_id
    else:
        updated_by_type = "admin"
        updated_admin_emp_id = product_details.admin_id  

    # Update product fields dynamically
    update_data = product_details.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)

    # Update timestamps
    product.updated_at = datetime.now()
    product.updated_by_type = updated_by_type
    product.updated_admin_emp_id =updated_admin_emp_id
    
    # Commit changes
    db.commit()
    db.refresh(product)

    return {"status": "true", "message": "Product Updated Successfully", "data": update_data}



@router.delete("/deleteProduct/{id}")
def delete_product_details_by_id(id: int, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return delete_product_by_product_id(id=id, db=db)



@router.post("/create_multiple_products")
def create_multiple_products_api(
    product_batch: StoreManagerProductBatchCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    response = create_multiple_products(db=db, products=product_batch.products)
    return response


@router.post("/get_products_list")
def get_products_list(
    query_params: ProductFilterQuery,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db) 
):
    if not query_params.admin_id or query_params.admin_id.strip() == "":
        return {"status": "false", "message": "admin id is required"}

    if auth_token != get_token():
        raise HTTPException(
            status_code=401, 
            detail="Unauthorized Request"
        )
    
    products = get_filtered_products(
        db,
        admin_id=query_params.admin_id,
        employee_id=query_params.employee_id,
        product_name=query_params.product_name,
        is_visible=query_params.is_visible
    )
    
    return {"status": "true", "message": "Products retrieved successfully", "products": products}
    
    
    


@router.post("/get_product_details")
def get_product_details_api(
    request: ProductDetailsRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    # Validate admin_id
    if not request.admin_id or request.admin_id.strip() == "":
        return {"status": "false", "message": "admin id is required"}

    # Validate auth token
    if auth_token != get_token():  # Replace with your actual token validation logic
        raise HTTPException(
            status_code=401,
            detail="Unauthorized Request"
        )

    product = get_product_details(
        db=db,
        admin_id=request.admin_id,
        product_id=request.product_id,
        employee_id=request.employee_id
    )

    return {"status": "true", "message": "Product details retrieved successfully", "product": product}
    


from src.parameter import get_current_datetime
from src.ProductQuantityDetails.models import ProductQuantity

@router.post("/UpdateProductQuantity")
def update_quantity(
    request: UpdateProductQuantity,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if not request.product_id:
        return {"status": "false", "message": "product_id is required"}

    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    upd = db.query(storeManagerProduct).filter(storeManagerProduct.id == request.product_id).first()
    if not upd:
        return {"status": "false", "message": "Product not found"}

    try:
        previous_stock = int(upd.opening_stock or 0)
        quantity_to_add = int(request.quantity)
    except ValueError:
        return {"status": "false", "message": "Invalid quantity: must be an integer"}

    upd.opening_stock = previous_stock + quantity_to_add
    upd.updated_at = get_current_datetime()

    if request.employee_id:
        created_by_type = "employee"
        admin_emp_id = request.employee_id
    else:
        created_by_type = "admin"
        admin_emp_id = request.admin_id  

    dtl = ProductQuantity(
        admin_id=request.admin_id,
        emplpoyee_id=request.employee_id,
        prev_opening_stock =previous_stock,
        new_opening_stock =request.quantity, 
        created_by_type =created_by_type,
        admin_emp_id =admin_emp_id,
        product_id =upd.id,   
        add_remark =request.add_remark
    )

    db.add(dtl)
    db.commit()

    return {
        "status": "true",
        "message": "Product quantity updated successfully"
    }



@router.post("/product_unable_disabled")
def product_unable_disabled(
    request: ProductUnableDisabled,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):

    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    upd = db.query(storeManagerProduct).filter(storeManagerProduct.id == request.product_id).first()
    if not upd:
        return {"status": "false", "message": "Product not found"}
    
    upd.is_visible = request.is_visible

    db.add(upd)
    db.commit()
    db.refresh(upd)
    return {
        "status": "true",
        "message": "Product visibility updated successfully"
    }


@router.post("/unable_disabled")
def product_unable_disabled(
    request: UnableDisabled_id,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    upd = db.query(storeManagerProduct).filter(storeManagerProduct.admin_id == request.admin_id)
    if request.employee_id:
        upd = upd.filter(storeManagerProduct.emplpoyee_id == request.employee_id)  # fixed typo

    products = upd.all()
    if not products:
        return {"status": "false", "message": "Product not found"}

    for product in products:
        product.is_visible = request.is_visible

    db.commit()  # commit once for all updates

    return {
        "status": "true",
        "message": "Product visibility updated successfully"
    }

@router.post("/get_products_list_by_code")
def get_products_list(
    request: ProductDetailsBycode,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(
            status_code=401,
            detail="Unauthorized Request"
        )
    return get_products_by_code(request=request, db=db)
    



from fastapi import APIRouter, UploadFile, File, Depends
import csv
import io
import pandas as pd
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew
import re  
from src.SuperAdminPlanAndPrice.models import SuperAdminPlanAndPrice
from typing import List,Optional
from .service import generate_item_code


@router.post("/upload-multiple-product/")
def upload_multiple_product(
    admin_id: str,
    categories : Optional[str] = None,
    sub_categories : Optional[str] = None,
    employe_id : Optional[str] = None,
    file: UploadFile = File(...),
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    ext = file.filename.lower().split(".")[-1]
    rows = []

    try:
        if ext == "csv":
            content = file.file.read().decode("utf-8")
            csv_reader = csv.DictReader(io.StringIO(content))
            rows = list(csv_reader)

        elif ext == "xlsx":
            df = pd.read_excel(file.file, engine="openpyxl")
            rows = df.fillna("").to_dict(orient="records")
        else:
            return {"status": "false", "message": "Only .csv or .xlsx files are supported."}

        created = 0
        failed_rows = []

        created_by_type = None
        admin_emp_id = None
        item_code = None

        if employe_id:
            admin_emp_id = employe_id
            created_by_type = "employee"
        else:
            admin_emp_id = admin_id
            created_by_type = "admin" 

        user_form = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == admin_id).first()

        if user_form:
            company_name = user_form.company_name
            item_code = generate_item_code(company_name, db)

        for idx, row in enumerate(rows, start=2):

            try:
                cleaned_data = {k: (str(v).strip() if isinstance(v, str) else v) for k, v in row.items()}
                cleaned_data = {k: (v if v != "" else None) for k, v in cleaned_data.items()}
                cleaned_data["admin_id"] = admin_id
                cleaned_data["emplpoyee_id"] = employe_id
                cleaned_data["item_code"] = item_code
                cleaned_data["admin_emp_id"] = admin_emp_id  # or get dynamically if needed
                cleaned_data["created_by_type"] = created_by_type  # or get dynamically if needed

                cleaned_data["categories"] = categories  # or get dynamically if needed
                cleaned_data["sub_categories"] = sub_categories  # or get dynamically if needed

                product_title = cleaned_data.get("product_title")
                cleaned_data["product_tital"] = product_title

                product = storeManagerProduct(**cleaned_data)
                db.add(product)
                db.commit()
                db.refresh(product)
                created += 1

            except Exception as e:
                failed_rows.append({
                    "row_number": idx,
                    "error": str(e),
                    "row_data": row
                })

        return {
            "status": "true" if created else "false",
            "message": f"{created} product(s) created.",
            "failures": failed_rows
        }

    except Exception as e:
        return {
            "status": "false",
            "message": f"File processing failed: {str(e)}"
        }


from fastapi.responses import StreamingResponse
import io
import xlsxwriter


# Data lists for dropdowns
GST_RATES = ['5%', '12%', '18%', '28%', '0%']
UNITS = [
    'Nos.', 'Pieces', 'Kilograms (kg)', 'Grams (g)', 'Pounds (lbs)',
    'Ton (mt)', 'Liters (L)', 'Milliliters (mL)'
]
SOLD_AS_OPTIONS = ['Pack of', 'Single']
AVAILABILITY_OPTIONS = ['In Stock', 'Out of Stock']
TYPE_OPTIONS = ['Trade', 'Internal Manufacture']

@router.get("/generate-product-template")
def generate_product_template():
    headers = [
        'product_title', 'item_code', 'hsn_sac_code', 'gst_rate',
        'description', 'price_per_product', 'unit', 'sold_as',
        'opening_stock', 'availability', 'type'
    ]

    dropdowns_map = {
        'gst_rate': GST_RATES,
        'unit': UNITS,
        'sold_as': SOLD_AS_OPTIONS,
        'availability': AVAILABILITY_OPTIONS,
        'type': TYPE_OPTIONS,
    }

    # Dummy data matching dropdowns and field types
    dummy_data = [
        [
            "Sample Product A", "ITEM001", "1234", "18%",
            "A sample item with tax", 99.99, "Pieces", "Single",
            50, "In Stock", "Trade"
        ],
        [
            "Sample Product B", "ITEM002", "5678", "12%",
            "Second sample item", 149.49, "Kilograms (kg)", "Pack of",
            25, "Out of Stock", "Internal Manufacture"
        ]
    ]

    # Create an in-memory byte stream
    output = io.BytesIO()
    
    # Create a new workbook and a worksheet
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('Product Template')
    
    # Write headers to the first row
    worksheet.write_row('A1', headers)

    # Write dummy data
    for row_index, row_data in enumerate(dummy_data, start=1):  # start=1 to write below headers
        worksheet.write_row(row_index, 0, row_data)


    # Set up data validation for each dropdown column
    for i, header in enumerate(headers):
        if header in dropdowns_map:
            values = dropdowns_map[header]
            col_letter = chr(65 + i)  # Convert 0-based index to A, B, C...
            
            # The XlsxWriter data_validation method is much more direct
            worksheet.data_validation(f'{col_letter}2:{col_letter}1000', {
                'validate': 'list',
                'source': values,
                'input_title': 'Select from the list:',
                'input_message': 'Please choose a value from the dropdown.',
                'error_title': 'Invalid Input',
                'error_message': 'Please select from the dropdown.'
            })

    # Close the workbook and save to the byte stream
    workbook.close()
    output.seek(0)

    # Return the Excel file as a streaming response
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=product_template.xlsx"}
    )




    

    
    