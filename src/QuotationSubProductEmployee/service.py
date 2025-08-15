from sqlalchemy.orm import Session
from typing import Dict, List,Optional
from sqlalchemy import select
from sqlalchemy import desc
from fastapi import APIRouter, Depends, HTTPException, Header
from src.parameter import get_current_datetime
from src.QuotationSubProductEmployee.models import QuotationSubProductEmployeeCreate ,QuotationSubProductEmployee ,QuotationSubProductEmployeeRead , QuotationSubProductEmployeeDelete , QuotationSubProductAddRemark,QuotationSubProductQuantity
from src.CheckPoint.models import CheckPoint

def create(db: Session, quotation_SubProductcreate: QuotationSubProductEmployeeCreate):
    created = []
    skipped = []

    for item in quotation_SubProductcreate.sub_products:
        name = item.sub_product_name
        quantity = item.quantity

        existing = db.query(QuotationSubProductEmployee).filter(
            QuotationSubProductEmployee.product_id == quotation_SubProductcreate.product_id,
            QuotationSubProductEmployee.sub_product_name == name
        ).first()

        if existing:
            skipped.append(name)
            continue

        db_subpro = QuotationSubProductEmployee(
            admin_id=quotation_SubProductcreate.admin_id,
            emp_id=quotation_SubProductcreate.emp_id,
            product_id=quotation_SubProductcreate.product_id,
            sub_product_name=name,
            quantity=quantity
        )
        db.add(db_subpro)
        db.commit()
        db.refresh(db_subpro)

        created.append({
            "id": db_subpro.id,
            "admin_id": db_subpro.admin_id,
            "emp_id": db_subpro.emp_id,
            "product_id": db_subpro.product_id,
            "sub_product_name": db_subpro.sub_product_name,
            "quantity": db_subpro.quantity
        })

    return {
        "status": "true",
        "message": f"{len(created)} sub-product(s) created",
        "created_sub_products": created

    }









# def create(db: Session, quotation_SubProductcreate: QuotationSubProductEmployeeCreate):

#     existing = db.query(QuotationSubProductEmployee).filter(
#         QuotationSubProductEmployee.product_id == quotation_SubProductcreate.product_id,
#         QuotationSubProductEmployee.sub_product_name == quotation_SubProductcreate.sub_product_name
#     ).first()

#     if existing:
#         return {"status": "false", "message": "Sub-product with the same name already exists for this product."}

#     db_subpro = QuotationSubProductEmployee(
#         admin_id=quotation_SubProductcreate.admin_id,
#         emp_id=quotation_SubProductcreate.emp_id,
#         product_id=quotation_SubProductcreate.product_id,
#         sub_product_name=quotation_SubProductcreate.sub_product_name,
#     )

#     db.add(db_subpro)
#     db.commit()
#     db.refresh(db_subpro)

#     response = {
#         "status": "true",
#         "message": "SubProduct created successfully",
#         "data": {
#             "sub_product": db_subpro,
#         }
#     }
#     return response




# def get_subproducts_by_product_id(db: Session, quotation_SubProductRead: QuotationSubProductEmployeeRead):
#     db_subpro = db.query(QuotationSubProductEmployee).filter(
#         QuotationSubProductEmployee.product_id == quotation_SubProductRead.product_id
#     ).all()

#     if not db_subpro:
#         return {"status": "false", "message": "No sub-products found for the given product ID"}
    

#     checkpoint = db.query(CheckPoint).filter(CheckPoint.subproduct_id == db_subpro.id).all()

#     response = {
#         "status": "true",
#         "message": "Sub-products fetched successfully",
#         "count": len(db_subpro),
#         "data": db_subpro
#     }
#     return response


from src.QuotationProductEmployee.models import QuotationProductEmployee
from src.StoreManagerProduct.models import storeManagerProduct
from src.cre_upd_name import get_creator

def get_subproducts_by_product_id(db: Session, quotation_SubProductRead: QuotationSubProductEmployeeRead):
    if quotation_SubProductRead.product_id is not None:
        db_subpro = db.query(QuotationSubProductEmployee).filter(
            QuotationSubProductEmployee.product_id == quotation_SubProductRead.product_id
        ).all()
    if quotation_SubProductRead.product_code is not None:
        product = db.query(storeManagerProduct).filter(storeManagerProduct.item_code == quotation_SubProductRead.product_code).first()
        
        if not product:
            return {"status": f"{product.id}", "message": "No sub-products found for the given product code "}
        print("check",QuotationSubProductEmployee.product_id == f"{product.id}")
        db_subpro = db.query(QuotationSubProductEmployee).filter(
            QuotationSubProductEmployee.product_id == f"{product.id}"
        ).all()


        if not db_subpro:
            return {"status": "false", "message": "No sub-products found for the given product ID"}
            
    subproducts_with_checkpoints = []

    for subpro in db_subpro:
        creator_data = get_creator(subpro.admin_id, subpro.emp_id, db)
    

        checkpoints = db.query(CheckPoint).filter(CheckPoint.subproduct_id == subpro.id).all()
        subproducts_with_checkpoints.append({
            "subproduct": {**vars(subpro.copy()),"creator_info":creator_data},

            "checkpoints": checkpoints
        })

    response = {
        "status": "true",
        "message": "Sub-products with checkpoints fetched successfully",
        "count": len(subproducts_with_checkpoints),
        "data": subproducts_with_checkpoints
    }
    return response



def delete_subproduct_by_id(db: Session, subproduct_id: int):
    subproduct = db.query(QuotationSubProductEmployee).filter(
        QuotationSubProductEmployee.id == subproduct_id
    ).first()

    if not subproduct:
        raise HTTPException(status_code=404, detail="Sub-product not found")
    
    del_ac = db.query(CheckPoint).filter(CheckPoint.subproduct_id == subproduct.id).all()
    for ac in del_ac:
        db.delete(ac)
        db.commit()


    db.delete(subproduct)
    db.commit()

    return {
        "status": "true",
        "message": "SubProduct deleted successfully"
    }




def add_remark_byid(db: Session, addremark: QuotationSubProductAddRemark):
    subproduct = db.query(QuotationSubProductEmployee).filter(
        QuotationSubProductEmployee.id == addremark.subproduct_id
    ).first()

    if not subproduct:
        return {
            "status": "false",
            "message": "Sub-product not found"
        }

    subproduct.add_remark = addremark.add_remark

    db.add(subproduct)
    db.commit()
    db.refresh(subproduct)

    return {
        "status": "true",
        "message": "Remark added to SubProduct successfully"
    }



def add_quantity_byid(db: Session, quantity: QuotationSubProductQuantity):
    subproduct = db.query(QuotationSubProductEmployee).filter(
        QuotationSubProductEmployee.id == quantity.subproduct_id
    ).first()

    if not subproduct:
        return {
            "status": "false",
            "message": "Sub-product not found"
        }

    subproduct.quantity = quantity.quantity

    db.add(subproduct)
    db.commit()
    db.refresh(subproduct)

    return {
        "status": "true",
        "message": "Quantity Update successfully"
    }


