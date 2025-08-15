from typing import List,Optional
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from .models import SubCategoryCreate,SubCategory
from .service import create,get_all_sub_category,update,get_sub_category_by_admin_id,delete_sub_category_id,get_sub_category_list_by_admin
from src.parameter import get_token

router = APIRouter()

@router.get("/showAllSubCategory")
def read_all_Sub_Category_details(auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_all_sub_category(db=db)
        
@router.get("/showSubCategoryByAdmin/{admin_id}")
def read_Sub_Category_by_admin(admin_id:str, category_id: Optional[int] = None, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_sub_category_by_admin_id(db=db, admin_id=admin_id, category_id=category_id)
        
@router.get("/showSubCategoryListByAdmin/{admin_id}")
def read_sub_category_list_by_admin(admin_id:str, category_id: Optional[int] = None, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_sub_category_list_by_admin(db=db, admin_id=admin_id, category_id=category_id)        

@router.post("/createSubCategory")
def create_Sub_Category_details(sub_category: SubCategoryCreate,
                auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return create(db=db, sub_category=sub_category)
     
@router.put("updateSubCategory/{sub_category_id}")
def update_Sub_Category_details(sub_category_id:int,sub_category:SubCategoryCreate,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db:Session=Depends(get_db)):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return update(sub_category_id=sub_category_id,sub_category=sub_category,db=db)

@router.delete("/deleteSubCategory/{id}")
def delete_Sub_Category_details_by_id(id: int, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return delete_sub_category_id(id=id, db=db)