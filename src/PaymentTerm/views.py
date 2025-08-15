from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from src.database import get_db
from src.PaymentTerm.models import PaymentTermCreate,PaymentTermRead ,PaymentTermDelete ,PaymentTerm
from src.PaymentTerm.service  import create_payment_term,payment_term_by_admin_id
from src.parameter import get_token

router = APIRouter()

@router.post("/create_payment_term")
def create_term_and_condition_api(
    term_data: PaymentTermCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
   
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    
    
    return create_payment_term(db=db, term_data=term_data)




@router.post("/get_payment_term_by_admin")
def get_all_payment_term_by_admin_id_api(
    term_data: PaymentTermRead, 
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
   
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    
    
    return payment_term_by_admin_id(db=db, admin_id=term_data.admin_id)





# @router.post("/update_term_and_condition")
# def update_term_and_condition_api(
#     term_data: UpdateTermAndConditionRequest,
#     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#     db: Session = Depends(get_db)
# ):
    
#     if auth_token != get_token():
#         raise HTTPException(status_code=401, detail="Unauthorized Request")
    
   
#     updated_data = {
#         "type": term_data.type,
#         "file_path": term_data.file_path,
#         "content": term_data.content
#     }

   
#     updated_record = update_term_and_condition(
#         db=db,
#         admin_id=term_data.admin_id,
#         term_and_condition_id=term_data.term_and_condition_id,
#         new_data=updated_data
#     )
    
#     return {"status": "true","message":"Term And Condition Update Successfully", "data": updated_record}



@router.post("/delete_payment_term")
def delete_term_and_condition_api(
    term_data: PaymentTermDelete,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    # Check token
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    # Get the actual record
    term = db.query(PaymentTerm).filter(
        PaymentTerm.admin_id == term_data.admin_id,
        PaymentTerm.id == term_data.payment_term_id,
    ).first()

    if not term:
        return {
            "status": "false",
            "message": "Payment Term not found",
        }

    # Delete and commit
    db.delete(term)
    db.commit()

    return {"status": "true", "message": "Payment Term deleted successfully"}



from src.PaymentTerm.models import UpdatePaymentTermRequest
from .service import save_base64_file
from datetime import datetime
import pytz

@router.post("/update_payment_term")
def update_payment_term_api(
    term_data: UpdatePaymentTermRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    term = db.query(PaymentTerm).filter(
        PaymentTerm.admin_id == term_data.admin_id,
        PaymentTerm.id == term_data.payment_term_id,
    ).first()

    if not term:
        return {
            "status": "false",
            "message": "Payment Term not found",
        }

    file_path = None
    # Update fields if provided
    if term_data.file_path is not None:
        current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{current_datetime}_payment_term_{term_data.admin_id}.pdf"  # You can change extension as needed
        file_path = save_base64_file(term_data.file_path, filename)  # Save the file

        term.file_path = file_path if term_data.file_path else term.file_path
        
    if term_data.content is not None:
        term.content = term_data.content if term_data.content else term.content

    db.commit()
    db.refresh(term)

    return {
        "status": "true",
        "message": "Payment Term updated successfully",
        "data": term

    }


