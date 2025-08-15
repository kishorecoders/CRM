from sqlalchemy.orm import Session
from src.CheckPoint.models import CheckPoint , CheckPointCreate , CheckPointRead , CheckPointDeletee ,CheckPointUpdate
from src.QuotationSubProductEmployee.models import QuotationSubProductEmployee 
from src.ProductStages.models import ProductStages


def create(db: Session, checkPointCreate: CheckPointCreate):

    subproduct = db.query(QuotationSubProductEmployee).filter(QuotationSubProductEmployee.id == checkPointCreate.subproduct_id).first()
    if not subproduct:
        return {
            "status": "false",
            "message": "Invalid subproduct_id"
        }

    stage = db.query(ProductStages).filter(ProductStages.id == checkPointCreate.stage_id).first()
    if not stage:
        return {
            "status": "false",
            "message": "Invalid stage_id"
        }

    created = []
    skipped = []

    for item in checkPointCreate.CheckPoints:
        name = item.check_point_name
        status = item.check_point_status

        existing = db.query(CheckPoint).filter(
            CheckPoint.subproduct_id == checkPointCreate.subproduct_id,
            CheckPoint.check_point_name == name
        ).first()

        if existing:
            skipped.append(name)
            continue

        db_check = CheckPoint(
            admin_id=checkPointCreate.admin_id,
            emp_id=checkPointCreate.emp_id,
            subproduct_id=checkPointCreate.subproduct_id,
            stage_id=checkPointCreate.stage_id,
            check_point_name=name,
            check_point_status = status
        )
        db.add(db_check)
        db.commit()
        db.refresh(db_check)

        created.append({
            "id": db_check.id,
            "admin_id": db_check.admin_id,
            "emp_id": db_check.emp_id,
            "subproduct_id": db_check.subproduct_id,
            "stage_id": db_check.stage_id,
            "check_point_name": db_check.check_point_name,
            "check_point_status": db_check.check_point_status
        })

    return {
        "status": "true",
        "message": f"{len(created)} CheckPoint(s) created",
        "created_sub_products": created

    }


def get_checkPoint(db: Session, checkPointRead: CheckPointRead):
    query = db.query(CheckPoint)

    if checkPointRead.subproduct_id and checkPointRead.stage_id:
        query = query.filter(
            CheckPoint.subproduct_id == checkPointRead.subproduct_id,
            CheckPoint.stage_id == checkPointRead.stage_id
        )
    elif checkPointRead.subproduct_id:
        query = query.filter(CheckPoint.subproduct_id == checkPointRead.subproduct_id)
    elif checkPointRead.stage_id:
        query = query.filter(CheckPoint.stage_id == checkPointRead.stage_id)
    else:
        return {"status": "false", "message": "Either Sub-product ID or Stage ID must be provided"}

    db_checkpoint = query.all()

    if not db_checkpoint:
        return {
            "status": "false",
            "message": "No checkpoint found for the given Sub-product ID and/or Stage ID"
        }

    return {
        "status": "true",
        "message": "Checkpoint fetched successfully",
        "count": len(db_checkpoint),
        "data": db_checkpoint
    }


def check_PointDeletee_by_id(db: Session, checkPoint_id: CheckPointDeletee):
    checkPoint = db.query(CheckPoint).filter(
        CheckPoint.id == checkPoint_id.checkPoint_id
    ).first()

    if not checkPoint:
        return {
            "status": "true",
            "message": "checkPoint not found"
        }

    db.delete(checkPoint)
    db.commit()

    return {
        "status": "true",
        "message": "checkPoint deleted successfully"
    }



def update_checkPoint(db: Session, checkPointUpdate: CheckPointUpdate):
    checkPoint = db.query(CheckPoint).filter(CheckPoint.id == checkPointUpdate.checkPoint_id).first()

    if not checkPoint:
        return {
            "status": "false",
            "message": "checkPoint not found"
        }

    if checkPointUpdate.subproduct_id:
        subproduct = db.query(QuotationSubProductEmployee).filter(
            QuotationSubProductEmployee.id == checkPointUpdate.subproduct_id
        ).first()
        if not subproduct:
            return {
                "status": "false",
                "message": "Invalid subproduct_id"
            }

    if checkPointUpdate.stage_id:
        stage = db.query(ProductStages).filter(
            ProductStages.id == checkPointUpdate.stage_id
        ).first()
        if not stage:
            return {
                "status": "false",
                "message": "Invalid stage_id"
            }

    # Update fields only if new values are provided
    checkPoint.admin_id = checkPointUpdate.admin_id or checkPoint.admin_id
    checkPoint.emp_id = checkPointUpdate.emp_id or checkPoint.emp_id
    checkPoint.subproduct_id = checkPointUpdate.subproduct_id or checkPoint.subproduct_id
    checkPoint.stage_id = checkPointUpdate.stage_id or checkPoint.stage_id

    for item in checkPointUpdate.CheckPoints:
        if item.check_point_name:
            checkPoint.check_point_name = item.check_point_name
    if item.check_point_status is not None:
            checkPoint.check_point_status = item.check_point_status

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
