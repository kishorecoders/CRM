from .models import ActivityCenter,ActivityCenterCreate
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status,HTTPException
from src.AdminSales.models import AdminSales
from src.AdminAddEmployee.models import AdminAddEmployee
from src.ActivityComment.models import ActivityComment
from sqlalchemy.exc import SQLAlchemyError
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew

# def get_all_activity(db: Session):
#     data = db.query(ActivityCenter).order_by(ActivityCenter.id.desc()).all()
#     response = {'status': 'true', 'message': "Data Received Successfully", 'data': data}
#     return response

def create(db: Session, activity_center: ActivityCenterCreate):
    db_activity_center = ActivityCenter(**activity_center.dict())
    db.add(db_activity_center)
    db.commit()
    db.refresh(db_activity_center)
    response = {'status': 'true','message':"Activity Details Added Successfully",'data':db_activity_center}
    return response

# def get_activity_details(lead_id: int, employee_id: str, name: Optional[str], db: Session,):
#     activities = db.query(ActivityCenter).filter(ActivityCenter.admin_sales_id == lead_id, ActivityCenter.employe_id == employee_id).all()

#     data_array = []
#     # Assuming 'name' is the parameter you're searching for

#     for activity in activities:
#         admin_details = db.query(AdminSales).filter(AdminSales.id == activity.admin_sales_id).all()
#         employee_details = db.query(AdminAddEmployee).filter(AdminAddEmployee.employee_id == activity.employe_id).all()

#         # Search within admin_details for the name parameter if it exists
#         lead_details = []
#         if name and name != '':
#             for admin_detail in admin_details:
#                 if name.lower() in admin_detail.name.lower():
#                     lead_details = admin_detail
#                     break  # Stop the loop if found
#         else:
#             # If no name parameter provided, assign the first lead detail
#             lead_details = admin_details[0] if admin_details else []

#         temp = {
#             'Activity_details': activity,
#             'Lead_details': lead_details,
#             'Employee_details': employee_details
#         }
#         data_array.append(temp)

#     response = {
#         'status': 'true',
#         'message': "Data Received Successfully",
#         'data': data_array
#     }

#     return response

from src.cre_upd_name import get_creator_updator_info , get_creator_info



def get_activity_details(lead_id: int, employee_id: Optional[str], name: Optional[str], db: Session):
    lead_details = db.query(AdminSales).filter(AdminSales.id == lead_id).first()

    if not lead_details:
        return {
            'status': 'true',
            'message': "No Lead Found with the provided ID",
            'data': {
                'Lead_details': {},
                'Employee_details': {},
                'activity_detail_list': []
            }
        }

    created_updated_data = get_creator_updator_info(
        admin_emp_id=lead_details.admin_emp_id,
        created_by_type=lead_details.created_by_type,
        updated_admin_emp_id=lead_details.updated_admin_emp_id,
        updated_by_type=lead_details.updated_by_type,
        db=db
    )
    
    allocated_employee_details = {}
    if lead_details.allocated_emplyee_id:
        allocated_employee_details = db.query(AdminAddEmployee).filter(
            AdminAddEmployee.id == lead_details.allocated_emplyee_id
        ).first()

    allocated_employee = None
    if allocated_employee_details:
        allocated_employee = get_creator_info(
            admin_emp_id=allocated_employee_details.id,
            created_by_type="employee",
            db=db
        )


    activities = db.query(ActivityCenter).filter(
        ActivityCenter.admin_sales_id == lead_id,
        #ActivityCenter.employe_id == employee_id
    ).order_by(ActivityCenter.id.desc()).all()

    activity_detail_list = []

    if activities:
        for activity in activities:
            activity_comments = db.query(ActivityComment).filter(
                ActivityComment.activity_id == str(activity.id)
            ).order_by(ActivityComment.id.desc()).all()
            
            
            
            admin_emp_name = ''
            if activity.admin_emp_id:
                if activity.created_by_type == 'employee':
                    empd = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == int(activity.admin_emp_id)).first()
                    if empd:
                        admin_emp_name=f"{empd.employe_name}({empd.employee_id})"
                if activity.created_by_type == 'admin':
                    empd = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == int(activity.admin_emp_id)).first()
                    if empd:
                        admin_emp_name=f"{empd.full_name}(Admin)"

            comm_list = []
            for comment in activity_comments:
                admin_emp_name_comment = ''
                if comment.admin_emp_id:
                    if comment.type == 'employee':
                        empd = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == int(comment.admin_emp_id)).first()
                        if empd:
                            admin_emp_name_comment=f"{empd.employe_name}({empd.employee_id})"
                    if comment.type == 'admin':
                        empd = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == int(comment.admin_emp_id)).first()
                        if empd:
                            admin_emp_name_comment=f"{empd.full_name}(Admin)"
                            
                
            
                comm_list.append({
                 "admin_emp_name":admin_emp_name_comment,
                 "activity_id":comment.activity_id,
                 "admin_emp_id":comment.admin_emp_id,
                 "activity_comment":comment.activity_comment,
                 "activity_comment_id":comment.activity_comment_id,
                 "type":comment.type,
                 "activity_docs":comment.activity_docs,
                 "name":comment.name,
                 "created_at":comment.created_at,
                 "updated_at":comment.updated_at
                })
            activity_data = {
                'Activity_details': activity,
                'admin_emp_name': admin_emp_name,
                #'activity_comment_list': [comment for comment in activity_comments]
                'activity_comment_list': comm_list
            }

            activity_detail_list.append(activity_data)

    lead_data = vars(lead_details).copy()
    lead_data['allocated_employee_details'] = allocated_employee if allocated_employee else None

    lead_data.pop("_sa_instance_state", None)


    response = {
        'status': 'true',
        'message': "Data Received Successfully",
        'data': {
            'Lead_details': {**lead_data,**created_updated_data},
            'Employee_details': allocated_employee_details if allocated_employee_details else {},
            'activity_detail_list': activity_detail_list
        }
    }

    return response





# def get_activity_by_employee(employee_id: str, name: Optional[str], db: Session):
#     activities = db.query(ActivityCenter).filter(ActivityCenter.employe_id == employee_id).all()

#     data_array = []

#     for activity in activities:
#         admin_details = db.query(AdminSales).filter(AdminSales.id == activity.admin_sales_id).all()
#         employee_details = db.query(AdminAddEmployee).filter(AdminAddEmployee.employee_id == activity.employe_id).all()
        
#         lead_details = []
#         if name and name != '':
#             for admin_detail in admin_details:
#                 if name.lower() in admin_detail.name.lower():
#                     lead_details.append(admin_detail)  
#                     break  
#         else:
            
#             lead_details = admin_details if admin_details else []

#         temp = {
#             'Activity_details': activity,
#             'Lead_details': lead_details,
#             'Employee_details': employee_details
#         }
#         data_array.append(temp)

#     response = {
#         'status': 'true',
#         'message': "Data Received Successfully",
#         'data': data_array
#     }

#     return response


def get_activity_by_employee(employee_id: str, name: Optional[str], db: Session):
    
    activities = db.query(ActivityCenter).filter(ActivityCenter.employe_id == employee_id).all()

    
    lead_activity_map = {}

    for activity in activities:
        
        admin_details = db.query(AdminSales).filter(AdminSales.id == activity.admin_sales_id).first()
        if not admin_details:
            continue  
        
        
        if name and name.lower() not in admin_details.name.lower():
            continue

        
        if activity.admin_sales_id not in lead_activity_map:
            lead_activity_map[activity.admin_sales_id] = activity
        else:
           
            existing_activity = lead_activity_map[activity.admin_sales_id]
            if activity.created_at > existing_activity.created_at:
                lead_activity_map[activity.admin_sales_id] = activity

    
    data_array = []
    for lead_id, activity in lead_activity_map.items():
        
        employee_details = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == activity.employe_id).first()

        temp = {
            'Activity_details': activity,
            'Lead_details': [db.query(AdminSales).filter(AdminSales.id == lead_id).first()],
            'Employee_details': employee_details
        }
        data_array.append(temp)

    response = {
        'status': 'true',
        'message': "Data Received Successfully",
        'data': data_array
    }

    return response







# def merge_function(lead_id: int, employee_id: str, db: Session):
#     data_array = []

#     # Fetch activity records
#     activity_records = db.query(ActivityCenter).filter(
#         ActivityCenter.admin_sales_id == lead_id,
#         ActivityCenter.employe_id == employee_id
#     ).all()

#     # Process activity records
#     for activity in activity_records:
#         admin_details = db.query(AdminSales).filter(AdminSales.id == activity.admin_sales_id).all()
#         employee_details = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == activity.employe_id).all()

#         temp = {
#             'Activity_details': activity,
#             'Lead_details': admin_details[0] if admin_details else [],
#             'Employee_details': employee_details
#         }

#         data_array.append(temp)

#     # Fetch meeting records
#     meeting_records = db.query(Meetingplanned).filter(
#         Meetingplanned.admin_sales_id == lead_id,
#         Meetingplanned.employe_id == employee_id
#     ).all()

#     # Process meeting records
#     for meeting in meeting_records:
#         admin_details = db.query(AdminSales).filter(AdminSales.id == meeting.admin_sales_id).all()
#         employee_details = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == meeting.employe_id).all()

#         temp = {
#             'Meeting_details': meeting,
#             'Lead_details': admin_details[0] if admin_details else [],
#             'Employee_details': employee_details
#         }

#         data_array.append(temp)

#     response = {
#         'status': 'true',
#         'message': "Data Received Successfully",
#         'data': data_array
#     }

#     return response
   

def update(activity_id:int,activity_center:ActivityCenter,db:Session):
    activity_center_update = activity_center.dict(exclude_unset=True)
    db.query(ActivityCenter).filter(ActivityCenter.id == activity_id).update(activity_center_update)
    db.commit()
    response = {'status': 'true','message':"Data Updated Successfully",'data':activity_center_update}
    return response

# def delete_activity(id: int, db: Session):
#     activity_center = db.query(ActivityCenter).filter(ActivityCenter.id == id).first()

#     if not activity_center:
#        {'status': 'false', 'message': "Activity Not Found"}

#     db.delete(activity_center)
#     db.commit()

#     response = {
#         'status': 'true',
#         'message': "Activity deleted successfully"
#     }
    
#     return response 



# def delete_activity(id: int, employe_id: str, db: Session):
#     try:
#         # Query for the activity that matches both id and employe_id
#         activity_center = db.query(ActivityCenter).filter(
#             ActivityCenter.id == id,
#             ActivityCenter.employe_id == employe_id
#         ).first()

#         # Check if the activity exists
#         if not activity_center:
#             return {
#                 'status': 'false',
#                 'message': "Activity not found"
#             }

#         # Delete the activity
#         db.delete(activity_center)
#         db.commit()  # Commit the transaction to persist changes

#         return {
#             'status': 'true',
#             'message': "Activity deleted successfully"
#         }

#     except SQLAlchemyError as e:
#         db.rollback()  # Rollback in case of an error
#         return {
#             'status': 'false',
#             'message': f"Error occurred: {str(e)}"
#         }



def delete_activity(id: int, created_by_type:Optional[str] ,  employe_id: Optional[str], db: Session):
    try:

        if  created_by_type and created_by_type.lower() == "admin":
            activity_center = db.query(ActivityCenter).filter(
                ActivityCenter.id == id,
                ActivityCenter.admin_emp_id == employe_id
            ).first()
        else:
            activity_center = db.query(ActivityCenter).filter(
                ActivityCenter.id == id,
                ActivityCenter.admin_emp_id == employe_id
            ).first()
        
        if not activity_center:
            return {
                'status': 'false',
                'message': f"Activity not found{id},Emp_id = {employe_id},Type = {created_by_type}"
            }
        del_ac = db.query(ActivityComment).filter(ActivityComment.activity_id == id).all()
        for ac in del_ac:
            db.delete(ac)
            db.commit()
            db.refresh(ac)
        
        db.delete(activity_center)
        db.commit() 

        return {
            'status': 'true',
            'message': "Activity deleted successfully"
        }

    except SQLAlchemyError as e:
        db.rollback()  
        return {
            'status': 'false',
            'message': f"Error occurred: {str(e)}"
        }

