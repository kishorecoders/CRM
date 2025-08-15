from sqlalchemy.orm import Session
from src.StoreCheckPoint.models import StoreCheckPoint , CheckPointUpdate

def update_checkPoint(db: Session, checkPointUpdate: CheckPointUpdate):
    checkPoint = db.query(StoreCheckPoint).filter(StoreCheckPoint.id == checkPointUpdate.checkPoint_id).first()

    if not checkPoint:
        return {
            "status": "false",
            "message": "checkPoint not found"
        }

    # Update fields only if new values are provided
    if checkPointUpdate.admin_id:
        checkPoint.admin_id = checkPointUpdate.admin_id
    else:
        checkPoint.admin_id = checkPoint.admin_id

    if checkPointUpdate.check_point_name:
        checkPoint.check_point_name = checkPointUpdate.check_point_name
    else:
        checkPoint.check_point_name = checkPoint.check_point_name

    if checkPointUpdate.check_point_status:

        checkPoint.check_point_status = checkPointUpdate.check_point_status
    else:
        checkPoint.check_point_status = checkPoint.check_point_status
    db.commit()
    db.refresh(checkPoint)

    return {
        "status": "true",
        "message": "checkPoint updated successfully",
        "data": {
            "id": checkPoint.id,
            "admin_id": checkPoint.admin_id,
            "emp_id": checkPoint.emp_id,
            "subproduct_id": checkPoint.subproduct_id,
            "stage_id": checkPoint.stage_id,
            "check_point_name": checkPoint.check_point_name,
            "check_point_status": checkPoint.check_point_status
        }
    }
