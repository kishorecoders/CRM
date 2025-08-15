from datetime import datetime, timedelta
import random
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
import requests
from sqlmodel import Session
from src.SubscribeOtp.models import OTPStore
from src.database import get_db
from .models import SendOtpRequest, Subscribe, SubscribeCreate, FetchSubscribeRequest, VerifyOtpRequest
from .service import create, fetch_subscribe_files
from src.parameter import get_token

router = APIRouter()


VISION_HLT_API_URL = "https://sms.visionhlt.com/api/mt/SendSMS"
VISION_HLT_API_KEY = "Inu4l5KPoUmyzBSNeo3nKQ"
YOUR_SENDER_ID = "VISHLT" 

@router.post("/send_otp")
def send_otp(
    request: SendOtpRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db),
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")

    otp = random.randint(100000, 999999)

    # message = f"Your verification code for login is {otp}. Kindly use above OTP to login to your account. Thanks and Regards VISION HLT"

    # payload = {
    #     "Account": {
    #         "APIKey": VISION_HLT_API_KEY,
    #         "SenderId": YOUR_SENDER_ID,
    #         "Channel": "Trans",
    #         "DCS": "0",
    #         "SchedTime": None,
    #         "GroupId": None,
    #     },
    #     "Messages": [{"Number": request.phone_number, "Text": message}],
    # }

    # try:
    #     print("Sending OTP payload:", payload)
    #     response = requests.post(
    #         VISION_HLT_API_URL,
    #         json=payload,
    #         headers={"Content-Type": "application/json"},
    #     )
    #     print("Response Code:", response.status_code)
    #     print("Response Body:", response.text)

    #     response.raise_for_status()
    #     response_data = response.json()

    #     if response_data.get("ErrorCode") != "000":
    #         return {
    #             "status": "false",
    #             "message": "Failed to send OTP",
    #             "error": response_data.get("ErrorMessage", "Unknown Error"),
    #         }
        
    otp_entry = OTPStore(phone_number=request.phone_number, otp=str(otp))
    db.add(otp_entry)
    db.commit()
    return {"status": "true", "message": "OTP sent successfully", "otp": otp}

    # except Exception as e:
    #     print("Error sending OTP:", str(e))
    #     return {"status": "false", "message": "Failed to send OTP", "error": str(e)}


@router.post("/verify_otp")
def verify_otp(request: VerifyOtpRequest, db: Session = Depends(get_db)):
    otp_entry = (
        db.query(OTPStore)
        .filter(OTPStore.phone_number == request.phone)
        .order_by(OTPStore.created_at.desc())
        .first()
    )

    if not otp_entry:
        return {"status": "false", "message": "OTP not found"}
    if datetime.utcnow() - otp_entry.created_at > timedelta(minutes=5):
        return {"status": "false", "message": "OTP expired"}
    if otp_entry.otp != request.otp:
        return {"status": "false", "message": "Invalid OTP"}
    
    # Save subscription only now
    sub = Subscribe(
        employee_id=request.employee_id,
        admin_id=request.admin_id,
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        phone=request.phone,
        plan_type=request.plan_type,
        privacy=request.privacy,
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)

    return {
        "status": "true",
        "message": "Subscription created",
    }


# @router.post("/create_subscribe")
# def create_subscribe(
#     subscribe_create: SubscribeCreate,
#     auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#     db: Session = Depends(get_db)
# ):
#
#     if auth_token != get_token():
#         return {"status": "false", "message": "Unauthorized Request"}
#
#     return create(db=db, subscribe_create=subscribe_create)


@router.post("/get_subscribe_files")
def get_subscribe_files(
    request: FetchSubscribeRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}


    results = fetch_subscribe_files(db=db, request=request)

    if not results:
        return {"status": "false", "message": "No records found"}

    return {"status": "true", "message": "Subscriptions retrieved successfully", "data": results}





