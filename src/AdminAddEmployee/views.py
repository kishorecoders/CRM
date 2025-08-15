from typing import List
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from src.AdminAddEmployee.models import AdminAddEmployee,AdminAddEmployeeCreate,OTPRequest,UpdateEmployeeStatusRequest,DeleteEmployee
from src.AdminAddEmployee.service import create,get_employee_by_admin_id,get_all_admin_employee,show_by_employee,delete_employee,update,update_employee_status
from src.parameter import get_token
from fastapi import Body, Header, Depends
from typing import Optional
import random
import requests
from typing import List, Optional
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew

router = APIRouter()

@router.get("showall/")
def get_all_admin_employee_details(auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_all_admin_employee(db=db)
    
    return inner_get_plan(auth_token)



@router.post("/")
def create_admin_employee_details(
    admin_add_employee: AdminAddEmployeeCreate,
    first_employee_id: Optional[str] = Body(None),  
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db),
):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return create(db=db, admin_add_employee=admin_add_employee, first_employee_id=first_employee_id)
    
    return inner_get_plan(auth_token)








@router.post("/multiple_employee_create_old")
def bulk_create_admin_employees(
    employees: List[AdminAddEmployeeCreate],
    first_employee_id: Optional[str] = Body(None),
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db),
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    if not employees:
        return {"status": "false", "message": "No employees provided."}

    admin_id = employees[0].admin_id
    if not admin_id:
        return {"status": "false", "message": "Admin ID is required"}

    created_count = 0
    skipped_identifiers = []
    first_used = False

    for emp in employees:
        email = emp.employe_email_id
        phone = emp.employe_phone_number
        skip_reason = []

        # Email check
        email_exists = db.query(AdminAddEmployee).filter(
            AdminAddEmployee.admin_id == admin_id,
            AdminAddEmployee.employe_email_id == email
        ).first() or db.query(SuperAdminUserAddNew).filter(
            SuperAdminUserAddNew.email == email
        ).first()
        if email_exists:
            skip_reason.append(f"{email}")

        # Phone check
        phone_exists = db.query(AdminAddEmployee).filter(
            AdminAddEmployee.admin_id == admin_id,
            AdminAddEmployee.employe_phone_number == phone
        ).first() or db.query(SuperAdminUserAddNew).filter(
            SuperAdminUserAddNew.phone_number == phone
        ).first()
        if phone_exists:
            skip_reason.append(f"{phone}")

        if skip_reason:
            skipped_identifiers.extend(skip_reason)
            continue

        # Proceed to create
        response = create(
            db=db,
            admin_add_employee=emp,
            first_employee_id=first_employee_id if not first_used else None
        )

        if response.get("status") == "true":
            created_count += 1
            first_used = True

    if created_count == 0:
        return {
            "status": "false",
            "message": f"All records failed. Skipped: {', '.join(set(skipped_identifiers))}"
        }

    return {
        "status": "true",
        "message": f"{created_count} employee(s) created. {len(employees) - created_count} skipped. {', '.join(set(skipped_identifiers))}"
    }





@router.post("/multiple_employee_create")
def bulk_create_admin_employees(
    employees: List[AdminAddEmployeeCreate],
    first_employee_id: Optional[str] = Body(None),
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db),
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    if not employees:
        return {"status": "false", "message": "No employees provided."}

    admin_id = employees[0].admin_id
    if not admin_id:
        return {"status": "false", "message": "Admin ID is required"}

    # ?? Check if this admin has at least 1 employee already
    existing_employee = db.query(AdminAddEmployee).filter(
        AdminAddEmployee.admin_id == admin_id
    ).first()

    if not existing_employee:
        return {
            "status": "false",
            "message": "Please create the first employee manually. Bulk creation is allowed only after the first entry."
        }

    created_count = 0
    skipped_identifiers = []
    first_used = False

    for emp in employees:
        email = emp.employe_email_id
        phone = emp.employe_phone_number
        skip_reason = []

        # ? Email check
        email_exists = db.query(AdminAddEmployee).filter(
            AdminAddEmployee.admin_id == admin_id,
            AdminAddEmployee.employe_email_id == email
        ).first() or db.query(SuperAdminUserAddNew).filter(
            SuperAdminUserAddNew.email == email
        ).first()
        if email_exists:
            skip_reason.append(f"{email}")

        # ? Phone check
        phone_exists = db.query(AdminAddEmployee).filter(
            AdminAddEmployee.admin_id == admin_id,
            AdminAddEmployee.employe_phone_number == phone
        ).first() or db.query(SuperAdminUserAddNew).filter(
            SuperAdminUserAddNew.phone_number == phone
        ).first()
        if phone_exists:
            skip_reason.append(f"{phone}")

        if skip_reason:
            skipped_identifiers.extend(skip_reason)
            continue

        # ? Proceed to create
        response = create(
            db=db,
            admin_add_employee=emp,
            first_employee_id=first_employee_id if not first_used else None
        )

        if response.get("status") == "true":
            created_count += 1
            first_used = True

    if created_count == 0:
        return {
            "status": "false",
            "message": f"All records failed. Skipped: {', '.join(set(skipped_identifiers))}"
        }

    return {
        "status": "true",
        "message": f"{created_count} employee(s) created. {len(employees) - created_count} skipped. {', '.join(set(skipped_identifiers))}"
    }





@router.get("/ShowEmployee/{admin_id}")
def get_emplyee_details_by_admin_id(
    admin_id: int, 
    role: Optional[str] = None, 
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), 
    db: Session = Depends(get_db)
):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_employee_by_admin_id(admin_id = admin_id , role = role, db = db)

    return inner_get_plan(auth_token)
    
@router.get("ShowByEmployee/{admin_id}/{employee_id}")
def get_emplyee_details_by_admin_id_and_employee_id(admin_id: int, employee_id:str, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
        def inner_get_plan(auth_token: str):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return show_by_employee(admin_id=admin_id, employee_id=employee_id, db=db)
    
        return inner_get_plan(auth_token)

@router.post("/deleteEmployee")
def get_emplyee_details_by_admin_id_and_employee_id(
    request: DeleteEmployee,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), 
    db: Session = Depends(get_db)
):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return delete_employee(db=db , request=request)

    return inner_get_plan(auth_token)
    
@router.put("/UpdateEmployee/{employe_id}")
def update_empoyee_details(employe_id:int,admin_add_employee:AdminAddEmployeeCreate,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db:Session=Depends(get_db)):
       def inner_get_plan(auth_token: str):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return update(employe_id=employe_id,admin_add_employee=admin_add_employee,db=db)
    
       return inner_get_plan(auth_token)  
       
       
       
       


VISION_HLT_API_URL = "https://sms.visionhlt.com/api/mt/SendSMS"
VISION_HLT_API_KEY = "Inu4l5KPoUmyzBSNeo3nKQ"
YOUR_SENDER_ID = "VISHLT" 


@router.post("/send_otp")
def send_otp(
    request: OTPRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db),
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    
    # Step 1: Try to find employee by phone number
    user = db.query(AdminAddEmployee).filter(
        AdminAddEmployee.employe_phone_number == request.phone_number
    ).first()

    if not user:
        # Step 2: Normalize phone number (remove country code '91' if present)
        phone_admin = request.phone_number
        phone1 = phone_admin[2:] if phone_admin.startswith("91") and len(phone_admin) == 12 else phone_admin

        # Step 3: Try to find admin by normalized phone
        user = db.query(SuperAdminUserAddNew).filter(
            SuperAdminUserAddNew.phone_number == phone1
        ).first()

        if not user:
            return {"status": "false", "message": "Phone number not registered"}

    if request.device_token:
        user.device_token = request.device_token
        db.add(user)
        db.commit()
        
    otp = random.randint(100000, 999999)
    print(f"Generated OTP for {request.phone_number}: {otp}")

    
    # message = f"Your verification code for login is {otp}. Kindly use above OTP to login to your account. Thanks and Regards VISION HLT"

    # payload = {
    #     "Account": {
    #         "APIKey": VISION_HLT_API_KEY,
    #         "SenderId": YOUR_SENDER_ID,
    #         "Channel": "Trans",
    #         "DCS": "0",
    #         "SchedTime": None,
    #         "GroupId": None,
    #     },
    #     "Messages": [
    #         {
    #             "Number": f"{request.phone_number}",  
    #             "Text": message,
    #         }
    #     ],
    # }
    
    # try:
    #     print(f"Payload: {payload}")
        
    #     response = requests.post(
    #         VISION_HLT_API_URL,
    #         json=payload, 
    #         headers={"Content-Type": "application/json"}, 
    #     )
    #     response.raise_for_status()  
    #     response_data = response.json()


    #     print(f"Response Status Code: {response.status_code}")
    #     print(f"Response Text: {response.text}")

       
    #     if response_data.get("ErrorCode") == "000":
    return {"status": "true", "message": "OTP sent successfully", "otp": otp}
        # else:
        #     return {
        #         "status": "false",
        #         "message": "Failed to send OTP",
        #         "error": response_data.get("ErrorMessage", "Unknown Error"),
        #     }
    # except requests.exceptions.RequestException as e:
    #     print(f"Error sending OTP: {str(e)}")
    #     return {"status": "false", "message": "Error sending OTP", "error": str(e)}
      




@router.post("/update_employee_status")
def update_employee_status_endpoint(
    request: UpdateEmployeeStatusRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db),
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    return update_employee_status(
        admin_id=request.admin_id,
        employee_id=request.employee_id,
        is_active=request.is_active,
        db=db
    )
    

from fastapi import APIRouter, UploadFile, File, Depends
import csv
import io
import pandas as pd
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew
import re  
from src.SuperAdminPlanAndPrice.models import SuperAdminPlanAndPrice



@router.post("/upload-multiple-employee/")
def upload_multiple_employee(
    admin_id: str,
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

        # Check admin and plan
        admin = db.query(SuperAdminUserAddNew).filter_by(id=admin_id).first()
        if not admin:
            return {"status": "false", "message": "Invalid admin ID"}

        admin_plan = db.query(SuperAdminPlanAndPrice).filter_by(id=admin.plan_id).first()
        if not admin_plan:
            return {"status": "false", "message": "Admin plan not found"}

        total_existing = db.query(AdminAddEmployee).filter_by(admin_id=admin_id).count()
        available_slots = admin_plan.total_access - total_existing

        if available_slots <= 0:
            return {"status": "false", "message": "Employee limit exceeded. Upgrade your plan."}

        # Determine prefix and counter
        prefix = "EMP"
        counter = 1

        last_employee = db.query(AdminAddEmployee).filter_by(admin_id=admin_id).order_by(AdminAddEmployee.id.desc()).first()
        if last_employee and last_employee.employee_id:
            match = re.match(r"([a-zA-Z#_]+)(\d+)", last_employee.employee_id)
            if match:
                prefix, last_counter = match.groups()
                counter = int(last_counter) + 1

        created = 0
        failed_rows = []

        for idx, row in enumerate(rows, start=2):
            if created >= available_slots:
                failed_rows.append({
                    "row_number": idx,
                    "error": f"Plan limit exceeded after {created} records.",
                    "row_data": row
                })
                break

            try:
                cleaned_data = {k: (str(v).strip() if isinstance(v, str) else v) for k, v in row.items()}
                cleaned_data = {k: (v if v != "" else None) for k, v in cleaned_data.items()}
                cleaned_data["admin_id"] = admin_id

                email = cleaned_data.get("employe_email_id")
                phone = cleaned_data.get("employe_phone_number")

                # Email checks
                if email:
                    email_exists = db.query(AdminAddEmployee).filter_by(admin_id=admin_id, employe_email_id=email).first() or \
                                   db.query(SuperAdminUserAddNew).filter_by(email=email).first()
                    if email_exists:
                        raise Exception("Duplicate email")

                # Phone checks
                if phone:
                    phone_exists = db.query(AdminAddEmployee).filter_by(admin_id=admin_id, employe_phone_number=phone).first() or \
                                   db.query(SuperAdminUserAddNew).filter_by(phone_number=phone).first()
                    if phone_exists:
                        raise Exception("Duplicate phone number")

                # Assign employee_id
                employee_id = f"{prefix}{str(counter).zfill(3)}"
                cleaned_data["employee_id"] = employee_id
                counter += 1

                employee = AdminAddEmployee(**cleaned_data)
                db.add(employee)
                db.commit()
                db.refresh(employee)
                created += 1

            except Exception as e:
                failed_rows.append({
                    "row_number": idx,
                    "error": str(e),
                    "row_data": row
                })

        return {
            "status": "true" if created else "false",
            "message": f"{created} employee(s) created.",
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

@router.get("/generate-employee-template")
def generate_employee_template():
    headers = [
        "employe_name",
        "employe_phone_number",
        "employe_email_id",
        "employe_password",
        "employee_salary",
        "paid_leave",
        "Designation"
    ]

    dummy_data = [
        ["Ravi Sharma", "9876543210", "ravi@example.com", "ravi@123", 30000, 12, "Sales Executive"],
        ["Anita Mehra", "9123456789", "anita@example.com", "anita@456", 45000, 15, "HR Manager"],
    ]
    # Create an in-memory byte stream
    output = io.BytesIO()
    
    # Create a new workbook and a worksheet
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('Employee Template')
    
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
        headers={"Content-Disposition": "attachment; filename=employee_template.xlsx"}
    )





from PIL import Image
import io
import face_recognition
import json
from sqlalchemy.future import select
from src.EmployeeFiles.models import EmployeeFiles


def resize_image(file_like, max_width=500):
    """Resize image to improve face recognition speed."""
    file_like.seek(0)
    image = Image.open(file_like)
    if image.width > max_width:
        ratio = max_width / float(image.width)
        new_height = int((float(image.height) * ratio))
        image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)
    output = io.BytesIO()
    image.save(output, format="JPEG")
    output.seek(0)
    return output

def fix_image_bytes(data):
    """Convert stored DB image to usable bytes."""
    if isinstance(data, bytes):
        if data[:3] == b'\xff\xd8\xff':
            return data
        try:
            return bytes(json.loads(data.decode('utf-8')))
        except Exception:
            return data
    elif isinstance(data, str):
        try:
            return bytes(json.loads(data))
        except Exception:
            pass
    elif isinstance(data, list):
        return bytes(data)
    raise ValueError("Unrecognized image format in DB.")

@router.post("/match-face/")
async def match_face(
    file: UploadFile = File(...),
    employee_id: int = None,
    db: Session = Depends(get_db)
):
    if not employee_id:
        raise HTTPException(status_code=400, detail="Employee ID is required.")

    # Step 1: Read uploaded image using PIL
    try:
        image_bytes = await file.read()
        resized_unknown = resize_image(io.BytesIO(image_bytes))
        unknown_image = face_recognition.load_image_file(resized_unknown)
        unknown_encodings = face_recognition.face_encodings(unknown_image)
        if not unknown_encodings:
            raise HTTPException(status_code=400, detail="No face found in uploaded image.")
        unknown_encoding = unknown_encodings[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Uploaded image error: {str(e)}")

    # Step 2: Load known image from DB and process it similarly
    user = db.execute(select(EmployeeFiles).where(EmployeeFiles.employee_id == employee_id)).scalars().first()
    if not user or not user.image_path:
        raise HTTPException(status_code=404, detail="Known image not found in DB.")

    try:
        known_image_bytes = fix_image_bytes(user.image_path)
        resized_known = resize_image(io.BytesIO(known_image_bytes))
        known_image = face_recognition.load_image_file(resized_known)
        known_encodings = face_recognition.face_encodings(known_image)
        if not known_encodings:
            raise HTTPException(status_code=400, detail="No face found in known image.")
        known_encoding = known_encodings[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Known image processing failed: {str(e)}")

    # Step 3: Compare faces
    try:
        tolerance = 0.45
        distance = face_recognition.face_distance([known_encoding], unknown_encoding)[0]
        match = distance <= tolerance
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Face comparison failed: {str(e)}")

    return {
        "status": "success",
        "match": bool(match),
        "distance": float(distance),
        "tolerance": tolerance
    }













