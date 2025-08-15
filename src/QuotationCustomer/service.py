from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status,HTTPException
from .models import QuotationCustomer,QuotationCustomerCreate,UpdateCustomerRequest,DeleteCustomerRequest
from sqlmodel import Session, select



def create(db: Session, customer: QuotationCustomerCreate):
   
    existing_customer_email = db.execute(
        select(QuotationCustomer).where(QuotationCustomer.email == customer.email)
    ).scalars().first()
    
    if existing_customer_email:
        return {
            'status': 'false',
            'message': "Email already exists. Please use a different email."
        }

    
    existing_customer_contact = db.execute(
        select(QuotationCustomer).where(QuotationCustomer.contact_number == customer.contact_number)
    ).scalars().first()
    
    if existing_customer_contact:
        return {
            'status': 'false',
            'message': "Contact number already exists. Please use a different number."
        }

    
    db_customer = QuotationCustomer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)

    return {
        'status': 'true',
        'message': "Customer Details Added Successfully",
        'data': db_customer
    }




def get_customers(db: Session, admin_id: str, employe_id: Optional[str] = None):
    query = select(QuotationCustomer).where(QuotationCustomer.admin_id == admin_id)

    if employe_id:
        query = query.where(QuotationCustomer.employe_id == employe_id)

    query = query.order_by(QuotationCustomer.id.desc()) 

    customers = db.execute(query).scalars().all()

    if not customers:
        return {
            'status': 'false',
            'message': "No customers found for the given criteria.",
            'data': []
        }

    return {
        'status': 'true',
        'message': "Customer List Retrieved Successfully",
        'data': customers
    }



def update_customer(db: Session, request: UpdateCustomerRequest):
    customer = db.execute(
        select(QuotationCustomer)
        .where(QuotationCustomer.admin_id == request.admin_id)
        .where(QuotationCustomer.id == request.customer_id)
    ).scalars().first()

    if not customer:
        return {
            'status': 'false',
            'message': "Customer not found.",
        }

    
    update_fields = request.dict(exclude_unset=True, exclude={"customer_id"})  

    for key, value in update_fields.items():
        if value is not None:
            setattr(customer, key, value)  

    customer.updated_at = datetime.utcnow()  
    db.add(customer)
    db.commit()
    db.refresh(customer)

    return {
        'status': 'true',
        'message': "Customer Details Updated Successfully",
        'data': customer
    }




def delete_customer(db: Session, request: DeleteCustomerRequest):
    customer = db.execute(
        select(QuotationCustomer)
        .where(QuotationCustomer.admin_id == request.admin_id)
        .where(QuotationCustomer.id == request.customer_id)
    ).scalars().first()

    if not customer:
        return {
            'status': 'false',
            'message': "Customer not found."
        }

    db.delete(customer) 
    db.commit()  

    return {
        'status': 'true',
        'message': "Customer Deleted Successfully"
    }
