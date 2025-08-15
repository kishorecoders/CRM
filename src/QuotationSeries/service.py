from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status,HTTPException
from .models import QuotationSeries,QuotationSeriesCreate,QuotationSeriesUpdateRequest
from sqlmodel import Session, select
import re
from sqlalchemy import select, update



# def create(db: Session, series: QuotationSeriesCreate):
#     existing_series = db.exec(
#         select(QuotationSeries).where(
#             QuotationSeries.admin_id == series.admin_id,
#             QuotationSeries.series_name == series.series_name
#         )
#     ).first()

#     if existing_series:
#         return {'status': 'false', 'message': "Quotation Series Name already exists for this Admin"}

    
#     db_series = QuotationSeries(**series.dict())
#     db.add(db_series)
#     db.commit()
#     db.refresh(db_series)
    
#     response = {'status': 'true', 'message': "Quotation Series Added Successfully", 'data': db_series}
#     return response


def validate_quotation_format(quotation_formate: str) -> bool:
    """Validate that quotation_formate follows 'ANY/ANY/YY-YY/' format."""
    pattern = r"^[A-Za-z0-9]+/[A-Za-z0-9]+/\d{2}-\d{2}/$"
    return bool(re.match(pattern, quotation_formate))





def create(db: Session, series: QuotationSeriesCreate):
    existing_series = db.execute(
        select(QuotationSeries).where(
            QuotationSeries.admin_id == series.admin_id,
            QuotationSeries.series_name == series.series_name
        )
    ).first()

    if existing_series:
        return {'status': 'false', 'message': "Quotation Series Name already exists for this Admin"}

    if series.is_default:
        db.execute(
            update(QuotationSeries)
            .where(QuotationSeries.admin_id == series.admin_id)
            .values(is_default=False)
        )

    
    db_series = QuotationSeries(**series.dict())
    db.add(db_series)
    db.commit()
    db.refresh(db_series)
    
    response = {'status': 'true', 'message': "Quotation Series Added Successfully", 'data': db_series}
    return response







# def create(db: Session, series: QuotationSeriesCreate):
#     """Create a new quotation series with validation."""

#     # Validate dynamic format (X/Y/YY-YY/)
#     if not validate_quotation_format(series.quotation_formate):
#         return {"status": "false", "message": "Invalid format! Use 'XXX/YYY/YY-YY/' format"}

#     # Check if series already exists
#     existing_series = db.exec(
#         select(QuotationSeries).where(
#             QuotationSeries.admin_id == series.admin_id,
#             QuotationSeries.series_name == series.series_name
#         )
#     ).first()

#     if existing_series:
#         return {'status': 'false', 'message': "Quotation Series Name already exists for this Admin"}

#     if series.is_default:
#         db.execute(
#             update(QuotationSeries)
#             .where(QuotationSeries.admin_id == series.admin_id)
#             .values(is_default=False)
#         )


#     # Create and save new series
#     db_series = QuotationSeries(**series.dict())
#     db.add(db_series)
#     db.commit()
#     db.refresh(db_series)

#     return {'status': 'true', 'message': "Quotation Series Added Successfully", 'data': db_series}











def get_series(db: Session, admin_id: str, employee_id: Optional[str] = None, series_type: Optional[str] = None , series_name: Optional[str] = None):
    
    
    query = select(QuotationSeries).where(QuotationSeries.admin_id == admin_id)
    
    if employee_id:
        query = query.where(QuotationSeries.employee_id == employee_id)
    
    if series_type:
        query = query.where(QuotationSeries.series_type == series_type)

    if series_name:
        query = query.where(QuotationSeries.series_name == series_name)

    query = query.order_by(QuotationSeries.id.desc())

    #series_list = db.exec(query).all()
    series_list = db.execute(query).scalars().all()

    return series_list




def update_series(db: Session, series_data: QuotationSeriesUpdateRequest):
    
    #series = db.exec(select(QuotationSeries).where(QuotationSeries.id == series_data.id)).first()
    series = db.query(QuotationSeries).filter(QuotationSeries.id == series_data.id).first()

    if not series:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quotation Series not found"
        )
    
    
    series.admin_id = series_data.admin_id
    series.employee_id = series_data.employee_id if series_data.employee_id is not None else series.employee_id
    series.series_type = series_data.series_type if series_data.series_type is not None else series.series_type
    series.series_name = series_data.series_name if series_data.series_name is not None else series.series_name
    series.quotation_formate = series_data.quotation_formate if series_data.quotation_formate is not None else series.quotation_formate
    series.branch_name = series_data.branch_name if series_data.branch_name is not None else series.branch_name
    series.updated_at = datetime.utcnow()  

    if series_data.is_default == "true":
        db.execute(
            update(QuotationSeries)
            .where(QuotationSeries.admin_id == QuotationSeries.admin_id)
            .values(is_default=False)
        )
        db.commit()  
        series.is_default = True
    elif series_data.is_default == "false":
        series.is_default = False
          
    db.add(series)
    db.commit()
    db.refresh(series)
    return {
        "status": "true",
        "message": "Quotation Series Updated Successfully",
        "data": series
    }


def delete_series(db: Session, admin_id: str, series_id: int):
    
    series = db.query(QuotationSeries).filter(
        QuotationSeries.id == series_id,
        QuotationSeries.admin_id == admin_id
    ).first()

    if not series:
        return {"status": "false", "message": "Quotation Series not found"}
        

    
    db.delete(series)
    db.commit()

    return {"status": "true", "message": "Quotation Series deleted successfully"}