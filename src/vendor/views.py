from typing import List
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from .models import Vendor,VendorCreate, VendorDelete
from .service import create,get_all_vendor,update,get_vendor_by_admin_id,delete_vendor_id
from src.parameter import get_token

router = APIRouter()

@router.get("/showAllVendor")
def read_all_Vendor_details(auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_all_vendor(db=db)
        
@router.get("/showVendorByAdmin/{admin_id}")
def read_Vendor_by_admin(admin_id:str,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_vendor_by_admin_id(admin_id=admin_id,db=db)

@router.post("/createVendor")
def create_Vendor_details(vendor: VendorCreate,
                auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return create(db=db, vendor=vendor)
     
@router.put("updateVendor/{vendor_id}")
def update_Vendor_details(vendor_id:int,vendor:VendorCreate,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db:Session=Depends(get_db)):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return update(vendor_id=vendor_id,vendor=vendor,db=db)

@router.post("/deleteVendor/")
def delete_Vendor_details_by_id(
      request: VendorDelete, 
      auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), 
      db: Session = Depends(get_db)):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    else:
        return delete_vendor_id(request=request, db=db)
        
        

from fastapi import APIRouter, UploadFile, File, Depends
import csv
import io
import pandas as pd
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew
import re  
from src.SuperAdminPlanAndPrice.models import SuperAdminPlanAndPrice
from typing import List,Optional

@router.post("/upload-multiple-vendor/")
def upload_multiple_vendor(
    admin_id: str,
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

        if employe_id:
            admin_emp_id = employe_id
            created_by_type = "employee"
        else:
            admin_emp_id = admin_id
            created_by_type = "admin" 

        for idx, row in enumerate(rows, start=2):

            try:
                cleaned_data = {k: (str(v).strip() if isinstance(v, str) else v) for k, v in row.items()}
                cleaned_data = {k: (v if v != "" else None) for k, v in cleaned_data.items()}
                cleaned_data["admin_id"] = admin_id
                cleaned_data["employe_id"] = employe_id
                cleaned_data["admin_emp_id"] = admin_emp_id  # or get dynamically if needed
                cleaned_data["created_by_type"] = created_by_type  # or get dynamically if needed


                bname = cleaned_data.get("Business Name")
                pno = cleaned_data.get("PAN No")
                gstn = cleaned_data.get("GST No")
                Contact_Person = cleaned_data.get("Contact Person")
                Contact_Number = cleaned_data.get("Contact Number")
                Email = cleaned_data.get("Email")
                Vendor_Name = cleaned_data.get("Vendor Name")

                cleaned_data["business_name"] = bname  # or get dynamically if needed
                cleaned_data["vendor_name"] = Vendor_Name  # or get dynamically if needed
                cleaned_data["contact_person"] = Contact_Person  # or get dynamically if needed
                cleaned_data["email"] = Email  # or get dynamically if needed
                cleaned_data["pan_no"] = pno  # or get dynamically if needed
                cleaned_data["contact_gst_number"] = gstn  # or get dynamically if needed
                cleaned_data["contact_number"] = Contact_Number  # or get dynamically if needed


                vendor = Vendor(**cleaned_data)
                db.add(vendor)
                db.commit()
                db.refresh(vendor)
                created += 1

            except Exception as e:
                failed_rows.append({
                    "row_number": idx,
                    "error": str(e),
                    "row_data": row
                })

        return {
            "status": "true" if created else "false",
            "message": f"{created} vendor(s) created.",
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

@router.get("/generate-vendor-template")
def generate_product_template():
    headers = ["Vendor Name","Business Name","PAN No","GST No","Contact Person","Contact Number","Email"]

    dummy_data = [
        ["ramu","ABC Traders", "ABCDE1234F", "27ABCDE1234F1Z5", "John Doe", "9876543210", "abc@example.com"],
        ["ramu kaka","XYZ Supplies", "XYZAB4321Z", "29XYZAB4321Z2P6", "Jane Smith", "9123456780", "xyz@example.com"],
    ]


    # Create an in-memory byte stream
    output = io.BytesIO()
    
    # Create a new workbook and a worksheet
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('Product Template')
    
    # Write headers to the first row
    worksheet.write_row('A1', headers)

    # Write dummy data starting from row 2 (index 1)
    for idx, row_data in enumerate(dummy_data, start=1):
        worksheet.write_row(idx, 0, row_data)  # (row index, column index, data)


    # Close the workbook and save to the byte stream
    workbook.close()
    output.seek(0)

    # Return the Excel file as a streaming response
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=Vendor_template.xlsx"}
    )

        
        
        
        