from sqlalchemy.orm import Session
from src.TermAndConditions.models import TermAndCondition, TermAndConditionCreate
from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.parameter import get_current_datetime




# def create_term_and_condition(db: Session, term_data: TermAndConditionCreate) -> dict:
   
#     db_term = TermAndCondition(
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
#         "message": "Term and Condition created successfully",
#         "data": db_term
#     }

#     return response





import base64
import os
from src.TermAndConditionContent import models

def save_base64_file(base64_str: str, filename: str) -> str:
    """Save a Base64 file to the 'uploads' directory and return the file path."""
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    file_path = os.path.join(upload_dir, filename)
    with open(file_path, "wb") as file:
        file.write(base64.b64decode(base64_str))

    return file_path

def create_term_and_condition(db: Session, term_data: TermAndConditionCreate) -> dict:
    """Create a new payment term and save the file path from base64 data."""
    
    
    filename = f"payment_term_{term_data.admin_id}.pdf"  
    file_path = save_base64_file(term_data.file_path, filename)  

    db_term = TermAndCondition(
        admin_id=term_data.admin_id,
        type=term_data.type,
        file_path=file_path, 
        content=", ".join([item.content for item in term_data.content]) if term_data.content else ""
    )

    db.add(db_term)
    db.commit()

    contents = []
    for item in term_data.content:
        term_content = models.TermAndConditionContent(
            termAndCondition_id=db_term.id,
            content=item.content
        )

        db.add(term_content)
        db.commit()
        db.refresh(term_content)

        contents.append({
            "id": term_content.id,
            "termAndCondition_id": term_content.termAndCondition_id,
            "content": term_content.content,
            "created_at": term_content.created_at,
            "updated_at": term_content.updated_at,
        })

    db.refresh(db_term)

    response = {
        "status": "true",
        "message": "Payment Term created successfully",
        "data": {
            "term": db_term,  
            "content": contents if contents else None
        }
    }

    return response



# def get_all_term_and_conditions_by_admin_id(db: Session, admin_id: int) -> dict:
   
#     db_terms = db.query(TermAndCondition).filter(TermAndCondition.admin_id == admin_id).order_by(desc(TermAndCondition.id)).all()

#     if not db_terms:
#         return{
#             "status": "false",
#             "message": "Term and Condition not found for this admin id",
#         }

#     response = {
#         "status": "true",
#         "message": "Term and Conditions retrieved successfully",
#         "data": db_terms
#     }

#     return response



from src.TermAndConditionContent.models import TermAndConditionContent

def get_all_term_and_conditions_by_admin_id(db: Session, admin_id: int) -> dict:
    db_terms = (
        db.query(TermAndCondition)
        .filter(TermAndCondition.admin_id == admin_id)
        .order_by(desc(TermAndCondition.id))
        .all()
    )

    if not db_terms:
        return {
            "status": "false",
            "message": "Term and Condition not found for this admin id",
        }

    response_data = []
    for term in db_terms:
        term_contents = (db.query(TermAndConditionContent).filter(TermAndConditionContent.termAndCondition_id == term.id).all())

        term_dict = {
            "id": term.id,
            "admin_id": term.admin_id,
            "file_path": term.file_path,
            "contents": [
                {
                    "id": content.id,
                    "termAndCondition_id": content.termAndCondition_id,
                    "content": content.content,
                    "created_at": content.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": content.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
                for content in term_contents
            ]
        }
        response_data.append(term_dict)

    return {
        "status": "true",
        "message": "Term and Conditions retrieved successfully",
        "count": len(response_data),
        "data": response_data
    }




def update_term_and_condition(
    db: Session,
    admin_id: int,
    term_and_condition_id: int,
    new_data: dict
) -> dict:
    
    term_and_condition = db.query(TermAndCondition).filter(
        TermAndCondition.admin_id == admin_id,
        TermAndCondition.id == term_and_condition_id
    ).first()

    if not term_and_condition:
        return{
            "status": "false",
            "message": "Term and Condition not found",
        }

    
    for key, value in new_data.items():
        if value is not None and hasattr(term_and_condition, key):
            setattr(term_and_condition, key, value)

    term_and_condition.updated_at = get_current_datetime()

    
    db.commit()
    db.refresh(term_and_condition)

    return {
        "id": term_and_condition.id,
        "admin_id": term_and_condition.admin_id,
        "type": term_and_condition.type,
        "file_path": term_and_condition.file_path,
        "content": term_and_condition.content,
        "created_at": term_and_condition.created_at,
        "updated_at": term_and_condition.updated_at
    }



def delete_term_and_condition(db: Session, admin_id: int, term_and_condition_id: int) -> bool:
    
    term_and_condition = db.query(TermAndCondition).filter(
        TermAndCondition.admin_id == admin_id,
        TermAndCondition.id == term_and_condition_id
    ).first()

    if not term_and_condition:
        return False

  
    db.delete(term_and_condition)
    db.commit()
    return True