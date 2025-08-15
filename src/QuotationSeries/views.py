from typing import List
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from .models import QuotationSeriesCreate,QuotationSeriesRequest,QuotationSeriesUpdateRequest,QuotationSeriesDeleteRequest,QuotationSeries,QuotationSeriesDetailRequest
from .service import create,get_series,update_series,delete_series
from src.parameter import get_token
from sqlmodel import Session, select
from src.Quotation.models import Quotation
from src.GrnInvoice.models import GrnInvoice
from src.Rfq.models import Rfq


router = APIRouter()



@router.post("/create_series")
def create_series_details(series: QuotationSeriesCreate,
                auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
                db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return create(db=db, series=series)
        



@router.post("/get_series")
def get_series_details(
    request: QuotationSeriesRequest,  
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
   
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    
    series_list = get_series(db=db, admin_id=request.admin_id, employee_id=request.employee_id , series_type = request.series_type , series_name = request.series_name)

    #series_list = get_series(db=db, admin_id=request.admin_id, employee_id=request.employee_id)

    return {
        "status": "true",
        "message": "Quotation Series Retrieved Successfully",
        "data": series_list
    }



@router.post("/update_series")
def update_series_details(
    request: QuotationSeriesUpdateRequest,  
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    
    
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    
    
    return update_series(db=db, series_data=request)



@router.post("/delete_series")
def delete_series_details(
    request: QuotationSeriesDeleteRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
   
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    
    return delete_series(db=db, admin_id=request.admin_id, series_id=request.series_id)
    
    
    
    

# @router.post("/get_series_detail")
# def get_series_detail(
#     request: QuotationSeriesDetailRequest,
#     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#     db: Session = Depends(get_db)
# ):
#     if auth_token != get_token():
#         return {"status": "false", "message": "Unauthorized Request"}

    
#     series = db.exec(
#         select(QuotationSeries).where(
#             QuotationSeries.admin_id == request.admin_id,
#             QuotationSeries.series_type == request.series_type,  # Check series_type first
#             QuotationSeries.series_name == request.series_name
#         )
#     ).first()

#     if not series:
#         return {"status": "false", "message": "Quotation Series Not Found"}

    
#     last_quotation = db.exec(
#         select(Quotation.quotation_number)
#         .where(Quotation.series == request.series_name)
#         .order_by(Quotation.id.desc())  
#     ).first()

#     last_quot_number = last_quotation if last_quotation else "0000" 

#     return {
#         "status": "true",
#         "message": "Quotation Series Found",
#         "data": {
#             "id": series.id,
#             "admin_id": series.admin_id,
#             "employee_id": series.employee_id,
#             "series_type": series.series_type,
#             "series_name": series.series_name,
#             "quotation_formate": series.quotation_formate,
#             "created_at": series.created_at,
#             "updated_at": series.updated_at,
#             "last_quot_number": last_quot_number  
#         }
#     }
    

    

from sqlalchemy.future import select
from sqlalchemy.exc import MultipleResultsFound
from src.PurchaseOrderIssue.models import PurchaseOrderIssue
from src.GrnOrders.models import GrnOrderIssue
from src.ProjectManagerOrder.models import ProjectManagerOrder

@router.post("/get_series_detail")
def get_series_detail(
    request: QuotationSeriesDetailRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    # Token check
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    # Construct query for QuotationSeries based on filters
    query = select(QuotationSeries)
    
    if request.admin_id:
        query = query.where(QuotationSeries.admin_id == request.admin_id)
    if request.series_type:
        query = query.where(QuotationSeries.series_type == request.series_type)
    if request.series_name:
        query = query.where(QuotationSeries.id == request.series_name)
        
    # Order the query by descending ID to get the most recent one first
    query = query.order_by(QuotationSeries.id.desc())

    # Execute query for series
    series = db.execute(query).scalar_one_or_none()

    if not series:
        return {"status": "false", "message": "Quotation Series Not Found"}

    # Query to get the last quotation 
    if request.series_type == "Sales Order":
        last_quotation_query = select(Quotation.pi_number).where(
            Quotation.pi_series == request.series_name
        ).order_by(Quotation.id.desc()).limit(1)  # Limit to the most recent 
        

        
    if request.series_type == "Quotation":
        last_quotation_query = select(Quotation.quotation_number).where(
            Quotation.series == request.series_name
        ).order_by(Quotation.id.desc()).limit(1)  # Limit to the most recent quotation



    if request.series_type == "Purchase Order":
        last_quotation_query = select(PurchaseOrderIssue.order_number).where(
            PurchaseOrderIssue.series == request.series_name
        ).order_by(PurchaseOrderIssue.id.desc()).limit(1)  # Limit to the most recent quotation




    if request.series_type == "Delivery Challan":
        last_quotation_query = select(Quotation.quotation_number).where(
            Quotation.dc_series == request.series_name
        ).order_by(Quotation.id.desc()).limit(1)  # Limit to the most recent quotation



    if request.series_type == "Proforma Invoices":
        last_quotation_query = select(Quotation.invoice_number).where(
            Quotation.inv_series == request.series_name
        ).order_by(Quotation.id.desc()).limit(1)  # Limit to the most recent quotation



    if request.series_type == "GRN":
        last_quotation_query = select(GrnOrderIssue.grn_number).where(
            GrnOrderIssue.series_id == request.series_name
        ).order_by(GrnOrderIssue.id.desc()).limit(1)  # Limit to the most recent quotation
        
        
    if request.series_type == "GRN Invoice":
        last_quotation_query = select(GrnInvoice.vender_invoice_number).where(
            GrnInvoice.series_id == request.series_name
        ).order_by(GrnInvoice.id.desc()).limit(1)
        
        
    if request.series_type == "RFQ Number":
        last_quotation_query = select(Rfq.rfq_id).where(
            Rfq.series_id == request.series_name
        ).order_by(Rfq.id.desc()).limit(1)
        
        
    if request.series_type == "Manual Order":
        last_quotation_query = select(
            ProjectManagerOrder.manual_sale_order_id , 
            ProjectManagerOrder.status == "Manual" 
            ).where(
            ProjectManagerOrder.series == request.series_name
        ).order_by(ProjectManagerOrder.id.desc()).limit(1)  # Limit to the most recent 
        
        
  

        
    try:
        # Execute query for the last quotation number
        last_quotation = db.execute(last_quotation_query).scalar_one_or_none()
        # Default to "0001" if no quotation found
        last_quot_number = last_quotation if last_quotation else "0000"

    except MultipleResultsFound:
        # Handle case where multiple results are found and avoid the exception
        return {"status": "false", "message": "Multiple quotations found. Please check the data."}

    # Return the result
    return {
        "status": "true",
        "message": "Quotation Series Found",
        "data": {
            "id": series.id,
            "admin_id": series.admin_id,
            "employee_id": series.employee_id,
            "series_type": series.series_type,
            "series_name": series.series_name,
            "quotation_formate": series.quotation_formate,
            "created_at": series.created_at,
            "updated_at": series.updated_at,
            "last_quot_number": last_quot_number
        }
    }
    
    
    
    
