from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from src.database import get_db
from src.TermAndConditions.models import TermAndConditionCreate,TermAndConditionRead,UpdateTermAndConditionRequest,TermAndConditionDelete
from src.TermAndConditions.service  import create_term_and_condition,get_all_term_and_conditions_by_admin_id,update_term_and_condition,delete_term_and_condition
from src.parameter import get_token

router = APIRouter()

@router.post("/create_term_and_condition")
def create_term_and_condition_api(
    term_data: TermAndConditionCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
   
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    
    
    return create_term_and_condition(db=db, term_data=term_data)




@router.post("/get_term_and_conditions_by_admin")
def get_all_term_and_conditions_by_admin_id_api(
    term_data: TermAndConditionRead, 
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
   
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    
    
    return get_all_term_and_conditions_by_admin_id(db=db, admin_id=term_data.admin_id)





@router.post("/update_term_and_condition")
def update_term_and_condition_api(
    term_data: UpdateTermAndConditionRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    
   
    updated_data = {
        "type": term_data.type,
        "file_path": term_data.file_path,
        "content": term_data.content
    }

   
    updated_record = update_term_and_condition(
        db=db,
        admin_id=term_data.admin_id,
        term_and_condition_id=term_data.term_and_condition_id,
        new_data=updated_data
    )
    
    return {"status": "true","message":"Term And Condition Update Successfully", "data": updated_record}




@router.post("/delete_term_and_condition")
def delete_term_and_condition_api(
    term_data: TermAndConditionDelete,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
  
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    
    
    success = delete_term_and_condition(
        db=db,
        admin_id=term_data.admin_id,
        term_and_condition_id=term_data.term_and_condition_id
    )
    
    if not success:
         return{
            "status": "false",
            "message": "Term and Condition not found",
        }
    
    return {"status": "true", "message": "Term and Condition deleted successfully"}