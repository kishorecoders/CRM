from typing import List,Optional
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from src.StoreManagerService.models import storeManagerServiceCreate,storeManagerService
from src.StoreManagerService.service import create,get_all_service,update,delete_service_by_service_id,get_service_by_admin
from src.parameter import get_token

router = APIRouter()

@router.get("/showAllService")
def read_all_service_details(auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_all_service(db=db)
        
@router.get("/showServiceByAdmin/{admin_id}")
def read_service_by_admin(admin_id:str, search:Optional[str] = None, categories: Optional[str] = None, sub_categories: Optional[str] = None, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_service_by_admin(db=db, admin_id=admin_id, search=search, categories=categories, sub_categories=sub_categories)

@router.post("/createService")
def create_service_details(service_create: storeManagerServiceCreate,
                auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return create(db=db, service_create=service_create)
     
@router.put("updateService/{service_id}")
def update_service_details(service_id:int,service_details:storeManagerServiceCreate,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db:Session=Depends(get_db)):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return update(service_id=service_id,service_details=service_details,db=db)

@router.delete("/deleteService/{id}")
def delete_service_details_by_id(id: int, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return delete_service_by_service_id(id=id, db=db)