from sqlalchemy.orm import Session
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew
from datetime import datetime, timedelta
from src.AdminSales.models import AdminSales
from src.ProjectManagerOrder.models import ProjectManagerOrder
from src.AdminAddEmployee.models import AdminAddEmployee


# def login_admin(db: Session, email, password):
#     user_profile = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.email == email).first()

#     if not user_profile or not user_profile.email:
#         return {'status': 'false', 'message': 'Email is not registered'}

#     if user_profile.is_deleted:
#         return {'status': 'false', 'message': 'User cannot login because the account has been deleted by the Super Admin'}
    
#     if not user_profile.is_active:
#         return {'status': 'false', 'message': 'User cannot be login because the account has been deactivated by the Super Admin'}

#     if password == user_profile.password:
#         current_date = datetime.now()
#         expiration_date = user_profile.expiry_date

#         if expiration_date and expiration_date >= current_date:
#             return {'status': 'true', 'message': 'User Login Successfully', 'admin_id': user_profile.id}
#         else:
#             return {'status': 'false', 'message': 'Your plan has expired'}
#     else:
#         return {'status': 'false', 'message': 'Invalid Email And Password'}
def login_admin(db: Session, email, password):
    user_profile = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.email == email).first()

    if not user_profile or not user_profile.email:
        return {'status': 'false', 'message': 'Email is not registered'}

    if user_profile.is_deleted:
        return {'status': 'false', 'message': 'User cannot login because the account has been deleted by the Super Admin'}
    
    if not user_profile.is_active:
        return {'status': 'false', 'message': 'User cannot login because the account has been deactivated by the Super Admin'}

    if password == user_profile.password:
        current_date = datetime.now()
        expiration_date = user_profile.expiry_date

        if expiration_date and expiration_date >= current_date:
            return {
                'status': 'true',
                'message': 'User Login Successfully',
                'admin_id': user_profile.id,
                'company_name': user_profile.company_name ,
                'full_name': user_profile.full_name,  
            }
        else:
            return {'status': 'false', 'message': 'Your plan has expired'}
    else:
        return {'status': 'false', 'message': 'Invalid Email And Password'}

    
def show_admin_deshbord_count(admin_id: str, db: Session):
    total_data_count = db.query(AdminSales).filter(AdminSales.admin_id == admin_id).count()
    total_order_count = db.query(ProjectManagerOrder).filter(ProjectManagerOrder.admin_id == admin_id).count()
    total_employee_count = db.query(AdminAddEmployee).filter(AdminAddEmployee.admin_id == admin_id).count()

    response = {
        'status': 'true',
        'message': "Data Received Successfully",
        'total_lead': total_data_count,
        'total_orders': total_order_count,
        'total_employee': total_employee_count
    }
    
    return response    
