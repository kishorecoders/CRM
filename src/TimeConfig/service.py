from sqlmodel import Session, select
from fastapi import HTTPException
from .models import TimeConfig, TimeConfigCreate
from datetime import datetime


from src.LateMark.models import LateMark

from datetime import datetime, timedelta

from datetime import datetime, timedelta

from datetime import datetime, timedelta

def validate_time_within_shift(label: str, shift_start: str, shift_end: str, *times):
    fmt = "%I:%M %p"

    try:
        shift_start_dt = datetime.strptime(shift_start.strip(), fmt)
        shift_end_dt = datetime.strptime(shift_end.strip(), fmt)
        # Strict rule: shift_end must be after shift_start
        if shift_end_dt <= shift_start_dt:
            return {
                "status": "false",
                "message": f"{label} shift end time must be after shift start time"
            }
        # Detect overnight shift
        overnight_shift = False
        if shift_end_dt <= shift_start_dt:
            shift_end_dt += timedelta(days=1)
            overnight_shift = True
    except ValueError:
        return {
            "status": "false",
            "message": f"{label} shift start/end time format is invalid"
        }

    shift_times = {}
    for time_label, t in times:
        if not t:
            continue
        try:
            t_dt = datetime.strptime(t.strip(), fmt)

            # Adjust time if overnight and time is earlier than shift_start
            if overnight_shift and t_dt < shift_start_dt:
                t_dt += timedelta(days=1)

            shift_times[time_label] = t_dt
        except ValueError:
            if time_label in ["in_time", "out_time"]:
                continue
            return {
                "status": "false",
                "message": f"{label} {time_label} has invalid format. Use HH:MM AM/PM"
            }

    # Validate all times (except out_time) are within shift start and end
    for time_label, t_dt in shift_times.items():
        # if time_label != "out_time"  and time_label != "lunch_start" and time_label != "lunch_end" and not (shift_start_dt <= t_dt <= shift_end_dt):
        if time_label != "out_time" and time_label != "in_time" and not (shift_start_dt <= t_dt <= shift_end_dt):
            # if time_label == "in_time":
            #     time_label = "In Time"
            if time_label == "lunch_start":
            # elif time_label == "lunch_start":
                time_label = "Lunch Start Time"
            elif time_label == "lunch_end":
                time_label = "Lunch End Time"
            else:
                time_label = time_label
            return {
                "status": "false",
                # "message": f"{label} {time_label} ({t_dt.strftime(fmt)}) must be within Shift Start ({shift_start}) and End Time ({shift_end})"
                "message": f"{label} {time_label} must be within Shift Start and End Time"
            }

    # if "out_time" in shift_times and shift_times["out_time"] <= shift_start_dt:
    #     return {
    #         "status": "false",
    #         "message": f"{label} Out Time must be after shift Start Time"
    #     }




    return {
        "status": "true",
        "message": f"{label} shift time(s) are valid"
    }




def validate_time_sequence(label: str, in_time: str, lunch_start: str, lunch_end: str, out_time: str):
    fmt = "%I:%M %p"
    try:
        #in_time_dt = datetime.strptime(in_time.strip(), fmt)
        lunch_start_dt = datetime.strptime(lunch_start.strip(), fmt)
        lunch_end_dt = datetime.strptime(lunch_end.strip(), fmt)
        # = datetime.strptime(out_time.strip(), fmt)

        #if lunch_start_dt < in_time_dt:
        #    lunch_start_dt += timedelta(days=1)
        if lunch_end_dt < lunch_start_dt:
            lunch_end_dt += timedelta(days=1)
        #if out_time_dt < lunch_end_dt:
        #    out_time_dt += timedelta(days=1)

    except ValueError:
        return {
            "status": "false",
            "message": f"{label} shift contains invalid time format. Expected format like '09:49 AM'"
        }



    return {
        "status": "true",
        "message": f"{label} shift time sequence is valid"
    }


def create_or_update_time_config(db: Session, time_config_create: TimeConfigCreate):
    existing_config = db.execute(
        select(TimeConfig).where(TimeConfig.admin_id == time_config_create.admin_id)
    ).scalars().first()

    def validate_shift(label, start, end, in_time, out_time, lunch_start, lunch_end):
        if start and end:
            result = validate_time_within_shift(
                label, start, end,
                ("in_time", in_time),
                ("out_time", out_time),
                ("lunch_start", lunch_start),
                ("lunch_end", lunch_end),
            )
            if result["status"] == "false":
                return result

            if all([in_time, lunch_start, lunch_end, out_time]):
                result = validate_time_sequence(label, in_time, lunch_start, lunch_end, out_time)
                if result["status"] == "false":
                    return result
        return {"status": "true"}

    # Validate 1st shift
    if time_config_create.start_time_1st and time_config_create.end_time_1st:
        result = validate_shift(
            "1st Shift",
            time_config_create.start_time_1st,
            time_config_create.end_time_1st,
            time_config_create.in_time_1st,
            time_config_create.out_time_1st,
            time_config_create.lunch_time_start_1st,
            time_config_create.lunch_time_end_1st,
        )
        if result["status"] == "false":
            return result

    # Validate 2nd shift
    result = validate_shift(
        "2nd Shift",
        time_config_create.start_time_2nd,
        time_config_create.end_time_2nd,
        time_config_create.in_time_2nd,
        time_config_create.out_time_2nd,
        time_config_create.lunch_time_start_2nd,
        time_config_create.lunch_time_end_2nd
    )
    if result["status"] == "false":
        return result

    # Validate 3rd shift
    result = validate_shift(
        "3rd Shift",
        time_config_create.start_time_3rd,
        time_config_create.end_time_3rd,
        time_config_create.in_time_3rd,
        time_config_create.out_time_3rd,
        time_config_create.lunch_time_start_3rd,
        time_config_create.lunch_time_end_3rd
    )
    if result["status"] == "false":
        return result

    # Validate General shift
    result = validate_shift(
        "General Shift",
        time_config_create.start_time_general,
        time_config_create.end_time_general,
        time_config_create.in_time_general,
        time_config_create.out_time_general,
        time_config_create.lunch_time_start_general,
        time_config_create.lunch_time_end_general
    )
    if result["status"] == "false":
        return result

    # Handle existing config update
    if existing_config:
        for field, value in time_config_create.dict().items():
            setattr(existing_config, field, value)
        existing_config.updated_at = datetime.utcnow()

        db.query(LateMark).filter(LateMark.config_id == existing_config.id).delete()

        db.commit()
        db.refresh(existing_config)

        return {
            "status": "true",
            "message": "Time configuration updated successfully",
            "data": existing_config
        }

    # Duplicate check
    duplicate_check = db.execute(
        select(TimeConfig).where(
            TimeConfig.admin_id == time_config_create.admin_id,
            TimeConfig.shift_name == time_config_create.shift_name
        )
    ).scalars().first()

    if duplicate_check:
        raise HTTPException(status_code=400, detail="Duplicate record exists")

    new_time_config = TimeConfig(**time_config_create.dict(exclude={"late"}))
    db.add(new_time_config)
    db.commit()
    db.refresh(new_time_config)

    return {
        "status": "true",
        "message": "Time configuration added successfully",
        "data": new_time_config
    }




# def create_or_update_time_config(db: Session, time_config_create: TimeConfigCreate):
#     existing_config = db.execute(
#         select(TimeConfig).where(
#             TimeConfig.admin_id == time_config_create.admin_id
#         )
#     ).scalars().first()

#     if existing_config:
#         for field, value in time_config_create.dict().items():
#             setattr(existing_config, field, value)
        
#         existing_config.updated_at = datetime.utcnow()
#         db.commit()
#         db.refresh(existing_config)

#         return {
#             "status": "true",
#             "message": "Time configuration updated successfully",
#             "data": existing_config
#         }

#     # Check for duplicate with same shift_name
#     duplicate_check = db.execute(
#         select(TimeConfig).where(
#             TimeConfig.admin_id == time_config_create.admin_id,
#             TimeConfig.shift_name == time_config_create.shift_name
#         )
#     ).scalars().first()

#     if duplicate_check:
#         raise HTTPException(status_code=400, detail="Duplicate record exists")

#     # Create new config
#     new_time_config = TimeConfig(**time_config_create.dict())
#     db.add(new_time_config)
#     db.commit()
#     db.refresh(new_time_config)

#     return {
#         "status": "true",
#         "message": "Time configuration added successfully",
#         "data": new_time_config
#     }



# def create_or_update_time_config(db: Session, time_config_create: TimeConfigCreate):
#     existing_config = db.exec(
#         select(TimeConfig).where(
#             TimeConfig.admin_id == time_config_create.admin_id
#         )
#     ).first()

#     if existing_config:
        
#         for field, value in time_config_create.dict().items():
#             setattr(existing_config, field, value)
        
        
#         existing_config.updated_at = datetime.utcnow()
#         db.commit()
#         db.refresh(existing_config)

#         return {
#             "status": "true",
#             "message": "Time configuration updated successfully",
#             "data": existing_config
#         }
#     else:
        
#         duplicate_check = db.exec(
#             select(TimeConfig).where(
#                 TimeConfig.admin_id == time_config_create.admin_id,
#                 TimeConfig.shift_name == time_config_create.shift_name
#             )
#         ).all()

#         if duplicate_check:
#             raise HTTPException(status_code=400, detail="Duplicate record exists")

        
#         new_time_config = TimeConfig(**time_config_create.dict())
#         db.add(new_time_config)
#         db.commit()
#         db.refresh(new_time_config)

#         return {
#             "status": "true",
#             "message": "Time configuration added successfully",
#             "data": new_time_config
#         }
