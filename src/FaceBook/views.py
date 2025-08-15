from starlette.responses import JSONResponse
from fastapi import Request
from fastapi import APIRouter
from .models import FacebookLead
import json
from sqlmodel import Session
from datetime import datetime
from src.database import engine
router = APIRouter()

VERIFY_TOKEN = "my_verify_token"

@router.get("/facebook/webhook")
async def verify_webhook(request: Request):
    params = dict(request.query_params)
    if params.get("hub.mode") == "subscribe" and params.get("hub.verify_token") == VERIFY_TOKEN:
        return JSONResponse(content=params.get("hub.challenge"))
    return JSONResponse(content="Verification token mismatch", status_code=403)

# @router.post("/facebook/webhook")
# async def receive_lead(request: Request):
#     data = await request.json()
#     print("Received lead data:", data)
#     # Here you can save data to your DB
#     return JSONResponse(content={"status": "received"}, status_code=200)

@router.post("/facebook/webhook")
async def receive_lead(request: Request):
    data = await request.json()
    print("Received lead data:", json.dumps(data, indent=2))

    entry = data["entry"][0]
    lead_data = entry["changes"][0]["value"]

    lead = FacebookLead(
        form_id=lead_data["form_id"],
        leadgen_id=lead_data["leadgen_id"],
        field_data=json.dumps(lead_data["field_data"])  # Save as raw JSON
    )

    with Session(engine) as session:
        session.add(lead)
        session.commit()

    return JSONResponse(content={"status": "received"}, status_code=200)


from starlette.responses import JSONResponse
import datetime


@router.post("/simulate/facebook/lead")
async def simulate_lead():
    data = {
        "entry": [
            {
                "changes": [
                    {
                        "value": {
                            "form_id": "test_form_id",
                            "leadgen_id": "test_lead_id",
                            "created_time": datetime.datetime.utcnow().isoformat(),
                            "field_data": [
                                {"name": "email", "values": ["test@example.com"]},
                                {"name": "full_name", "values": ["Test User"]},
                            ]
                        }
                    }
                ]
            }
        ]
    }
    # Forward this internally to the same POST webhook
    from fastapi.testclient import TestClient
    from src.main import app  # assuming your FastAPI instance is called `app`
    client = TestClient(app)
    res = client.post("/v1/FaceBook/facebook/webhook", json=data)
    return res.json()
