from typing import List,Optional
from fastapi import APIRouter, Depends, HTTPException, status,Header,Query
from sqlmodel import Session
from src.database import get_db
from src.AdminSales.models import AdminSales,AdminSalesCreate,AssignLeadsRequest,AdminAssignLeadsRequest,AdminSalesFilterRequest,ReassignLeadsRequest,RemoveAdminSalesRequest , AdminSalesM, Leadcount
from src.AdminSales.service import create,get_admin_sales_by_multi_id,get_all_admin_sales,get_admin_sales,get_admin_sales_search_two,get_lead_count,delete_admin_sales,show_all_count,get_admin_sales_name,update_admin_sales,lead_assign_employee,get_allocated_leads,get_today_allocated_leads,reassign_leads,remove_admin_sales , create_multi,get_lead_count_main
from src.parameter import get_token
from src.AdminAddEmployee.models import AdminAddEmployee
from fastapi import APIRouter, Depends, Header, Body
from sqlalchemy import desc

router = APIRouter()

@router.get("/ShowAllAdminSales")
def get_all_reffral_details(auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_all_admin_sales(db=db)
    
    return inner_get_plan(auth_token)

@router.post("/CreateAdminSales")
def create_admin_sales_details(admin_sales: AdminSalesCreate,
                auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return create(db=db, admin_sales=admin_sales)
    
    return inner_get_plan(auth_token)


@router.post("/CreateMultipleAdminSales")
def create_admin_sales_details(admin_sales: AdminSalesM,
                auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return create_multi(db=db, admin_sales=admin_sales)
    
    return inner_get_plan(auth_token)


# @router.post("/ShowAdminSales")
# def read_admin_sales_by_multi_id(
#     request: AdminSalesFilterRequest,
#     auth_token: str = Header(None, alias="AuthToken"),
#     db: Session = Depends(get_db),
# ):
    
#     if auth_token != get_token():
#         return {"status": "false", "message": "Unauthorized Request"}

   
#     return get_admin_sales_by_multi_id(
#         db=db,
#         admin_id=request.admin_id,
#         employe_id=request.employe_id,
#         status=request.status,
#         lead_source=request.lead_source,
#         lead_name=request.lead_name,
#         lead_from_date=request.lead_from_date,
#         lead_to_date=request.lead_to_date,
#         time_frame=request.time_frame,
#         lead_id_from=request.lead_id_from,  
#         lead_id_to=request.lead_id_to     
#     )




@router.post("/ShowAdminSales")
def read_admin_sales_by_multi_id(
    request: AdminSalesFilterRequest,
    auth_token: str = Header(None, alias="AuthToken"),
    db: Session = Depends(get_db),
):
    
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    
    return get_admin_sales_by_multi_id(
        db=db,
        admin_id=request.admin_id,
        employe_id=request.employe_id,
        status=request.status,
        lead_source=request.lead_source,
        lead_name=request.lead_name,
        lead_from_date=request.lead_from_date,
        lead_to_date=request.lead_to_date,
        mobile_num=request.mobile_num,
        time_frame=request.time_frame,
        lead_id_from=request.lead_id_from,  
        lead_id_to=request.lead_id_to,
        page=request.page,  
        page_size=request.page_size  
        
    )







@router.get("/leadByName/{admin_id}")
def read_admin_sales(
    admin_id: int,
    employe_id: Optional[str] = None,
    name: Optional[str] = None,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    def inner_get_sales(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_admin_sales(admin_id=admin_id, employe_id=employe_id, name=name, db=db)

    return inner_get_sales(auth_token)






@router.get("/showsearchtwo/{admin_id}")
def read_admin_sales_search_two(
    admin_id: int,
    search_term: Optional[str] = None,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    def inner_get_sales(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_admin_sales_search_two(admin_id=admin_id, search_term=search_term, db=db)

    return inner_get_sales(auth_token)







@router.get("/showleadcount/{admin_id}/{employee_id}")
def read_lead_count(
    admin_id: int,
    employee_id: str,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    def inner_get_lead_count(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_lead_count(admin_id=admin_id, employee_id=employee_id, db=db)

    return inner_get_lead_count(auth_token)






@router.delete("/deleteadminsales/{id}")
def delete_admin_sales_details(id:int,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db:Session=Depends(get_db)):
       def inner_get_plan(auth_token: str):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return delete_admin_sales(id=id,db=db)
    
       return inner_get_plan(auth_token)

   
@router.get("/showAllCount/{admin_id}")
def Admin_all_count_details(admin_id:int,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db:Session=Depends(get_db)):
       def inner_get_plan(auth_token: str):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return show_all_count(admin_id=admin_id,db=db)
    
       return inner_get_plan(auth_token)

 

# @router.put("/UpdateAdminSales/{admin_sales_id}", tags=["AdminSales"])
# def update_admin_sales_details(
#     admin_sales_id: int,
#     admin_sales: AdminSalesCreate,
#     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#     db: Session = Depends(get_db)
# ):
    
#     if auth_token != get_token():
#         return {"status": "false", "message": "Unauthorized Request"}
    
#     return update_admin_sales(admin_sales_id=admin_sales_id, admin_sales_data=admin_sales, db=db)
@router.put("/UpdateAdminSales/{admin_sales_id}", tags=["AdminSales"])
def update_admin_sales_details(
    admin_sales_id: int,
    admin_sales: AdminSalesCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    
    return update_admin_sales(admin_sales_id=admin_sales_id, admin_sales_data=admin_sales, db=db)



@router.get("/admin-sales-name/{admin_id}")
def read_admin_sales_name(admin_id:str, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_admin_sales_name(db=db, admin_id=admin_id)
    
    return inner_get_plan(auth_token)  




@router.post("/leadsAssignEmployee/")
def assign_leads_to_employee(
    request: AssignLeadsRequest,
    db: Session = Depends(get_db),
    auth_token: str = Header(...),  
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    return lead_assign_employee(
        db=db,
        lead_ids=request.lead_ids,  
        employee_id=request.employee_id,
        admin_id=request.admin_id,
    )



@router.post("/getAssignedLeadsByEmployee/")
def get_assigned_leads(
    request: AdminAssignLeadsRequest,  
    db: Session = Depends(get_db),
    auth_token: str = Header(...),  
):

    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    
    admin_id = request.admin_id
    employee_id = request.employee_id

    
    allocated_leads = (
        db.query(AdminSales)
        .filter(AdminSales.admin_id == admin_id, AdminSales.allocated_emplyee_id == employee_id)
        .order_by(desc(AdminSales.id))
        .all()
    )

    if not allocated_leads:
        return {"status": "false", "message": "No leads found for this employee."}

    
    employee = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == employee_id).first()

    
    response = {
        'status': 'true',
        'message': "Data Received Successfully",
        "assigned_leads": allocated_leads,
        "employee_details": {
            "id": employee.id if employee else None,
            "name": employee.employe_name if employee else None,
            "email": employee.employe_email_id if employee else None,
            "phone_number": employee.employe_phone_number if employee else None,
            "employe_job_title": employee.employe_job_title,
            "employee_id": employee.employee_id,
            "employe_user_name": employee.employe_user_name,
            "employe_password": employee.employe_password,
            "employe_confirm_password": employee.employe_confirm_password,
            "employe_remark": employee.employe_remark,
            "level": employee.level,
            "school_or_college_name": employee.school_or_college_name,
            "education_passout_year": employee.education_passout_year,
            "description": employee.description,
            "bank_name": employee.bank_name,
            "bank_account_holder_name": employee.bank_account_holder_name,
            "bank_account_number": employee.bank_account_number,
            "bank_ifsc_code": employee.bank_ifsc_code,
            "skills_list": employee.skills_list,
            "position": employee.position,
            "past_company_name": employee.past_company_name,
            "experience": employee.experience,
            "created_at": employee.created_at,
            "updated_at": employee.updated_at,
        }
    }

    return response






@router.post("/getTodayAssignedLeadsByEmployee/")
def get_today_assigned_leads(
    request: AdminAssignLeadsRequest,
    db: Session = Depends(get_db),
    auth_token: str = Header(...),
):
   
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    
    admin_id = request.admin_id
    employee_id = request.employee_id

    
    allocated_leads = get_today_allocated_leads(db, admin_id, employee_id)

    
    if "status" in allocated_leads and allocated_leads["status"] == "false":
        return allocated_leads

    
    employee = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == employee_id).first()

    response = {
        "status": "true",
        "message": "Data Received Successfully",
        "today_assigned_leads": allocated_leads,
        "employee_details": {
            "id": employee.id if employee else None,
            "name": employee.employe_name if employee else None,
            "email": employee.employe_email_id if employee else None,
            "phone_number": employee.employe_phone_number if employee else None,
            "employe_job_title": employee.employe_job_title if employee else None,
            "employee_id": employee.employee_id if employee else None,
            "employe_remark": employee.employe_remark if employee else None,
            "level": employee.level if employee else None,
        } if employee else None,
    }

    return response



@router.post("/reassignLeads/")
def reassign_leads_to_employee(
    request: ReassignLeadsRequest,
    db: Session = Depends(get_db),
    auth_token: str = Header(...),  
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    return reassign_leads(
        db=db,
        lead_ids=request.lead_ids,
        from_employee_id=request.from_employee_id,
        to_employee_id=request.to_employee_id,
        admin_id=request.admin_id,
    )
    


@router.post("/removeadminsales/")
def remove_admin_sales_details(
    request: RemoveAdminSalesRequest,
    auth_token: str = Header(None, alias="AuthToken"),
    db: Session = Depends(get_db),
    
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    
    if request.admin_id is None and request.employee_id is None:
        return {"status": "false", "message": "At least one of 'admin_id' or 'employee_id' is required with 'lead_id'"}

    return remove_admin_sales(
        lead_id=request.lead_id,
        admin_id=request.admin_id,
        employee_id=request.employee_id,
        db=db
    )



@router.post("/showleadcount")
def read_lead_count_post(
    request: Leadcount,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    def inner_get_lead_count(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_lead_count_main(request , db)

    return inner_get_lead_count(auth_token)



from fastapi import APIRouter, UploadFile, File, Depends
import csv
import io
import pandas as pd
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew
from src.AdminAddEmployee.models import AdminAddEmployee


@router.post("/upload-multiple-adminsales/")
def upload_multiple_admin_sales(
    admin_id : str,
    employee_id : Optional[str] = None,
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

        admin_emp_id = None
        created_by_type = None
        lead_source_name = None
        
        if employee_id:
            admin_emp_id = employee_id
            created_by_type = "employee"
        else:
            admin_emp_id = admin_id
            created_by_type = "admin" 

        if created_by_type and admin_emp_id:
            if created_by_type == "admin":
                query = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == admin_emp_id).first()
                name = query.full_name
                lead_source_name = name
            elif created_by_type == "employee":
                query = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == admin_emp_id).first()
                id = query.employee_id
                name = query.employe_name
                lead_source_name =f"{name}({id})"

        for idx, row in enumerate(rows, start=2):  # assuming header in row 1
            try:
                # Clean & convert empty strings to None
                cleaned_data = {
                    k: (str(v).strip() if isinstance(v, str) else v)
                    for k, v in row.items()
                }
                cleaned_data = {k: (v if v != "" else None) for k, v in cleaned_data.items()}
                cleaned_data["admin_id"] = admin_id  # or get dynamically if needed
                cleaned_data["employee_id"] = employee_id  # or get dynamically if needed
                cleaned_data["admin_emp_id"] = admin_emp_id  # or get dynamically if needed
                cleaned_data["created_by_type"] = created_by_type  # or get dynamically if needed
                cleaned_data["lead_source_name"] = lead_source_name  # or get dynamically if needed

                admin_sales_obj = AdminSales(**cleaned_data)
                create(db, admin_sales_obj)
                created += 1

            except Exception as e:
                failed_rows.append({
                    "row_number": idx,
                    "error": str(e),
                    "row_data": row
                })

        return {
            "status": "true" if created else "false",
            "message": f"{created} AdminSales record(s) created.",
            "failures": failed_rows
        }

    except Exception as e:
        return {
            "status": "false",
            "message": f"File processing failed: {str(e)}"
        }


