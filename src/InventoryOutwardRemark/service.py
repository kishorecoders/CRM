from .models import InventoryOutwardRemark,InventoryOutwardRemarkCreate
from fastapi import HTTPException
from sqlalchemy.orm import Session


def create(outward_data: InventoryOutwardRemarkCreate, db: Session):
    try:
        # Convert Pydantic model to dictionary
        data = outward_data.dict()

        # Create ORM instance from the data
        new_outward_remark = InventoryOutwardRemark(**data)

        # Save to database
        db.add(new_outward_remark)
        db.commit()
        db.refresh(new_outward_remark)

        return {
            "status": "true",
            "message": "Inventory Remark Outward created successfully",
            "data": new_outward_remark
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create inventory remark: {str(e)}")