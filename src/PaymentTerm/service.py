from sqlalchemy.orm import Session
from src.PaymentTerm.models import PaymentTerm, PaymentTermCreate
from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.parameter import get_current_datetime



import os
import base64
import re
from datetime import datetime
import imghdr    
from datetime import datetime
import pytz

# def create_payment_term(db: Session, term_data: PaymentTermCreate) -> dict:
   
#     db_term = PaymentTerm(
#         admin_id=term_data.admin_id,
#         type=term_data.type,
#         file_path=term_data.file_path,
#         content=term_data.content
#     )
    
  
#     db.add(db_term)
#     db.commit()

    
#     db.refresh(db_term)

    
#     response = {
#         "status": "true",
#         "message": "Payment Term created successfully",
#         "data": db_term
#     }

#     return response
    
    
    

def save_base64_file(base64_str: str, filename: str) -> str:
    """Save a Base64 file to the 'uploads' directory and return the file path."""
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    file_path = os.path.join(upload_dir, filename)
    with open(file_path, "wb") as file:
        file.write(base64.b64decode(base64_str))

    return file_path

def create_payment_term(db: Session, term_data: PaymentTermCreate) -> dict:
    """Create a new payment term and save the file path from base64 data."""
    
    if term_data.type in ["Terms and Conditions", "Privacy Policy","Purchase Terms and Conditions"]:
        exist = db.query(PaymentTerm).filter(PaymentTerm.type == term_data.type , PaymentTerm.admin_id == str(term_data.admin_id)).first()
        if exist:
            return {"status": "false", "message": f"{term_data.type} Already Exist"}

    
    file_path = None
    if term_data.file_path:
        current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{current_datetime}_payment_term_{term_data.admin_id}.pdf"  # You can change extension as needed
        file_path = save_base64_file(term_data.file_path, filename)  # Save the file

        

    db_term = PaymentTerm(
        admin_id=term_data.admin_id,
        type=term_data.type,
        file_path=file_path,  # Use the saved file path
        content=term_data.content
    )

    db.add(db_term)
    db.commit()
    db.refresh(db_term)

    response = {
        "status": "true",
        "message": "Payment Term created successfully",
        "data": db_term
    }
    return response







def payment_term_by_admin_id(db: Session, admin_id: int) -> dict:
   
    db_terms = db.query(PaymentTerm).filter(PaymentTerm.admin_id == admin_id).order_by(desc(PaymentTerm.id)).all()

    if not db_terms:
        return{
            "status": "false",
            "message": "Payment Term not found for this admin id",
        }

    response = {
        "status": "true",
        "message": "Payment Term retrieved successfully",
        "data": db_terms
    }

    return response





# def update_term_and_condition(
#     db: Session,
#     admin_id: int,
#     term_and_condition_id: int,
#     new_data: dict
# ) -> dict:
    
#     term_and_condition = db.query(TermAndCondition).filter(
#         TermAndCondition.admin_id == admin_id,
#         TermAndCondition.id == term_and_condition_id
#     ).first()

#     if not term_and_condition:
#         return{
#             "status": "false",
#             "message": "Term and Condition not found",
#         }

    
#     for key, value in new_data.items():
#         if value is not None and hasattr(term_and_condition, key):
#             setattr(term_and_condition, key, value)

#     term_and_condition.updated_at = get_current_datetime()

    
#     db.commit()
#     db.refresh(term_and_condition)

#     return {
#         "id": term_and_condition.id,
#         "admin_id": term_and_condition.admin_id,
#         "type": term_and_condition.type,
#         "file_path": term_and_condition.file_path,
#         "content": term_and_condition.content,
#         "created_at": term_and_condition.created_at,
#         "updated_at": term_and_condition.updated_at
#     }



# def delete_term_and_condition(db: Session, admin_id: int, term_and_condition_id: int) -> bool:
    
#     term_and_condition = db.query(TermAndCondition).filter(
#         TermAndCondition.admin_id == admin_id,
#         TermAndCondition.id == term_and_condition_id
#     ).first()

#     if not term_and_condition:
#         return False

  
#     db.delete(term_and_condition)
#     db.commit()
#     return True