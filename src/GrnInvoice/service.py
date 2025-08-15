from sqlmodel import Session
from src.GrnInvoice.models import GrnInvoice, GrnInvoiceCreate,GrnInvoiceUpdate,GrnInvoiceGetRequest,GrnInvoiceCreateExtended
from src.parameter import get_current_datetime
from src.GrnOrderProduct.models import GrnOrderProduct
from src.vendor.models import Vendor

from src.GrnOrders.models import GrnOrderIssue







def create_grn_invoice_old(db: Session, request: GrnInvoiceCreateExtended):
    if request.employee_id:
        created_by_type = "employee"
        admin_emp_id = request.employee_id
    else:
        created_by_type = "admin"
        admin_emp_id = request.admin_id

    invoice_data = request.dict(exclude={"products"})
    invoice_data["created_by_type"] = created_by_type
    invoice_data["admin_emp_id"] = admin_emp_id

    new_invoice = GrnInvoice(**invoice_data)
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)

    for item in request.products:
        product = db.query(GrnOrderProduct).filter(
            GrnOrderProduct.grn_order_id == request.grn_id,
            GrnOrderProduct.product_id == item.product_id
        ).first()

        if product:
            product.accepted_qty_by_invoice = item.accepted_qty_by_invoice
            product.rate = item.rate
            product.amount = item.amount
            product.updated_by_type = created_by_type
            product.updated_admin_emp_id = admin_emp_id
            product.updated_at = get_current_datetime()
            db.add(product)

   

    db.commit()

    return {
        "status": "true",
        "message": "Grn Invoice and associated products updated successfully"
    }



def create_grn_invoice(db: Session, request: GrnInvoiceCreateExtended):
    if request.employee_id:
        created_by_type = "employee"
        admin_emp_id = request.employee_id
    else:
        created_by_type = "admin"
        admin_emp_id = request.admin_id

    invoice_data = request.dict(exclude={"products"})
    invoice_data["created_by_type"] = created_by_type
    invoice_data["admin_emp_id"] = admin_emp_id

    new_invoice = GrnInvoice(**invoice_data)
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)

    for item in request.products:
        product = db.query(GrnOrderProduct).filter(
            GrnOrderProduct.grn_order_id == request.grn_id,
            GrnOrderProduct.product_id == item.product_id
        ).first()

        if product:
            product.accepted_qty_by_invoice = item.accepted_qty_by_invoice
            product.rate = item.rate
            product.amount = item.amount
            product.updated_by_type = created_by_type
            product.updated_admin_emp_id = admin_emp_id
            product.updated_at = get_current_datetime()
            db.add(product)

    # ? Update corresponding GRN Order status
    grn_order = db.query(GrnOrderIssue).filter(GrnOrderIssue.id == request.grn_id).first()
    if grn_order:
        grn_order.grn_status = "Invoice Created"
        grn_order.invoice_created = "1"
        grn_order.updated_by_type = created_by_type
        grn_order.updated_admin_emp_id = admin_emp_id
        grn_order.updated_at = get_current_datetime()
        db.add(grn_order)

    db.commit()

    return {
        "status": "true",
        "message": "Grn Invoice and associated products updated successfully"
    }








def update_grn_invoice(db: Session, request: GrnInvoiceUpdate):
    grn_invoice = db.query(GrnInvoice).filter(GrnInvoice.id == request.id).first()
    if not grn_invoice:
        raise HTTPException(status_code=404, detail="GRN Invoice not found")

    if request.employee_id:
        grn_invoice.updated_by_type = "employee"
        grn_invoice.updated_admin_emp_id = request.employee_id
    else:
        grn_invoice.updated_by_type = "admin"
        grn_invoice.updated_admin_emp_id = request.admin_id

    update_data = request.dict(exclude_unset=True, exclude={"id"})
    for key, value in update_data.items():
        setattr(grn_invoice, key, value)

    db.add(grn_invoice)
    db.commit()
    db.refresh(grn_invoice)

    return {
        "status": "true",
        "message": "GRN Invoice updated successfully"
        
    }
    
    
    
    
    
    
def get_grn_invoice_list(db: Session, request: GrnInvoiceGetRequest):
    query = db.query(GrnInvoice).filter(GrnInvoice.admin_id == request.admin_id)

    if request.employee_id:
        query = query.filter(GrnInvoice.employee_id == request.employee_id)
        
    if request.grn_id:
        query = query.filter(GrnInvoice.grn_id == request.grn_id)
        
        
    query1 = query.order_by(GrnInvoice.id.desc())

    invoice_list = query1.all()
    
    data = []

    for invoice in invoice_list:
        invoice_data = invoice.dict()

        # ? Fetch full vendor object using vendor_id
        vendor = db.query(Vendor).filter(Vendor.id == invoice.vendor_id).first()
        invoice_data["vendor"] = vendor

        data.append(invoice_data)

    return {
        "status": "true",
        "message": "Invoice list fetched successfully",
        "data": data
    }
