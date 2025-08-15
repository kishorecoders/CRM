from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from src.database import get_db
from src.QuotationProduct.models import QuotationProductCreate,ProductQuery,QuotationProductCreateList,QuotationProduct,QuotationProductDeleteRequest,QuotationProductUpdate
from src.QuotationProduct.service import create,get_products_by_admin_and_template,create_multiple_products,update_quotation_product
from src.parameter import get_token

router = APIRouter()

@router.post("/create_quotation_product")
def create_quotation_product(
    quotation_product_create: QuotationProductCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
   
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

   
    return create(db=db, quotation_product_create=quotation_product_create)




@router.post("/get_products_by_admin_template")
def get_products(
    product_query: ProductQuery,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    
    result = get_products_by_admin_and_template(
        db=db,
        admin_id=product_query.admin_id,
        template_id=product_query.template_id
    )

    
    return result



@router.post("/create_quotation_products")
def create_multiple_quotation_products(
    product_list: QuotationProductCreateList,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    
    return create_multiple_products(db=db, products=product_list.products)



@router.post("/delete-quotation-product")
def delete_quotation_product(
    request: QuotationProductDeleteRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    product = db.query(QuotationProduct).filter(
        QuotationProduct.admin_id == request.admin_id,
        QuotationProduct.template_id == request.template_id,
        QuotationProduct.id == request.product_id
    ).first()

    if not product:
        return {"status": "false", "message": "Product not found"}
       # raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return {"status": "true", "message": "Product deleted successfully"}



@router.post("/quotation_product_update")
def update_product(
    update_data: QuotationProductUpdate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    
    updated_product = update_quotation_product(update_data, db)
    
    if isinstance(updated_product, dict):
        return updated_product

    return {"status": "true", "message": "Product updated successfully", "product": updated_product}
