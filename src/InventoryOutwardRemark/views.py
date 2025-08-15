from fastapi import APIRouter, Depends,Header
from sqlmodel import Session
from src.database import get_db
from .models import InventoryOutwardRemarkCreate
from .service import create
from src.parameter import get_token

router = APIRouter()


@router.post("/createInventoryOutwardRemark")
def create_inventory_outward(
    outward_data: InventoryOutwardRemarkCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    
    return create(outward_data=outward_data, db=db)



