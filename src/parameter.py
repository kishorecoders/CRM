import functools
from fastapi import HTTPException, Header
from datetime import datetime
import pytz


auth_key = '2ec26ad9-e039-445e-915e-a482dc6f5e3b'

def get_token():
    return auth_key

def get_current_datetime():
    ist = pytz.timezone('Asia/Kolkata')
    current_utc_time = datetime.now(pytz.utc)
    current_ist_time = current_utc_time.astimezone(ist)
    return current_ist_time

