from typing import List,Optional
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from .models import GrnOrderProductRead,GrnOrderRemarkUpdateRequest, GrnOrderProductusedQty , UpdateGrnOrderProductusedQty
from .service import get
from src.parameter import get_token

router = APIRouter()

@router.post("/showGrnOrderProduct")
def read_all_grn_order_issue_details(
     order : GrnOrderProductRead,
     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get(db=db , order = order)
        




# @router.post("/update-grn-remark")
# def update_grn_remark(request: GrnOrderRemarkUpdateRequest, db: Session = Depends(get_db)):
#     grn_product = db.query(GrnOrderProduct).filter(GrnOrderProduct.id == request.id).first()

#     if not grn_product:
#         raise HTTPException(status_code=404, detail="GRN Order Product not found")

#     grn_product.remark = request.remark
#     grn_product.admin_id = request.admin_id
#     grn_product.employee_id = request.employee_id
#     grn_product.updated_at = get_current_datetime()

#     db.add(grn_product)
#     db.commit()
#     db.refresh(grn_product)

#     return {"status": "success", "message": "Remark updated successfully"}



from src.GrnOrderProduct.models import GrnOrderProduct
from src.GrnOrders.models import GrnOrderIssue
from src.PurchaseOrderIssue.models import PurchaseOrderIssue
from src.StoreManagerPurchase.models import StoreManagerPurchase
from src.ProjectManagerOrder.models import ProjectManagerOrder
from src.QuotationProductEmployee.models import QuotationProductEmployee
from src.StoreManagerProduct.models import storeManagerProduct
from src.Quotation.models import Quotation
from src.PurchaseOrderProduct.models import PurchaseOrderProduct
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy import cast, Integer ,func


@router.post("/get_product_quantity_by_grn")
def used_update(
    request: GrnOrderProductusedQty,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    
    result = []

    store_product  = db.query(storeManagerProduct).filter(storeManagerProduct.id== int(request.product_id)).first()
    if store_product :
            
        pur = db.query(PurchaseOrderProduct).filter(PurchaseOrderProduct.product_code==store_product.item_code).all()

        for pr in pur :
        
            products = db.query(GrnOrderProduct).filter(
                GrnOrderProduct.product_id == str(pr.id),
                cast(func.coalesce(GrnOrderProduct.accepted_quantity, 0), Integer) >
                cast(func.coalesce(GrnOrderProduct.used_quantity, 0), Integer)
            ).all()
            
            for product in products:
                data = product.__dict__.copy()
                grnorder = db.query(GrnOrderIssue).filter(
                    GrnOrderIssue.id == int(product.grn_order_id)
                ).first()

                sales_order_id = None

                if grnorder:
                    purchaseorder = db.query(PurchaseOrderIssue).filter(
                        PurchaseOrderIssue.id == int(grnorder.purchase_order_id)
                    ).first()

                    store_purchase = None
                    if purchaseorder and purchaseorder.purchase_request_id and str(purchaseorder.purchase_request_id).isdigit():
                        store_purchase = db.query(StoreManagerPurchase).filter(
                            StoreManagerPurchase.id == int(purchaseorder.purchase_request_id)
                        ).first()
                        
                    project_manager = None
                    if store_purchase:
                        project_manager = db.query(ProjectManagerOrder).filter(
                            ProjectManagerOrder.id == int(store_purchase.product_manager_id or 0)
                        ).first()

                        if project_manager:
                            if project_manager.status == "Won" and project_manager.quotation_id:
                                quotation_id = int(project_manager.quotation_id)
                                sale_order = db.query(Quotation).filter(Quotation.id == quotation_id).first()
                                if sale_order:
                                    sales_order_id = sale_order.pi_number
                            elif project_manager.status == "Manual":
                                sales_order_id = project_manager.manual_sale_order_id

                result.append({
                    "product": data,
                    "grnorder": grnorder,
                    "sales_order_id": sales_order_id,
                })

    
    return {
        "status": "true",
        "message": "Update successful",
        "data": result
    }



#######################################################################################################################################
@router.post("/update_product_quantity_by_grn")
def update_product_quantity_by_grn(
    request: UpdateGrnOrderProductusedQty,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    product = db.query(GrnOrderProduct).filter(
        GrnOrderProduct.admin_id == request.admin_id,
        GrnOrderProduct.id == int(request.grn_product_id)
    ).first()
    if not product:
        return {"status": "false", "message": "GRN product not found"}
    new_quantity = None
    try:
        accepted_quantity = int(product.accepted_quantity or 0)
        used_quantity = int(product.used_quantity or 0)
        new_quantity = str(accepted_quantity - used_quantity)
    except (ValueError, TypeError):
        return {"status": "false", "message": "Invalid quantity values"}

    product.used_quantity = str(int(product.used_quantity) + int(new_quantity))
    db.add(product)

    grnorder = db.query(GrnOrderIssue).filter(
        GrnOrderIssue.id == int(product.grn_order_id)
    ).first()
    if not grnorder:
        return {"status": "false", "message": "GRN Order not found"}

    purchaseorder = db.query(PurchaseOrderIssue).filter(
        PurchaseOrderIssue.id == int(grnorder.purchase_order_id)
    ).first()
    if not purchaseorder:
        return {"status": "false", "message": "Purchase Order not found"}

    store_purchase = db.query(StoreManagerPurchase).filter(
        StoreManagerPurchase.id == int(purchaseorder.purchase_request_id)
    ).first()
    if not store_purchase:
        return {"status": "false", "message": "Store Purchase not found"}

    if request.type == "Order":
        if store_purchase.request_type == "Order":
            project_manager = db.query(ProjectManagerOrder).filter(
                ProjectManagerOrder.id == int(store_purchase.product_manager_id)
            ).first()
            if project_manager:
                if project_manager.status == "Won":
                    Quotation_Product = db.query(QuotationProductEmployee).filter(
                        QuotationProductEmployee.id == int(store_purchase.product_id)
                    ).first()
                    if Quotation_Product:
                        Quotation_Product.manufacture_quantity = str(
                            int(Quotation_Product.manufacture_quantity) - int(new_quantity)
                        )
                        Quotation_Product.available_quantity = str(
                            int(Quotation_Product.available_quantity) + int(new_quantity)
                        )
                        db.add(Quotation_Product)


                elif project_manager.status == "Manual":
                    updated = False
                    for data in project_manager.product_id_and_quantity:
                        if str(data['product_id']) == str(store_purchase.product_id):
                            data['available_quantity'] = str(
                                int(data['available_quantity']) + int(new_quantity)
                            )
                            data['manufacture_quantity'] = str(
                                int(data['manufacture_quantity']) - int(new_quantity)
                            )
                            flag_modified(project_manager, "product_id_and_quantity")  # IMPORTANT
                            db.add(project_manager)
                            updated = True
                            break

                    if not updated:
                        print("Product not found in product_id_and_quantity")

        else:
            return {"status": "false", "message": "Request type mismatch"}
    else:
        store_Product = db.query(storeManagerProduct).filter(
            storeManagerProduct.id == int(store_purchase.product_id)
        ).first()
        if store_Product:
            store_Product.opening_stock = str(
                int(store_Product.opening_stock) + int(new_quantity)
            )
            db.add(store_Product)

    db.commit()
    return {
        "status": "true",
        "message": "Update successful",
    }




