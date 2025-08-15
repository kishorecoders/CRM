from typing import List
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from .models import Category,CategoryCreate
from .service import create,get_all_category,update,get_category_by_admin_id,delete_category_id
from src.parameter import get_token
from typing import List, Optional

router = APIRouter()

@router.get("/showAllCategory")
def read_all_Category_details(auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_all_category(db=db)
        
# @router.get("/showCategoryByAdmin/{admin_id}/{type}")
# def read_Category_by_admin(admin_id:str, type:str,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#              db: Session = Depends(get_db)):
#         if auth_token != get_token():
#             return {"status": "false", "message": "Unauthorized Request"}
#         else:
#             return get_category_by_admin_id(admin_id=admin_id, type=type, db=db)


# @router.get("/showCategoryByAdmin/{admin_id}/{type}")
# def read_Category_by_admin(admin_id: str, type: str, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#                            db: Session = Depends(get_db)):
#     if auth_token != get_token():
#         return {"status": "false", "message": "Unauthorized Request"}
#     else:
#         return get_category_by_admin_id(admin_id=admin_id, type=type, db=db)




@router.get("/showCategoryByAdmin/{admin_id}/{type}")
def read_Category_by_admin(admin_id: str, type: str, emp_id: Optional[str] = None, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                           db: Session = Depends(get_db)):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    else:
        return get_category_by_admin_id(admin_id=admin_id, type=type, db=db , emp_id = emp_id)




# @router.post("/createCategory")
# def create_Category_details(catagory: CategoryCreate,
#                 auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#                 db: Session = Depends(get_db)):
#         if auth_token != get_token():
#             return {"status": "false", "message": "Unauthorized Request"}
#         else:
#             return create(db=db, catagory=catagory)
@router.post("/createCategory")
def create_Category_details(
    catagory: CategoryCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    
   
    return create(db=db, catagory=catagory)
     
@router.put("updateCategory/{category_id}")
def update_Category_details(category_id:int,catagory:CategoryCreate,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db:Session=Depends(get_db)):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return update(category_id=category_id,catagory=catagory,db=db)

@router.delete("/deleteCategory/{id}")
def delete_Category_details_by_id(id: int, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return delete_category_id(id=id, db=db)