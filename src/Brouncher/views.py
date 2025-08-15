from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session
from src.database import get_db
from .models import BrouncherCreate,BrouncherRead,BrouncherDelete
from .service import create,get_all_brouncher_by_admin_id,delete_brouncher
from src.parameter import get_token

router = APIRouter()


@router.post("/create_brouncher")
def create_brouncher_details(brouncher_create: BrouncherCreate,
                           auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                           db: Session = Depends(get_db)):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    else:
        return create(db=db, brouncher_create=brouncher_create)
    



@router.post("/get_brouncher_by_admin")
def get_all_brouncher_by_admin_id_api(
    brouncher_data: BrouncherRead, 
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
   
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    
    
    return get_all_brouncher_by_admin_id(db=db, admin_id=brouncher_data.admin_id)




@router.post("/delete_brouncher")
def delete_brouncher_api(
    brouncher_data: BrouncherDelete,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    
    
    success = delete_brouncher(
        db=db,
        admin_id=brouncher_data.admin_id,
        brouncher_id=brouncher_data.brouncher_id
    )
    
    if not success:
        return {"status": "false", "message": "Brouncher not found"}
    
    return {"status": "true", "message": "Brouncher deleted successfully"}