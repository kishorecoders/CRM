from .models import EmployeeFiles, EmployeeFilesCreate
from sqlmodel import Session
from src.AdminAddEmployee.models import AdminAddEmployee
from sqlalchemy import cast
from sqlmodel import Session, select
from datetime import datetime
from src.Account.service import save_base64_file


# def create(db: Session, setting_create: EmployeeFilesCreate):
#     db_setting = EmployeeFiles(**setting_create.dict())
#     db.add(db_setting)
#     db.commit()
#     db.refresh(db_setting)
#     response = {'status': 'true', 'message': "Employee Files Added Successfully", 'data': db_setting}
#     return response 


def create(db: Session, setting_create: EmployeeFilesCreate):

    # if setting_create.file_path:
    #     current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    #     file_extension = "pdf"
    #     filename = f"{current_datetime}_EmployeeFile_pdf_{setting_create.admin_id}.{file_extension}"
    #     file_path = save_base64_file(setting_create.file_path, filename)
    # else:
    #     file_path = None 

    # if setting_create.image_path:
    #     current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    #     file_extension = "jpg"
    #     filename = f"{current_datetime}_EmployeeFile_image_{setting_create.admin_id}.{file_extension}"
    #     image_path = save_base64_file(setting_create.image_path, filename)
    # else:
    #     image_path = None 


    query = select(EmployeeFiles).where(
        EmployeeFiles.employee_id == setting_create.employee_id,
        EmployeeFiles.admin_id == setting_create.admin_id,
        EmployeeFiles.type == setting_create.type
    )
    # existing_record = db.exec(query).first()
    existing_record = db.execute(query).scalars().first()

    if existing_record:
      
        existing_record.image_path = setting_create.image_path
        existing_record.medical_file_path = setting_create.medical_file_path
        existing_record.file_path = setting_create.file_path
        existing_record.m_file_name = setting_create.m_file_name
        existing_record.updated_at = datetime.utcnow()
        db.add(existing_record)
        db.commit()
        db.refresh(existing_record)
        response = {
            "status": "true",
            "message": "Employee File Updated Successfully",
            "data": existing_record
        }
    else:
        data_dict = setting_create.dict()
        data_dict["image_path"] = setting_create.image_path
        data_dict["medical_file_path"] = setting_create.medical_file_path
        data_dict["file_path"] = setting_create.file_path
        data_dict["m_file_name"] = setting_create.m_file_name
        new_record = EmployeeFiles(**data_dict)
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        response = {
            "status": "true",
            "message": "Employee File Added Successfully",
            "data": new_record
        }
    
    return response


# def create(db: Session, setting_create: EmployeeFilesCreate):
   
#     query = select(EmployeeFiles).where(
#         EmployeeFiles.employee_id == setting_create.employee_id,
#         EmployeeFiles.admin_id == setting_create.admin_id,
#         EmployeeFiles.type == setting_create.type
#     )
#     # existing_record = db.exec(query).first()
#     existing_record = db.execute(query).scalars().first()

#     if existing_record:
      
#         existing_record.image_path = setting_create.image_path
#         existing_record.file_path = setting_create.file_path
#         existing_record.updated_at = datetime.utcnow()
#         db.add(existing_record)
#         db.commit()
#         db.refresh(existing_record)
#         response = {
#             "status": "true",
#             "message": "Employee File Updated Successfully",
#             "data": existing_record
#         }
#     else:
        
#         new_record = EmployeeFiles(**setting_create.dict())
#         db.add(new_record)
#         db.commit()
#         db.refresh(new_record)
#         response = {
#             "status": "true",
#             "message": "Employee File Added Successfully",
#             "data": new_record
#         }
    
#     return response



def fetch_employee_files(db: Session, admin_id: int = None, employee_id: int = 0):
    if employee_id != 0:
        # Fetch for specific employee
        results = db.query(EmployeeFiles).filter(
            EmployeeFiles.employee_id == employee_id
        ).all()
    elif admin_id is not None:
        # Fetch all employees under this admin
        results = db.query(EmployeeFiles).filter(
            EmployeeFiles.admin_id == admin_id
        ).all()
    else:
        # Neither admin_id nor valid employee_id provided
        results = []
    response_results = [] 
    for result in results:
        employee = db.query(AdminAddEmployee).filter(
            AdminAddEmployee.id == result.employee_id
        ).first()
        
        if employee:
            result_dict = result.dict()
            result_dict['employee_name'] = employee.employe_name
            response_results.append(result_dict)


    return response_results

