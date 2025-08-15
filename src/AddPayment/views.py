from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from src.database import get_db
from src.Account.models import Account
from src.parameter import get_token
from src.Quotation.models import Quotation
from .models import PaymentRequest, PaymentRequestSchema , GetPaymentsAccount , EditPaymentRequest, DeletePaymentRequest # ✅ Use correct names
from src.QuotationProductEmployee.models import QuotationProductEmployee
from src.ProductDispatch.models import ProductDispatch
from sqlalchemy import func

from datetime import datetime
from src.Account.service import save_base64_file

router = APIRouter()




# @router.post("/create_payment")
# def create_payment(
#     request: PaymentRequestSchema,  
#     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#     db: Session = Depends(get_db)
# ):
#     """Create a payment record and update account balance."""
    
#     # ✅ Authentication check
#     if auth_token != get_token():
#         raise HTTPException(status_code=401, detail="Unauthorized Request")

#     if not request.product_id:
#         return {
#             "status": "false",
#             "message": "Product ID is required"
#         }

#     # ✅ Validate account existence
#     account = db.query(Account).filter(Account.id == request.account_id).first()
#     if not account:
#         return {
#             "status": "false",
#             "message": "Account not found"
#         }

#     # ✅ Validate quotation existence
#     quotation = db.query(Quotation).filter(Quotation.id == account.quote_id).first()
#     if not quotation:
#         return {
#             "status": "false",
#             "message": "Quotation not found for this account"
#         }

#     # ✅ Validate product existence
#     product = db.query(QuotationProductEmployee).filter(QuotationProductEmployee.id == request.product_id).first()
#     if not product:
#         return {
#             "status": "false",
#             "message": "Product not found"
#         }

#     # ✅ Convert received amount to integer and validate
#     try:
#         rcvd_amt_int = int(request.rcvd_amt)
#     except ValueError:
#         return {
#             "status": "false",
#             "message": "Invalid received amount format"
#         }

#     # # ✅ Fetch all dispatch records for the given account
#     # dispatch_records = db.query(Dispatch).filter(Dispatch.account_id == request.account_id).all()

#     # if not dispatch_records:
#     #     return {
#     #         "status": "false",
#     #         "message": "No dispatch record found for this account"
#     #     }

#     # # ✅ Dictionary to store total dispatch quantity per product
#     # dispatch_qty_per_product = {}

#     # # ✅ Sum `dc_qty` for each product_id
#     # for dispatch in dispatch_records:
#     #     product_id = dispatch.product_id
#     #     if product_id in dispatch_qty_per_product:
#     #         dispatch_qty_per_product[product_id] += int(dispatch.dc_qty)
#     #     else:
#     #         dispatch_qty_per_product[product_id] = int(dispatch.dc_qty)

#     # total_receivable = 0  # Initialize total receivable

#     # # ✅ Fetch rate per unit for each product and calculate total_receivable
#     # for product_id, total_dispatch_qty in dispatch_qty_per_product.items():
#     #     product = db.query(QuotationProductEmployee).filter(QuotationProductEmployee.id == product_id).first()
        
#     #     if not product:
#     #         continue  # Skip if product not found

#     #     try:
#     #         rate_per_unit = int(product.rate_per_unit)
#     #         total_receivable += total_dispatch_qty * rate_per_unit  # Sum up all products' receivables
#     #     except ValueError:
#     #         return { 
#     #             "message": f"Invalid rate per unit format for product ID {product_id}"
#     #         }

#     # ✅ Insert Payment record using `PaymentRequest`
#     new_payment = PaymentRequest(
#         account_id=request.account_id,
#         admin_id=request.admin_id,
#         emp_id=request.emp_id,
#         product_id=request.product_id,
#         rcvd_amt=rcvd_amt_int,  
#         payment_type=request.payment_type,
#         sent_by=request.sent_by,
#         handover_name=request.handover_name,
#         payment_date=request.payment_date,
#         bank_name=request.bank_name,
#         account_holder_name=request.account_holder_name,
#         branch_name=request.branch_name,
#         ifsc_code=request.ifsc_code,
#         ac_no=request.ac_no,
#         gst=request.gst
#     )
    
#     db.add(new_payment)
#     db.commit()
#     db.refresh(new_payment)

#     # # ✅ Update quotation details
#     # if quotation.total_received is None:
#     #     quotation.total_received = 0 
#     # else:
#     #     quotation.total_received = int(quotation.total_received)

#     # quotation.taxable_amount = "50"
#     # quotation.total_received += rcvd_amt_int  

#     # # ✅ Ensure total_receivable is stored as an integer
#     # if quotation.total_receivable is None:
#     #     quotation.total_receivable = 0  # Initialize as integer
#     # else:
#     #     quotation.total_receivable = int(quotation.total_receivable)  # Convert to int if stored as a string

#     # quotation.total_receivable = total_receivable  # ✅ Now addition will work properly

#     db.commit()
#     db.refresh(quotation)

#     return {
#         "status": "true",
#         "message": "Payment created successfully",
#         "payment_id": new_payment.id,
#     }







@router.post("/create_payment")
def create_payment(
    request: PaymentRequestSchema,  
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

   

    account = db.query(Account).filter(Account.id == request.account_id).first()
    if not account:
        return {
            "status": "false",
            "message": "Account not found"
        }

    quotation = db.query(Quotation).filter(Quotation.id == account.quote_id).first()
    if not quotation:
        return {
            "status": "false",
            "message": "Quotation not found for this account"
        }

    # product = db.query(QuotationProductEmployee).filter(QuotationProductEmployee.id == request.product_id).first()
    # # if not product:
    # #     return {
    # #         "status": "false",
    # #         "message": "Product not found"
    # #     }

    # # Calculate the total due amount (rate_per_unit * quantity)
    # total_due = product.rate_per_unit * product.quantity

    # # Query for the total amount already received for this product (related to the quotation)
    # total_received = db.query(func.sum(PaymentRequest.rcvd_amt)).filter(
    #     PaymentRequest.product_id == request.product_id,
    #     PaymentRequest.account_id == request.account_id
    # ).scalar() or 0

    # # Calculate remaining balance
    # remaining_balance = total_due - total_received

    # Check if the received amount is valid
    # Check if the received amount is valid
    # try:
    if not request.rcvd_amt:
        return {
            "status": "false",
            "message": "rcvd amount is required"
        }
    rcvd_amt_int = request.rcvd_amt
    # except ValueError:
    #     return {
    #         "status": "false",
    #         "message": "Invalid received amount format"
    #     }
    # if rcvd_amt_int > remaining_balance:
    #     return {
    #         "status": "false",
    #         "message": f"Received amount cannot exceed the remaining balance of {remaining_balance}"
    #     }

    file_path = None
    upi_file_path = None
    pdf_file_path= None

    if request.cheque_image:
        current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{current_datetime}_cheque_image_{request.admin_id}.jpg"
        file_path = save_base64_file(request.cheque_image, filename)

    if request.upi_image:
        current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{current_datetime}_upi_image_{request.admin_id}.jpg"
        upi_file_path = save_base64_file(request.upi_image, filename)

    if request.file_path:
        current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{current_datetime}_file_path_{request.admin_id}.pdf"
        pdf_file_path = save_base64_file(request.file_path, filename)


    new_payment = PaymentRequest(
        account_id=request.account_id,
        admin_id=request.admin_id,
        emp_id=request.emp_id,
        product_id=request.product_id,
        rcvd_amt=rcvd_amt_int,  
        payment_type=request.payment_type,
        sent_by=request.sent_by,
        handover_name=request.handover_name,
        payment_date=request.payment_date,
        bank_name=request.bank_name,
        account_holder_name=request.account_holder_name,
        branch_name=request.branch_name,
        ifsc_code=request.ifsc_code,
        ac_no=request.ac_no,
        gst=request.gst,
        
        payment_method_type=request.payment_method_type,  
        cheque_no=request.cheque_no,  
        cheque_date=request.cheque_date,  
        cheque_image=file_path,  
        upi_number_or_id=request.upi_number_or_id,  
        transaction_upi_id=request.transaction_upi_id,  
        upi_image=upi_file_path,
        file_path =pdf_file_path,
        note= request.note,
    )
    
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)


    rcvd_amt_float = float(rcvd_amt_int or 0)

    account.adavnce_amt = str(round(float(account.adavnce_amt or 0) + rcvd_amt_float, 2))

    if request.payment_type == "Cash":
        account.advance_cash = str(round(float(account.advance_cash or 0) + rcvd_amt_float, 2))
    else:
        account.advance_account = str(round(float(account.advance_account or 0) + rcvd_amt_float, 2))

    account.pending = str(round(float(account.pending or 0) - rcvd_amt_float, 2))

    db.commit()
    db.refresh(account)


    return {
        "status": "true",
        "message": "Payment created successfully",
    }






# @router.post("/create_payment")
# def create_payment(
#     request: PaymentRequestSchema,  # ✅ Use request schema
#     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#     db: Session = Depends(get_db)
# ):
#     """Create a payment record and update account balance."""
    
#     # ✅ Authentication check
#     if auth_token != get_token():
#         raise HTTPException(status_code=401, detail="Unauthorized Request")

#     if not request.product_id:
#         return {
#         "status": "false",
#         "message": "Product ID is required"
#     }
#     # ✅ Validate account existence
#     account = db.query(Account).filter(Account.id == request.account_id).first()
#     if not account:
#         return {
#         "status": "false",
#         "message": "Account not found"
#     }

#     # ✅ Validate quotation existence
#     quotation = db.query(Quotation).filter(Quotation.id == account.quote_id).first()
#     if not quotation:
#         return {
#         "status": "false",
#         "message": "Quotation not found for this account"
#     }

#     product = db.query(QuotationProductEmployee).filter(QuotationProductEmployee.id == request.product_id).first()


#     # ✅ Convert received amount to integer and validate
#     try:
#         rcvd_amt_int = int(request.rcvd_amt)
#     except ValueError:
#         return {
#         "status": "false",
#         "message": "Invalid received amount format"
#     }

#     # ✅ Insert Payment record using `PaymentRequest`
#     new_payment = PaymentRequest(
#         account_id=request.account_id,
#         admin_id=request.admin_id,
#         emp_id=request.emp_id,
#         product_id=request.product_id,
#         rcvd_amt=rcvd_amt_int,  # ✅ Convert amount to int
#         payment_type=request.payment_type,
#         sent_by=request.sent_by,
#         handover_name=request.handover_name,
#         payment_date=request.payment_date,
#         bank_name=request.bank_name,
#         account_holder_name=request.account_holder_name,
#         branch_name=request.branch_name,
#         ifsc_code=request.ifsc_code,
#         ac_no=request.ac_no
#     )
    
#     db.add(new_payment)
#     db.commit()
#     db.refresh(new_payment)

#     # ✅ Update account balance
#     # account.balance += rcvd_amt_int
#     db.commit()
#     db.refresh(account)

#     # ✅ Ensure total_received is stored as an integer
#     if quotation.total_received is None:
#         quotation.total_received = 0 
#     else:
#         quotation.total_received = int(quotation.total_received) 
#     quotation.taxable_amount = "50"
#     quotation.total_received += rcvd_amt_int  
#     db.commit()
#     db.refresh(quotation)


#     return {
#         "status": "true",
#         "message": "Payment created successfully",
#         "payment_id": new_payment.id,
       
#     }


@router.post("/get_payments_account")
def get_payments(
    request: GetPaymentsAccount,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    """Retrieve payment records with product details based on account ID."""
    
    # ✅ Authentication check
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    # ✅ Validate account existence
    account = db.query(Account).filter(Account.id == request.account_id).first()
    if not account:
        return {
            "status": "false",
            "message": "Account not found"
        }

    # ✅ Fetch all payments related to the account_id
    payment_records = db.query(PaymentRequest).filter(PaymentRequest.account_id == request.account_id).all()

    if not payment_records:
        return {
            "status": "false",
            "message": "No payment records found for this account"
        }

    # ✅ Fetch product details for each payment record
    payment_data = []
    for record in payment_records:
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
            "description": product.discription if product else "N/A",
        } if product else {}

        payment_data.append({
            "payment_id": record.id,
            "admin_id": record.admin_id,
            "emp_id": record.emp_id,
            "rcvd_amt": record.rcvd_amt,
            "payment_type": record.payment_type,
            "sent_by": record.sent_by,
            "handover_name": record.handover_name,
            "payment_date": record.payment_date,
            "bank_name": record.bank_name,
            "account_holder_name": record.account_holder_name,
            "branch_name": record.branch_name,
            "ifsc_code": record.ifsc_code,
            "ac_no": record.ac_no,
            "gst": record.gst,
            "created_at": record.created_at,  # Assuming `PaymentRequest` has a timestamp field
            "product_details": product_details,
            
            # Optional fields
            "payment_method_type": record.payment_method_type,
            "cheque_no": record.cheque_no,
            "cheque_date": record.cheque_date,
            "cheque_image": record.cheque_image,
            "upi_number_or_id": record.upi_number_or_id,
            "transaction_upi_id": record.transaction_upi_id,
            "upi_image": record.upi_image,
            "note": record.note,  
            "file_path": record.file_path,             
        })

    # ✅ Return response
    return {
        "status": "true",
        "message": "Payment records retrieved successfully",
        "payment_records": payment_data
    }
    
    
    
    
    
    
@router.post("/get_pi_value")
def get_payments(
    request: GetPaymentsAccount,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    account = db.query(Account).filter(Account.id == request.account_id).first()
    if not account:
        return {"status": "false", "message": "Account not found"}

    payment_records = db.query(PaymentRequest).filter(PaymentRequest.account_id == request.account_id).all()

    if not payment_records:
        return {"status": "false", "message": "No payment records found for this account"}

    product_total_map = {}
    for record in payment_records:
        product = db.query(QuotationProductEmployee).filter(
            QuotationProductEmployee.id == record.product_id
        ).first()

        if not product:
            continue  # Skip if no product found

        total = product.total if product else 0.0
        total_taxable_amount = product.rate_per_unit * product.quantity if product else 0.0

        # Initialize values
        cash_amount = on_account_amount = on_gst_amt = 0.0

        if record.payment_type == "Cash":
            cash_amount = record.rcvd_amt
        elif record.payment_type == "On Account":
            on_account_amount = record.rcvd_amt
            on_gst_amt = on_account_amount * 0.18  # Only GST amount (18% of on_account_amount)

        # ✅ Correct Percentage Calculation
        case_percent = (cash_amount / total_taxable_amount) * 100 if total_taxable_amount else 0.0
        billing_percent = (on_account_amount / total_taxable_amount) * 100 if total_taxable_amount else 0.0

        # Store/update product details
        if product.id not in product_total_map:
            product_total_map[product.id] = {
                "product_id": product.id,
                "product_name": product.product_name,
                "product_code": product.product_code,
                "hsn_code": product.hsn_code,
                "rate_per_unit": product.rate_per_unit,
                "quantity": product.quantity,
                "total": product.total,
                "gst_percentage": product.gst_percentage,
                "gross_total": product.gross_total,
                "availability": product.availability,
                "description": product.discription,
                "case_percent": case_percent,
                "billing_percent": billing_percent,
                "cash_amount": cash_amount,
                "on_account_amount": on_account_amount,
                "on_gst_amt": on_gst_amt,  # Only GST amount (18% of on_account_amount)
                "total_taxable_amount": total_taxable_amount
            }
        else:
            # Accumulate values if multiple payments exist
            product_total_map[product.id]["case_percent"] += case_percent
            product_total_map[product.id]["billing_percent"] += billing_percent
            product_total_map[product.id]["cash_amount"] += cash_amount
            product_total_map[product.id]["on_account_amount"] += on_account_amount
            product_total_map[product.id]["on_gst_amt"] += on_gst_amt

    return {
        "status": "true",
        "message": "PI values retrieved successfully",
        "product_details": list(product_total_map.values())  # Return single object per product
    }


@router.post("/edit_payment")
def edit_payment(
    request: EditPaymentRequest,  
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):

    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    payment = db.query(PaymentRequest).filter(PaymentRequest.id == request.payment_id).first()
    if not payment:
        return {
            "status": "false",
            "message": "Payment record not found"
        }

    account = db.query(Account).filter(Account.id == request.account_id).first()
    if not account:
        return {
            "status": "false",
            "message": "Account not found"
        }

    # ✅ Convert received amount to integer and validate
    try:
        rcvd_amt_int = int(request.rcvd_amt)
    except ValueError:
        return {
            "status": "false",
            "message": "Invalid received amount format"
        }

    # ✅ Update Payment record
    payment.account_id = request.account_id
    payment.admin_id = request.admin_id
    payment.emp_id = request.emp_id
    payment.product_id = request.product_id
    payment.rcvd_amt = rcvd_amt_int
    payment.payment_type = request.payment_type
    payment.sent_by = request.sent_by
    payment.handover_name = request.handover_name
    payment.payment_date = request.payment_date
    payment.bank_name = request.bank_name
    payment.account_holder_name = request.account_holder_name
    payment.branch_name = request.branch_name
    payment.ifsc_code = request.ifsc_code
    payment.ac_no = request.ac_no
    payment.gst = request.gst

    payment.gst = request.payment_method_type
    payment.cheque_no = request.cheque_no
    payment.cheque_date = request.cheque_date
    payment.cheque_image = request.cheque_image
    payment.upi_number_or_id = request.upi_number_or_id
    payment.transaction_upi_id = request.transaction_upi_id
    payment.upi_image = request.upi_image

    db.commit()
    db.refresh(payment)

    return {
        "status": "true",
        "message": "Payment updated successfully",
    }


@router.post("/delete_payment")
def delete_payment(
    request: DeletePaymentRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    """Delete a payment record using request body."""

    # ✅ Authentication check
    if auth_token != get_token():
        return {
            "status": "false",
            "message": "Unauthorized Request"
        }

    # ✅ Validate payment record existence
    payment = db.query(PaymentRequest).filter(PaymentRequest.id == request.payment_id).first()
    if not payment:
        return {
            "status": "false",
            "message": "Payment record not found"
        }

    # ✅ Delete the payment record
    db.delete(payment)
    db.commit()

    return {
        "status": "true",
        "message": "Payment deleted successfully",
    }

