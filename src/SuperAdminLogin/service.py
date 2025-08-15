from sqlmodel import Session
from datetime import datetime, timedelta
from src.SuperAdminBilling.models import SuperAdminBilling
from src.AdminAddEmployee.models import AdminAddEmployee
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew


class UserService:
    email = 'sphuritcrm@gmail.com'
    password = 'Sphurit@454545'
    auth_key = '2ec26ad9-e039-445e-915e-a482dc6f5e3b'

    @classmethod
    def login(cls, auth_key, email, password):
     header_key = cls.auth_key

     if auth_key != header_key:
        return {'status': 'false', 'message': 'Unauthorized Request'}

     if email == cls.email and password == cls.password:
        return {
            'status': 'true',
            'message': 'Login successful',
            'data': {'user': {'email': email}}
        }
     elif email != cls.email:
        return {'status': 'false', 'message': 'Invalid email'}
     elif password != cls.password:
        return {'status': 'false', 'message': 'Invalid password'}
     else:
        return {'status': 'false', 'message': 'Invalid email or password'}
     

from datetime import datetime
from sqlalchemy import extract
from sqlalchemy.orm import Session

def show_all_count(db: Session):
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year

    # All time counts
    total_data_count = db.query(SuperAdminUserAddNew).count()

    total_free_user = db.query(SuperAdminUserAddNew).filter(
        SuperAdminUserAddNew.amount == "0",
        SuperAdminUserAddNew.expiry_date >= current_date,
        SuperAdminUserAddNew.is_deleted != "1"
    ).count()

    total_billing = db.query(SuperAdminBilling).filter(
        SuperAdminBilling.amount_of_transection != "0"
    ).count()

    total_active_user = db.query(SuperAdminUserAddNew).filter(
        SuperAdminUserAddNew.expiry_date >= current_date,
        SuperAdminUserAddNew.amount != "0",
        SuperAdminUserAddNew.is_deleted != "1"
    ).count()

    total_employee = db.query(AdminAddEmployee).count()

    # Monthly counts (based on created_at)
    monthly_user = db.query(SuperAdminUserAddNew).filter(
        extract('month', SuperAdminUserAddNew.created_at) == current_month,
        extract('year', SuperAdminUserAddNew.created_at) == current_year
    ).count()

    monthly_free_user = db.query(SuperAdminUserAddNew).filter(
        SuperAdminUserAddNew.amount == "0",
        SuperAdminUserAddNew.expiry_date >= current_date,
        SuperAdminUserAddNew.is_deleted != "1",
        extract('month', SuperAdminUserAddNew.created_at) == current_month,
        extract('year', SuperAdminUserAddNew.created_at) == current_year
    ).count()

    monthly_billing = db.query(SuperAdminBilling).filter(
        SuperAdminBilling.amount_of_transection != "0",
        extract('month', SuperAdminBilling.created_at) == current_month,
        extract('year', SuperAdminBilling.created_at) == current_year
    ).count()

    monthly_active_user = db.query(SuperAdminUserAddNew).filter(
        SuperAdminUserAddNew.expiry_date >= current_date,
        SuperAdminUserAddNew.amount != "0",
        SuperAdminUserAddNew.is_deleted != "1",
        extract('month', SuperAdminUserAddNew.created_at) == current_month,
        extract('year', SuperAdminUserAddNew.created_at) == current_year
    ).count()

    monthly_employee = db.query(AdminAddEmployee).filter(
        extract('month', AdminAddEmployee.created_at) == current_month,
        extract('year', AdminAddEmployee.created_at) == current_year
    ).count()

    response = {
        'status': 'true',
        'message': "Data Received Successfully",
        'total_User': total_data_count,
        'total_Free_User': total_free_user,
        'total_billing': total_billing,
        'total_active_user': total_active_user,
        'total_employee': total_employee,
        'monthly_User': monthly_user,
        'monthly_Free_User': monthly_free_user,
        'monthly_billing': monthly_billing,
        'monthly_active_user': monthly_active_user,
        'monthly_employee': monthly_employee
    }

    return response

     