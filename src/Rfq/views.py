from fastapi import APIRouter, Depends, Header
from src.database import get_db
from src.parameter import get_token
from .models import RfqCreate,RfqFilterRequest,RfqRead,RfqUpdate,RfqFileUploadRequest,Rfq,RfqEmail
from .service import create_rfq_record,get_rfq_list
from typing import List
import os
import shutil
from fastapi import APIRouter, Depends, Header, UploadFile, File, Form
import json
from fastapi.responses import JSONResponse
import base64
from sqlmodel import Session, select
from src.parameter import get_current_datetime


router = APIRouter()

@router.post("/create_rfq")
def create_rfq(
    request: RfqCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    return create_rfq_record(db=db, request=request)
    
    
    
    
@router.post("/get_rfq_list")
def fetch_rfq_list(
    request: RfqFilterRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    rfqs = get_rfq_list(db=db, admin_id=request.admin_id, employee_id=request.employee_id)

    return {
        "status": "true",
        "message": "RFQ list fetched successfully",
        "data": rfqs
    }







@router.post("/update_rfq")
def update_rfq(
    request: RfqUpdate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    return update_rfq_record(db=db, request=request)
    
    
    
    
    
def save_base64_file(base64_str: str, filename: str) -> str:
    """Save a Base64 file to the 'uploads' directory."""
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    file_path = os.path.join("uploads", filename)
    with open(file_path, "wb") as file:
        file.write(base64.b64decode(base64_str))

    return file_path
        
        


        
        
@router.post("/attach_rfq_file")
async def upload_rfq_file(
    request: RfqFileUploadRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    try:
        # Save file locally
        file_path = save_base64_file(request.base64_file, request.filename)

        # Fetch and update RFQ
        rfq: Rfq = db.query(Rfq).filter(Rfq.id == request.rfq_id).first()

        if not rfq:
            return JSONResponse(status_code=404, content={
                "status": "false",
                "message": "RFQ not found"
            })

        rfq.file_path = file_path
        rfq.file_name = request.filename
        rfq.updated_at = get_current_datetime()

        db.commit()

        return JSONResponse(content={
            "status": "true",
            "message": "File uploaded and RFQ updated successfully",
            "file_path": file_path
        })

    except base64.binascii.Error as ve:
        return JSONResponse(content={
            "status": "false",
            "message": f"Invalid base64 data: {str(ve)}"
        })
    except Exception as e:
        return JSONResponse(content={
            "status": "false",
            "message": f"Unexpected error: {str(e)}"
        
        })
        
from src.SmtpEmail.Smtp_mail import send_login_email, send_rqf 
from datetime import datetime
from src.vendor.models import Vendor
from fastapi import Request

@router.post("/send_rfq_file")
def send_rfq_file(
    rrr: RfqEmail,
    request: Request,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    client_ip = request.client.host
    current_date = datetime.now()

    # Get the RFQ entry
    rfq = db.query(Rfq).filter(Rfq.id == int(rrr.rfq_id)).first()
    if not rfq or not rfq.vendor_id:
        return {"status": "false", "message": "RFQ or vendor IDs not found"}

    # Parse vendor_ids (stored as string like '"2","22","33"')
    try:
        raw_ids = rfq.vendor_id.replace('"', '').split(',')  # Removes quotes and splits
        vendor_ids = [int(id.strip()) for id in raw_ids if id.strip().isdigit()]
    except Exception as e:
        return {"status": "false", "message": f"Invalid vendor_id format: {str(e)}"}

    # Fetch vendors and send email
    vendors = db.query(Vendor).filter(Vendor.id.in_(vendor_ids)).all()

    for vendor in vendors:
        # send_login_email(
        #     # to_email=vendor.email,
        #     to_email="poojaevolve20@gmail.com",
        #     subject="RFQ Created Successfully",
        #     body=(
        #         f"Hello {vendor.vendor_name},\n\n"
        #         f"You have received an RFQ on {current_date.strftime('%Y-%m-%d %H:%M:%S')}.\n"
        #         f"IP Address: {client_ip}.\n"
        #         f"File: {rrr.file_url}\n\n"
        #         f"Regards,\n"
        #         f"SphuritCRM Team"
        #     )
        # )

        send_rqf(
            to_email=vendor.email,
            subject="RFQ Created Successfully",
            body="Hello,\n\nYou have received an RFQ...\n\nRegards,\nSphuritCRM Team",
            attachment_path=rrr.file_url
        )

    return {"status": "true", "message": "Emails sent to all vendors"}

        
        
from fastapi import UploadFile, File
import shutil
import os

@router.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    save_path = f"./uploads/{file.filename}"
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"file_url": save_path}

        
        
        
        