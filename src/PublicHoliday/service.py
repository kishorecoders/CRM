from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from src.PublicHoliday.models import PublicHoliday,PublicHolidayCreate
from fastapi.responses import JSONResponse
from sqlalchemy import select
from fastapi import HTTPException





def create_public_holiday_service(db: Session, holiday: PublicHolidayCreate):
    try:
        
        try:
            parsed_event_date = datetime.strptime(holiday.event_date, "%d-%m-%Y")
        except ValueError:
            return JSONResponse(
                status_code=200,
                content={"status": "false", "message": "Invalid date format. Use dd-MM-yyyy"}
            )

       
        existing_holiday = db.query(PublicHoliday).filter(
            PublicHoliday.admin_id == holiday.admin_id,
            PublicHoliday.event_date == parsed_event_date,
        ).first()

        if existing_holiday:
            return JSONResponse(
                status_code=200,
                content={"status": "false", "message": "Holiday already exists for the given date."}
            )

       
        new_holiday = PublicHoliday(
            admin_id=holiday.admin_id,
            event_name=holiday.event_name,
            event_date=parsed_event_date,
        )
        db.add(new_holiday)
        db.commit()
        db.refresh(new_holiday)

      
        formatted_date = new_holiday.event_date.strftime("%d-%m-%Y")

        return JSONResponse(
            status_code=200,
            content={
                "status": "true",
                "message": "Public holiday created successfully",
                "data": {
                    "id": new_holiday.id,
                    "admin_id": new_holiday.admin_id,
                    "event_name": new_holiday.event_name,
                    "event_date": formatted_date,
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "false", "message": f"Error creating holiday: {str(e)}"}
        )




def get_public_holiday_list_service(db: Session, admin_id: str) -> List[dict]:
   
    try:
        
       # query = select(PublicHoliday).where(PublicHoliday.admin_id == admin_id)
        query = select(PublicHoliday).where(PublicHoliday.admin_id == admin_id).order_by(PublicHoliday.id.desc())
        results = db.execute(query).scalars().all()

        if not results:
            raise ValueError("Admin not found")

 
        holiday_list = []
        for result in results:
            
            holiday = result if isinstance(result, PublicHoliday) else result[0]
            holiday_data = {
                "id":holiday.id,
                "admin_id": holiday.admin_id,
                "event_name": holiday.event_name,
                "event_date": holiday.event_date.isoformat() if isinstance(holiday.event_date, datetime) else str(holiday.event_date),
                "create_date": holiday.created_at,
            }
            holiday_list.append(holiday_data)

        
        

        return holiday_list
    except ValueError as ve:
        
        raise ValueError(str(ve))
    except Exception as e:
        
        raise Exception(f"Error fetching public holidays: {str(e)}")
    


def delete_public_holiday_service(db: Session, admin_id: str, public_holiday_id: int) -> dict:
   
    try:
       
        query = select(PublicHoliday).where(PublicHoliday.admin_id == admin_id).where(PublicHoliday.id == public_holiday_id)
        
        
        holiday = db.execute(query).scalar_one_or_none()

       
        if not holiday:
            return {
            "status": "false",
            "message": "Public Holiday not found"
        }
            # raise HTTPException(status_code=200, detail="Public Holiday not found")

        
        db.delete(holiday)
        db.commit()

        return {
            "status": "true",
            "message": "Public holiday deleted successfully"
        }
    except Exception as e:
        db.rollback()  
        raise HTTPException(status_code=500, detail=f"Error deleting public holiday: {str(e)}")