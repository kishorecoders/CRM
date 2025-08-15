# from fastapi import APIRouter, Depends, HTTPException, Header
# from sqlalchemy.orm import Session
# from src.database import get_db
# from src.parameter import get_token
# from typing import List
# from src.QuotationSubProductEmployee.models import QuotationSubProductEmployeeCreate , QuotationSubProductEmployeeRead ,QuotationSubProductEmployeeDelete ,QuotationSubProductAddRemark
# from src.QuotationSubProductEmployee.service import create , get_subproducts_by_product_id ,delete_subproduct_by_id , add_remark_byid

# router = APIRouter()


# @router.post("/add_sub_product")
# def create_quotation_details(
#     quotation_SubProductcreate: QuotationSubProductEmployeeCreate,
#     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#     db: Session = Depends(get_db)
# ):
    
#     if auth_token != get_token():
#         return {"status": "false", "message": "Unauthorized Request"}

    
#     return create(db=db, quotation_SubProductcreate=quotation_SubProductcreate)


# @router.post("/get_sub_product")
# def create_quotation_details(
#     quotation_SubProductRead: QuotationSubProductEmployeeRead,
#     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#     db: Session = Depends(get_db)
# ):
    
#     if auth_token != get_token():
#         return {"status": "false", "message": "Unauthorized Request"}

    
#     return get_subproducts_by_product_id(db=db, quotation_SubProductRead=quotation_SubProductRead)


# @router.post("/delete_subproduct")
# def delete_subproduct(
#     subproduct_id: QuotationSubProductEmployeeDelete, 
#     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#     db: Session = Depends(get_db)
# ):
#     if auth_token != get_token():
#         return {"status": "false", "message": "Unauthorized Request"}

#     return delete_subproduct_by_id(db=db, subproduct_id=subproduct_id.subproduct_id)


# @router.post("/add_remark")
# def add_remark(
#     addremark: QuotationSubProductAddRemark, 
#     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#     db: Session = Depends(get_db)
# ):
#     if auth_token != get_token():
#         return {"status": "false", "message": "Unauthorized Request"}

#     return add_remark_byid(db=db, addremark=addremark)


