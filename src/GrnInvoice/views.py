from fastapi import APIRouter, Depends, Header
from sqlmodel import Session
from src.database import get_db
from src.GrnInvoice.models import GrnInvoiceCreate,GrnInvoiceUpdate,GrnInvoiceGetRequest,GrnInvoiceCreateExtended,GrnInvoiceStatusUpdateRequest,GrnInvoice
from src.GrnInvoice.service import create_grn_invoice,update_grn_invoice,get_grn_invoice_list
from src.parameter import get_token
from src.GrnOrders.models import GrnOrderIssue
from src.parameter import get_current_datetime

router = APIRouter()


# @router.post("/create_grn_invoice")
# def create_grn_invoice_api(
#     request: GrnInvoiceCreate,
#     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#     db: Session = Depends(get_db)
# ):
#     if auth_token != get_token():
#         return {"status": "false", "message": "Unauthorized Request"}

#     return create_grn_invoice(db=db, request=request)
        
    
    
@router.post("/create_grn_invoice")
def create_grn_invoice_api(
    request: GrnInvoiceCreateExtended,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    return create_grn_invoice(db=db, request=request)

    
    
    
    

@router.post("/update_grn_invoice")
def update_grn_invoice_api(
    request: GrnInvoiceUpdate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    return update_grn_invoice(db=db, request=request)
    
    
    
    
    
    
@router.post("/get_grn_invoice_list")
def fetch_grn_invoices(
    request: GrnInvoiceGetRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    return get_grn_invoice_list(db=db, request=request)
    
    
    
    
    
    
@router.post("/update_grn_invoice_status")
def update_grn_invoice_status(
    request: GrnInvoiceStatusUpdateRequest, 
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)):
    
    try:
        invoice = db.query(GrnInvoice).filter(GrnInvoice.id == request.id).first()

        if not invoice:
            return {"status": "false", "message": "GrnInvoice not found"}

        # Determine who is updating
        if request.employee_id:
            updated_by_type = "employee"
            updated_admin_emp_id = request.employee_id
        else:
            updated_by_type = "admin"
            updated_admin_emp_id = request.admin_id

        # Update invoice status
        invoice.status = "Paid"
        invoice.remark = request.remark
        invoice.updated_by_type = updated_by_type
        invoice.updated_admin_emp_id = updated_admin_emp_id
        invoice.updated_at = get_current_datetime()

        # Fetch the GRN Order
        grn_order = db.query(GrnOrderIssue).filter(GrnOrderIssue.id == request.grn_id).first()

        if grn_order:
            # Get all invoices for this GRN
            invoices = db.query(GrnInvoice).filter(
                GrnInvoice.grn_id == str(grn_order.id)
            ).all()

            # Check if all invoice statuses are "Paid"
            all_paid = all(inv.status == "Paid" for inv in invoices)

            if all_paid:
                grn_order.grn_status = "Invoiced"
                grn_order.updated_by_type = updated_by_type
                grn_order.updated_admin_emp_id = updated_admin_emp_id
                grn_order.updated_at = get_current_datetime()
        db.commit()

        return {
            "status": "true",
            "message": "Invoice status updated to Paid and GRN status updated to Invoiced"
        }

    except Exception as e:
        db.rollback()
        return {
            "status": "false",
            "message": f"Failed to update status: {str(e)}"
        }

