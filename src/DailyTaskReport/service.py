from sqlmodel import Session
from .models import DailyReport , ReportRequestCreate , ReportRequestCreatelist, ReportRequestGet , ReportRequestDelete,ReportRequestUpdate
from src.EmployeeTasks.models import TaskRequest
from src.EmployeeTasks.service import get_task_list


def create_report(db: Session, report_create: ReportRequestCreate):

    report_data = report_create.dict()
    new_report = DailyReport(**report_data)

    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    return {
        "status": "true",
        "message": "Task created successfully",
        "data": new_report
    }


def create_multi_report(db: Session, paylode: ReportRequestCreatelist):

    for report_create in paylode.reports:

        report_data = report_create.dict()
        new_report = DailyReport(**report_data)

        db.add(new_report)
        db.commit()
        db.refresh(new_report)

    return {
        "status": "true",
        "message": "Reports created successfully",
    }

from src.cre_upd_name import get_creator_info


def get_report(db: Session, getpaylode: ReportRequestGet):
    query = db.query(DailyReport).filter(
        DailyReport.admin_id == getpaylode.admin_id
    ).order_by(DailyReport.id.desc())

    if getpaylode.employee_id:
        query = query.filter(DailyReport.employee_id == getpaylode.employee_id)
    if getpaylode.task_id:
        query = query.filter(DailyReport.task_id == getpaylode.task_id)

    reports = query.all()

    result = []

    for report in reports:
        data = report.__dict__.copy()
        created_by_type = None
        admin_emp_id = None

        if report.employee_id not in ["" , None]:
            created_by_type = "employee"
            admin_emp_id = report.employee_id
        else:
            created_by_type = "admin"
            admin_emp_id = report.admin_id    

        creater = get_creator_info(admin_emp_id=admin_emp_id , created_by_type=created_by_type ,db=db)

        # task = db.query(TaskRequest).filter(TaskRequest.id == int(report.task_id)).first()
        task = get_task_list(admin_id=report.admin_id , task_id=report.task_id , db=db)
        data['creater_info'] = creater
        if task:
            data['task'] = task[0]
        else:
            data['task'] = None
        
        result.append(data)



    return {
        "status": "true",
        "message": "Reports fetched successfully",
        "data": result
    }


def delete_report(db: Session, deletepaylode: ReportRequestDelete):
    query = db.query(DailyReport).filter(
        DailyReport.id == int(deletepaylode.report_id),
        DailyReport.admin_id == deletepaylode.admin_id
    )

    if deletepaylode.employee_id:
        query = query.filter(DailyReport.employee_id == deletepaylode.employee_id)

    report = query.first()

    if not report:
        return {
            "status": "false",
            "message": "Report not found",
            "data": None
        }

    db.delete(report)
    db.commit()

    return {
        "status": "true",
        "message": "Report deleted successfully",
        "data": {
            "id": deletepaylode.report_id
        }
    }
    

def update_report(db: Session, updatepaylode: ReportRequestUpdate):
    query = db.query(DailyReport).filter(
        DailyReport.id == int(updatepaylode.report_id),
        DailyReport.admin_id == updatepaylode.admin_id
    )

    if updatepaylode.employee_id:
        query = query.filter(DailyReport.employee_id == updatepaylode.employee_id)

    report = query.first()

    if not report:
        return {
            "status": "false",
            "message": "Report not found",
            "data": None
        }
    
    report.task_id = updatepaylode.task_id

    db.add(report)
    db.commit()

    return {
        "status": "true",
        "message": "Report updated successfully",
        "data": report
    }



