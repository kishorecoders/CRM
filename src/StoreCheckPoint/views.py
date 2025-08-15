from fastapi import APIRouter, Depends,  Header
from sqlalchemy.orm import Session
from src.database import get_db
from src.parameter import get_token
from src.StoreCheckPoint.models import CheckPointUpdate
from src.StoreCheckPoint.service import  update_checkPoint

router = APIRouter()

@router.post("/Update_StoreCheckpoint")
def update_checkPoint_by_id(
    checkPointUpdate: CheckPointUpdate, 
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    return update_checkPoint(db=db, checkPointUpdate = checkPointUpdate)



