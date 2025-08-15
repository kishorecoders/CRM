from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from src.database import get_db
from src.Account.models import AccountCreate,AccountRequest,Account , AccountApprove
from src.Account.service  import create_account
from src.parameter import get_token
from src.Quotation.models import Quotation
from src.ProductDispatch.models import ProductDispatch,EditDispatchRequest, DeleteDispatch
from src.QuotationProductEmployee.models import QuotationProductEmployee
from pydantic import BaseModel


from src.Inventoryoutward.models import InventoryOutward
from pydantic import BaseModel
from fastapi import Query
from src.QuotationProductEmployee.models import QuotationProductEmployee
from src.AddPayment.models import PaymentRequest
from src.Bank.models import BankBase ,Bank
from src.cre_upd_name import get_creator_info



router = APIRouter()

@router.post("/create_account")
def create_account_api(
    account: AccountCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
   
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    
    
    return create_account(db=db, account=account)





@router.delete("/delete_account/{account_id}")
def delete_account(
    account_id: str,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    """Delete an account without affecting the quotation."""
    
    # ✅ Authentication check
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    # ✅ Find the account
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # ✅ Delete the account
    db.delete(account)
    db.commit()

    return {
        "status": "true",
        "message": "Account deleted successfully"
    }


@router.post("/get_account_details")
def get_account_details(
    request: AccountRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {
            "status": "false",
            "message": "Unauthorized Request",
        }

    query = db.query(Account).filter(Account.admin_id == request.admin_id)

    if request.employee_id:
        query = query.filter(Account.employee_id == request.employee_id)

    if request.account_id:
        # query = query.filter(Account.id == request.account_id , Account.acc_status == 1)
        query = query.filter(Account.id == request.account_id)


    #accounts = query.all()
    accounts = query.order_by(Account.id.desc()).all()

    if not accounts:
        return {
            "status": "false",
            "message": "No accounts found",
        }

    response_data = []

    for account in accounts:
        quotation = db.query(Quotation).filter(Quotation.id == account.quote_id).first()

        account_data = account.dict()
        account_data["quotation"] = quotation.dict() if quotation else None
        #response_data.append(account_data)
        created_by = None
        admin_emp_id = None

        if account.employee_id:
            created_by = "employee"
            admin_emp_id = account.employee_id
        else:
            created_by = "admin"
            admin_emp_id = account.admin_id

        created_by_data = get_creator_info(admin_emp_id,created_by,db)
        account_data["creator_info"] = created_by_data if created_by_data else {}

        products = []
        if quotation:
            products = db.query(QuotationProductEmployee).filter(QuotationProductEmployee.quote_id == quotation.id).all()

            data = []
            for pro in products:
                pro_data = pro.__dict__.copy()
                pro_data.pop("_sa_instance_state", None)  # Remove SQLAlchemy internal key

                invent = db.query(InventoryOutward).filter(
                    InventoryOutward.product_id == str(pro.id)
                ).first()

                if invent:
                    invent_data = invent.__dict__.copy()
                    invent_data.pop("_sa_instance_state", None)
                else:
                    invent_data = None

                pro_data["inventry"] = invent_data
                data.append(pro_data)

            bank_id = quotation.bank_detail  # This should store the bank_id (or any other unique identifier for BankBase)

            bank_details = db.query(Bank).filter(Bank.id == bank_id).first()  # Correctly using BankBase.id
            
            account_data["products"] = data
            
            if bank_details:
                account_data["bank_details"] = {
                    "admin_id": bank_details.admin_id,
                    "employee_id": bank_details.employee_id,
                    "bank_name": bank_details.bank_name,
                    "branch": bank_details.branch,
                    "account_number": bank_details.account_number,
                    "ifsc_code": bank_details.ifsc_code
                }

            response_data.append(account_data)

    # ✅ Initialize total payment tracking by account
    for account in accounts:
        cash_total = 0.0
        on_account_total = 0.0

        # Fetch payments only for the current account
        payments_for_account = db.query(PaymentRequest).filter(PaymentRequest.account_id == account.id).all()

        if payments_for_account:
            # Segregate amounts based on payment type for this specific account
            for payment in payments_for_account:
                if payment.payment_type == "Cash":
                    cash_total += float(payment.rcvd_amt or 0)  # Convert to float safely
                elif payment.payment_type == "On Account":
                    on_account_total += float(payment.rcvd_amt or 0)  # Convert to float safely

            # ✅ Update Quotation Table (Cash Balance + On Account Balance)
            quotation = db.query(Quotation).filter(Quotation.id == account.quote_id).first()
            if quotation:
                # Update the quotation for the current account with the calculated totals
                quotation.cash_balance = str(cash_total)  # Convert back to str
                quotation.account_balance = str(on_account_total)  # Convert back to str

                db.commit()
                db.refresh(quotation)
       
    for account in accounts:
        quotation = db.query(Quotation).filter(Quotation.id == account.quote_id).first()

        total_amount = float(quotation.total_amount or 0)
        gst = float(quotation.gst or 0)
        advance_amt = float(account.adavnce_amt or 0)

        taxable = total_amount - gst
        pending = taxable - advance_amt

        account.pending = str(round(pending, 2))
        db.commit()
        db.refresh(account)


    # ✅ Return response with account details and balances
    return {
        "status": "true",
        "message": "Account details retrieved successfully",
        "data": response_data
    }



@router.post("/get_account_details_copy")
def get_account_details_copy(
    request: AccountRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {
            "status": "false",
            "message": "Unauthorized Request",
        }

    query = db.query(Account).filter(Account.admin_id == request.admin_id)

    if request.employee_id:
        query = query.filter(Account.employee_id == request.employee_id)

    if request.account_id:
        # query = query.filter(Account.id == request.account_id , Account.acc_status == 1)
        query = query.filter(Account.id == request.account_id)


    #accounts = query.all()
    accounts = query.order_by(Account.id.desc()).all()

    if not accounts:
        return {
            "status": "false",
            "message": "No accounts found",
        }

    response_data = []

    for account in accounts:
        quotation = db.query(Quotation).filter(Quotation.id == account.quote_id).first()

        account_data = account.dict()
        account_data["quotation"] = quotation.dict() if quotation else None
        #response_data.append(account_data)

        products = []
        if quotation:
            products = db.query(QuotationProductEmployee).filter(QuotationProductEmployee.quote_id == quotation.id).all()

            bank_id = quotation.bank_detail  # This should store the bank_id (or any other unique identifier for BankBase)

            bank_details = db.query(Bank).filter(Bank.id == bank_id).first()  # Correctly using BankBase.id
            
            account_data["products"] = [product.dict() for product in products]
            
            if bank_details:
                account_data["bank_details"] = {
                    "admin_id": bank_details.admin_id,
                    "employee_id": bank_details.employee_id,
                    "bank_name": bank_details.bank_name,
                    "branch": bank_details.branch,
                    "account_number": bank_details.account_number,
                    "ifsc_code": bank_details.ifsc_code
                }

            response_data.append(account_data)

    # ✅ Initialize total payment tracking by account
    for account in accounts:
        cash_total = 0.0
        on_account_total = 0.0

        # Fetch payments only for the current account
        payments_for_account = db.query(PaymentRequest).filter(PaymentRequest.account_id == account.id).all()

        if payments_for_account:
            # Segregate amounts based on payment type for this specific account
            for payment in payments_for_account:
                if payment.payment_type == "Cash":
                    cash_total += float(payment.rcvd_amt or 0)  # Convert to float safely
                elif payment.payment_type == "On Account":
                    on_account_total += float(payment.rcvd_amt or 0)  # Convert to float safely

            # ✅ Update Quotation Table (Cash Balance + On Account Balance)
            quotation = db.query(Quotation).filter(Quotation.id == account.quote_id).first()
            if quotation:
                # Update the quotation for the current account with the calculated totals
                quotation.cash_balance = str(cash_total)  # Convert back to str
                quotation.account_balance = str(on_account_total)  # Convert back to str

                db.commit()
                db.refresh(quotation)
       
    for account in accounts:
        quotation = db.query(Quotation).filter(Quotation.id == account.quote_id).first()

        total_amount = float(quotation.total_amount or 0)
        gst = float(quotation.gst or 0)
        advance_amt = float(account.adavnce_amt or 0)

        taxable = total_amount - gst
        pending = taxable - advance_amt

        account.pending = str(round(pending, 2))
        db.commit()
        db.refresh(account)


    # ✅ Return response with account details and balances
    return {
        "status": "true",
        "message": "Account details retrieved successfully",
        "data": response_data
    }




@router.post("/approve_quotation_status")
def approve_quotation(
    request: AccountApprove,

    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    # ✅ Authentication check
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    account = db.query(Account).filter(Account.id == request.account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    quotation = db.query(Quotation).filter(Quotation.id == account.quote_id).first()
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found for this account")

    # ✅ Status validation (0 = Canceled, 1 = Pending, 2 = Approved)
    if request.status not in [0, 1, 2]:
        raise HTTPException(status_code=400, detail="Invalid status. Use 0 for Canceled, 1 for Pending, or 2 for Approved.")
    
    # ✅ Update quotation status
    quotation.status = request.status

    if request.status ==  0:
        quotation.quotation_status = 2

    if request.status ==  2:
        quotation.quotation_status = 3

    if request.status in [0, 1]:
        account.acc_status = request.status
        if request.add_note or request.select_remark:
            account.add_note = request.add_note
            account.select_remark = request.select_remark
        else:
            account.add_note = ""
            account.select_remark = ""
        
        
        
        #if request.status == 1:
            #account.add_note = request.add_note
            #account.select_remark = request.select_remark
        #else:
          #  account.add_note = ""
          #  account.select_remark = ""


    if request.status == 0:
        # Canceled - reset balances
        quotation.cash_balance = 0
        quotation.account_balance = 0

    db.commit()
    db.refresh(quotation)

    return {
        "status": "true",
        "message": f"Quotation  successfully",
        "data": {
            "id": quotation.id,
            "status": quotation.status,
            "data": quotation.dict()
        }
    }




@router.put("/approve_quotation_status/{account_id}")
def approve_quotation(
    account_id: str,
    status: int ,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    # ✅ Authentication check
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    quotation = db.query(Quotation).filter(Quotation.id == account.quote_id).first()
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found for this account")

    # ✅ Status validation (0 = Canceled, 1 = Pending, 2 = Approved)
    if status not in [0, 1, 2]:
        raise HTTPException(status_code=400, detail="Invalid status. Use 0 for Canceled, 1 for Pending, or 2 for Approved.")
    
    # ✅ Update quotation status
    quotation.status = status

    if status in [0, 1]:
        account.acc_status = status

    if status == 0:
        # Canceled - reset balances
        quotation.cash_balance = 0
        quotation.account_balance = 0

    db.commit()
    db.refresh(quotation)

    return {
        "status": "true",
        #"message": f"Quotation {'pending' if status == 1 else 'approved' if status == 2 else 'canceled'} successfully",
        "message": "Status Updated successfully",
        "data": {
            "id": quotation.id,
            "status": quotation.status,
            "data": quotation.dict()
        }
    }








class InvoiceRequest(BaseModel):
    admin_id: str
    emp_id: str
    invoice_file: str
    invoice_number: str
    account_id: str

@router.post("/add_invoice")
def add_invoice(
    request: InvoiceRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    # Authorization check
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    # Fetch Account based on request data
    query = db.query(Account).filter(Account.admin_id == request.admin_id)

    if request.emp_id:
        query = query.filter(Account.employee_id == request.emp_id)
    
    if request.account_id:
        query = query.filter(Account.id == request.account_id)
    
    account = query.first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # Find Quotation linked to this account
    quotation = db.query(Quotation).filter(Quotation.id == account.quote_id).first()

    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found for this account")

    # Update the quotation with invoice details
    quotation.invoice_number = request.invoice_number
    quotation.invoice_file = request.invoice_file

    # Commit the changes to the database
    db.commit()
    db.refresh(quotation)

    return {
        "status": "true",
        "message": "Invoice added successfully to the quotation",
        "data": quotation.dict()
    }


@router.put("/send_invoice/{account_id}")
def send_invoice(
    account_id: str,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    # Authorization check
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    # Find Account by account_id
    account = db.query(Account).filter(Account.id == account_id).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # Find the Quotation linked to this account
    quotation = db.query(Quotation).filter(Quotation.id == account.quote_id).first()

    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found for this account")

    # Update invoice_status to 1 (sent/approved)
    quotation.invoice_status = 1  # Sent/Approved status

    # Commit the changes to the database
    db.commit()
    db.refresh(quotation)

    return {
        "status": "true",
        "message": "Invoice status updated to sent successfully",
        "data": quotation.dict()
    }



@router.get("/get-products/{account_id}") 
def get_products( 
    account_id: str,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    # ✅ Authentication check
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    # ✅ Find the account
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # ✅ Find the related quotation
    quotation = db.query(Quotation).filter(Quotation.id == account.quote_id).first() 
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found for this account")

    
    # ✅ Fetch related products from QuotationProductEmployee
    products = db.query(QuotationProductEmployee).filter(
        QuotationProductEmployee.quote_id == quotation.id
    ).all()

    data = []
    for pro in products:
        pro_data = pro.__dict__.copy()  # Safely copy the data
        invent = db.query(InventoryOutward).filter(
            InventoryOutward.product_id == str(pro.id)
        ).first()
        pro_data["inventry"] = invent
        data.append(pro_data)

    return {
        "status": "true",
        "message": "Products fetched successfully",
        "products": data
    }
    
    
    


# ✅ Request Model
class DispatchRequest(BaseModel):
    account_id: str
    admin_id: str = ""
    emp_id: str = ""
    dc_no: str = ""
    dc_qty: str = ""
    dispatch_qty: str = ""
    balance_qty: str = ""
    product_id: str = ""


@router.post("/create_dispatch")
def create_dispatch(
    request: DispatchRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    """Create a dispatch record and update product quantity."""
    
    # ✅ Authentication check
    if auth_token != get_token():
        return {
        "status": "false",
        "message": "Unauthorized Request"
    }
        #raise HTTPException(status_code=401, detail="Unauthorized Request")
    
    if not request.product_id:
        return {
        "status": "false",
        "message": "Product ID is required"
    }

    # ✅ Validate account existence
    account = db.query(Account).filter(Account.id == request.account_id).first()
    if not account:
        return {
        "status": "false",
        "message": "Account not found"
    }
        #raise HTTPException(status_code=404, detail="Account not found")

    # ✅ Find the related quotation
    quotation = db.query(Quotation).filter(Quotation.id == account.quote_id).first() 
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found for this account")

    # ✅ Fetch the related product
    product = db.query(QuotationProductEmployee).filter(
        QuotationProductEmployee.quote_id == quotation.id,
        QuotationProductEmployee.id == request.product_id
    ).first()

    if not product:
        return {
        "status": "false",
        "message": "Product not found in quotation"
    }
        #raise HTTPException(status_code=404, detail="Product not found in quotation")

    # ✅ Convert dc_qty to integer and validate
    try:
        dc_qty_int = int(request.dc_qty)
    except ValueError:
        return {
        "status": "false",
        "message": "Invalid DC quantity format"
    }
        #raise HTTPException(status_code=400, detail="Invalid DC quantity format")

    if dc_qty_int > product.quantity:
        return {
        "status": "false",
        "message": "DC quantity exceeds available stock"
    }
        #raise HTTPException(status_code=400, detail="DC quantity exceeds available stock")

    # ✅ Insert Dispatch record
    new_dispatch = ProductDispatch(
        account_id=request.account_id,
        admin_id=request.admin_id,
        emp_id=request.emp_id,
        dc_no=request.dc_no,
        dc_qty=request.dc_qty,
        dispatch_qty=request.dispatch_qty,
        balance_qty=request.balance_qty,
        product_id=request.product_id
    )
    
    db.add(new_dispatch)
    db.commit()
    db.refresh(new_dispatch)

    # ✅ Subtract DC quantity from product quantity
    product.quantity -= dc_qty_int  # ✅ Update quantity
    db.commit()
    db.refresh(product)


    return {
        "status": "true",
        "message": "Dispatch created successfully",
        "dispatch_id": new_dispatch.id,
        "new_product_quantity": product.quantity
    }
    
    
    
    


# ✅ Request Model
class Get_dispatch_account(BaseModel):
    account_id: str

@router.post("/get_dispatch_account")
def get_dispatch_account(
    request: Get_dispatch_account,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    """Retrieve dispatch records with product details based on account ID."""
    
    # ✅ Authentication check
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    # ✅ Validate account existence
    account = db.query(Account).filter(Account.id == request.account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # ✅ Fetch all dispatch records related to the account_id
    dispatch_records = db.query(ProductDispatch).filter(ProductDispatch.account_id == request.account_id).all()

    if not dispatch_records:
        return {
            "status": "false",
            "message": "No dispatch records found for this account"
        }

    # ✅ Fetch product details for each dispatch record
    dispatch_data = []
    for record in dispatch_records:
        product = db.query(QuotationProductEmployee).filter(
            QuotationProductEmployee.id == record.product_id
        ).first()

        product_details = {
            "product_id": record.product_id,
            "product_name": product.product_name if product else "N/A",
            "product_code": product.product_code if product else "N/A",
            "hsn_code": product.hsn_code if product else "N/A",
            "rate_per_unit": product.rate_per_unit if product else 0.0,
            "quantity": product.quantity if product else 0,
            "total": product.total if product else 0.0,
            "gst_percentage": product.gst_percentage if product else 0.0,
            "gross_total": product.gross_total if product else 0.0,
            "availability": product.availability if product else "N/A",
            "availability": product.discription if product else "N/A",
        } if product else {}

        dispatch_data.append({
            "dispatch_id": record.id,
            "admin_id": record.admin_id,
            "emp_id": record.emp_id,
            "dc_no": record.dc_no,
            "dc_qty": record.dc_qty,
            "dispatch_qty": record.dispatch_qty,
            "balance_qty": record.balance_qty,
            "created_at": record.created_at,  # Assuming Dispatch model has a timestamp field
            "product_details": product_details
        })

    # ✅ Return response
    return {
        "status": "true",
        "message": "Dispatch records retrieved successfully",
        "dispatch_records": dispatch_data
    }







@router.post("/edit_dispatch")
def edit_dispatch(
    request: EditDispatchRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    """Edit an existing dispatch record and update product quantity accordingly."""

    # ✅ Authentication check
    if auth_token != get_token():
        return {
            "status": "false",
            "message": "Unauthorized Request"
        }

    dispatch = db.query(ProductDispatch).filter(ProductDispatch.id == request.dispatch_id).first()
    if not dispatch:
        return {
            "status": "false",
            "message": "Dispatch record not found"
        }

    product = db.query(QuotationProductEmployee).filter(
        QuotationProductEmployee.id == dispatch.product_id
    ).first()

    if not product:
        return {
            "status": "false",
            "message": "Product not found in quotation"
        }

    
    try:
        dc_qty_int = int(request.dc_qty)
    except ValueError:
        return {
            "status": "false",
            "message": "Invalid DC quantity format"
        }

    
    product.quantity += int(dispatch.dc_qty)  

    if dc_qty_int > product.quantity:
        return {
            "status": "false",
            "message": "DC quantity exceeds available stock"
        }

    product.quantity -= dc_qty_int 

    
    dispatch.account_id = request.account_id
    dispatch.admin_id = request.admin_id
    dispatch.emp_id = request.emp_id
    dispatch.dc_no = request.dc_no
    dispatch.dc_qty = request.dc_qty
    dispatch.dispatch_qty = request.dispatch_qty
    dispatch.balance_qty = request.balance_qty
    dispatch.product_id = request.product_id

    db.commit()
    db.refresh(dispatch)
    db.refresh(product)

    return {
        "status": "true",
        "message": "Dispatch updated successfully"
    
    }




@router.post("/delete_dispatch")
def delete_dispatch(
    request: DeleteDispatch,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):

    # ✅ Authentication check
    if auth_token != get_token():
        return {
            "status": "false",
            "message": "Unauthorized Request"
        }

    dispatch = db.query(ProductDispatch).filter(ProductDispatch.id == request.dispatch_id).first()
    if not dispatch:
        return {
            "status": "false",
            "message": "Dispatch record not found"
        }

    product = db.query(QuotationProductEmployee).filter(
        QuotationProductEmployee.id == dispatch.product_id
    ).first()

    if not product:
        return {
            "status": "false",
            "message": "Product not found in quotation"
        }

    product.quantity += int(dispatch.dc_qty)

    db.delete(dispatch)
    db.commit()
    db.refresh(product)

    return {
        "status": "true",
        "message": "Dispatch deleted successfully",
    }









    
    






