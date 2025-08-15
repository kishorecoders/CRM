from typing import List
from fastapi import APIRouter, Depends, HTTPException, status,Header,Body
from sqlmodel import Session
from src.database import get_db
from src.AdminRoleCreation.models import AdminRoleCreation,AdminRoleCreationCreate,RoleInput
from src.AdminRoleCreation.service import create,get_all_role,get_role_by_admin_id,update,deactivate_role,delete_admin_role,get_role_detail_by_id
from src.parameter import get_token
from typing import Dict

from src.parameter import get_current_datetime

router = APIRouter()

@router.get("/")
def get_all_role_details(auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_all_role(db=db)
    
    return inner_get_plan(auth_token)


def convert_to_flat_model(data: RoleInput) -> AdminRoleCreationCreate:
    flat_data = {
        "admin_id": data.admin_id,
        "role_name": data.role_name,

        "sale_integration_read": data.sales.integration.read,
        "sale_integration_write": data.sales.integration.write,
        "sale_integration_edit": data.sales.integration.edit,
        "sale_integration_delete": data.sales.integration.delete,

        "sale_lead_read": data.sales.lead.read,
        "sale_lead_write": data.sales.lead.write,
        "sale_lead_edit": data.sales.lead.edit,
        "sale_lead_delete": data.sales.lead.delete,

        "sale_quotation_read": data.sales.quotation.read,
        "sale_quotation_write": data.sales.quotation.write,
        "sale_quotation_edit": data.sales.quotation.edit,
        "sale_quotation_delete": data.sales.quotation.delete,

        "sale_assign_employee_read": data.sales.assign_employee.read,
        "sale_assign_employee_write": data.sales.assign_employee.write,
        "sale_assign_employee_edit": data.sales.assign_employee.edit,
        "sale_assign_employee_delete": data.sales.assign_employee.delete,

        "sales_read": data.sales.sale.read,
        "sales_write": data.sales.sale.write,
        "sales_edit": data.sales.sale.edit,
        "sales_delete": data.sales.sale.delete,
        "sales_attendance": data.sales.sale.attendance,
        "sales_task": data.sales.sale.task,
        "sales_leave": data.sales.sale.leave,
        
        
        
        "project_manager_read" : data.project_manager.projectmanager.read,
        "project_manager_write" : data.project_manager.projectmanager.write,
        "project_manager_edit" : data.project_manager.projectmanager.edit,
        "project_manager_delete": data.project_manager.projectmanager.delete,

        "project_manager_jobcard_read": data.project_manager.jobcard.read,
        "project_manager_jobcard_write": data.project_manager.jobcard.write,
        "project_manager_jobcard_edit": data.project_manager.jobcard.edit,
        "project_manager_jobcard_delete": data.project_manager.jobcard.delete,

        "project_manager_orderhistory_read": data.project_manager.orderhistory.read,
        "project_manager_orderhistory_write": data.project_manager.orderhistory.write,
        "project_manager_orderhistory_edit": data.project_manager.orderhistory.edit,
        "project_manager_orderhistory_delete": data.project_manager.orderhistory.delete,

        "project_manager_upcomingorder_read": data.project_manager.upcomingorder.read,
        "project_manager_upcomingorder_write": data.project_manager.upcomingorder.write,
        "project_manager_upcomingorder_edit": data.project_manager.upcomingorder.edit,
        "project_manager_upcomingorder_delete": data.project_manager.upcomingorder.delete,



        "project_manager_allocatedwork_read": data.project_manager.allocatedwork.read,
        "project_manager_allocatedwork_write": data.project_manager.allocatedwork.write,
        "project_manager_allocatedwork_edit": data.project_manager.allocatedwork.edit,
        "project_manager_allocatedwork_delete": data.project_manager.allocatedwork.delete,


        "project_manager_designhandover_read": data.project_manager.designhandover.read,
        "project_manager_designhandover_write": data.project_manager.designhandover.write,
        "project_manager_designhandover_edit": data.project_manager.designhandover.edit,
        "project_manager_designhandover_delete": data.project_manager.designhandover.delete,


        "store_engineer_read": data.inventory.storeengineer.read,
        "store_engineer_write":data.inventory.storeengineer.write,
        "store_engineer_edit":data.inventory.storeengineer.edit,
        "store_engineer_delete":data.inventory.storeengineer.delete,


        "inventory_requestbyteam_read" : data.inventory.requestbyteam.read,
        "inventory_requestbyteam_write" : data.inventory.requestbyteam.write,
        "inventory_requestbyteam_edit" : data.inventory.requestbyteam.edit,
        "inventory_requestbyteam_delete": data.inventory.requestbyteam.delete,
 

        "inventory_upload_product_read" : data.inventory.uploadproduct.read,
        "inventory_upload_product_write" :  data.inventory.uploadproduct.write,
        "inventory_upload_product_edit" :  data.inventory.uploadproduct.edit,
        "inventory_upload_product_delete" :  data.inventory.uploadproduct.delete,


        "inventory_inword_read" : data.inventory.inword.read,
        "inventory_inword_write" : data.inventory.inword.write,
        "inventory_inword_edit" : data.inventory.inword.edit,
        "inventory_inword_delete" : data.inventory.inword.delete,


        "inventory_outword_read" : data.inventory.outword.read,
        "inventory_outword_write" : data.inventory.outword.write,
        "inventory_outword_edit" : data.inventory.outword.edit,
        "inventory_outword_delete" : data.inventory.outword.delete,



        "inventory_export_read" : data.inventory.export.read,
        "inventory_export_write" : data.inventory.export.write,
        "inventory_export_edit" : data.inventory.export.edit,
        "inventory_export_delete" : data.inventory.export.delete,

        "inventory_category_read" :  data.inventory.category.read,
        "inventory_category_write" :  data.inventory.category.write,
        "inventory_category_edit" : data.inventory.category.edit,
        "inventory_category_delete" : data.inventory.category.delete,


        "inventory_steps_read" : data.inventory.steps.read,
        "inventory_steps_write" : data.inventory.steps.write,
        "inventory_steps_edit" : data.inventory.steps.edit,
        "inventory_steps_delete" : data.inventory.steps.delete,


        "inventory_req_purchase_read" : data.inventory.reqpurchase.read,
        "inventory_req_purchase_write" : data.inventory.reqpurchase.write,
        "inventory_req_purchase_edit" : data.inventory.reqpurchase.edit,
        "inventory_req_purchase_delete" : data.inventory.reqpurchase.delete,

        "inventory_order_read" : data.inventory.order.read,
        "inventory_order_write" :data.inventory.order.write,
        "inventory_order_edit" : data.inventory.order.edit,
        "inventory_order_delete" : data.inventory.order.delete,



        "purchase_read" : data.purchase.purchase.read,
        "purchase_write" : data.purchase.purchase.write,
        "purchase_edit" : data.purchase.purchase.edit,
        "purchase_delete" : data.purchase.purchase.delete,


        "purchase_request_from_store_read" : data.purchase.requestfromstore.read,
        "purchase_request_from_store_write" : data.purchase.requestfromstore.write,
        "purchase_request_from_store_edit" : data.purchase.requestfromstore.edit,
        "purchase_request_from_store_delete" :  data.purchase.requestfromstore.delete,


        "purchase_issue_order_read" : data.purchase.issueorder.read,
        "purchase_issue_order_write" : data.purchase.issueorder.write,
        "purchase_issue_order_edit" : data.purchase.issueorder.edit,
        "purchase_issue_order_delete" : data.purchase.issueorder.delete,


        "purchase_vender_list_read" : data.purchase.venderlist.read,
        "purchase_vender_list_write" : data.purchase.venderlist.write,
        "purchase_vender_list_edit" : data.purchase.venderlist.edit,
        "purchase_vender_list_delete" : data.purchase.venderlist.delete,


        "purchase_order_history_read" : data.purchase.orderhistory.read,
        "purchase_order_history_write" : data.purchase.orderhistory.write,
        "purchase_order_history_edit" : data.purchase.orderhistory.edit,
        "purchase_order_history_delete" :data.purchase.orderhistory.delete,


        "purchase_inventory_alert_read" : data.purchase.inventoryalert.read,
        "purchase_inventory_alert_write" : data.purchase.inventoryalert.write,
        "purchase_inventory_alert_edit" : data.purchase.inventoryalert.edit,
        "purchase_inventory_alert_delete" : data.purchase.inventoryalert.delete,
        
        
        
        "purchase_grn_read" : data.purchase.grn.read,
        "purchase_grn_write" : data.purchase.grn.write,
        "purchase_grn_edit" : data.purchase.grn.edit,
        "purchase_grn_delete" : data.purchase.grn.delete,


        "dispatch_read" : data.dispatch.dispatch.read,
        "dispatch_write" : data.dispatch.dispatch.write,
        "dispatch_edit" : data.dispatch.dispatch.edit,
        "dispatch_delete" : data.dispatch.dispatch.delete,


        "dispatch_transport_read" : data.dispatch.transport.read,
        "dispatch_transport_write" : data.dispatch.transport.write,
        "dispatch_transport_edit" : data.dispatch.transport.edit,
        "dispatch_transport_delete" : data.dispatch.transport.delete,


        "dispatch_current_read" : data.dispatch.current.read,
        "dispatch_current_write" : data.dispatch.current.write,
        "dispatch_current_edit" : data.dispatch.current.edit,
        "dispatch_current_delete" : data.dispatch.current.delete,
        
        
        
        "dispatch_dashboard_read" : data.dispatch.dashboard.read,
        "dispatch_dashboard_write" : data.dispatch.dashboard.write,
        "dispatch_dashboard_edit" : data.dispatch.dashboard.edit,
        "dispatch_dashboard_delete" : data.dispatch.dashboard.delete,
        
        
        



        "account_read" : data.account.account.read,
        "account_write" :data.account.account.write,
        "account_edit" : data.account.account.edit,
        "account_delete" : data.account.account.delete,


        "employee_attendance_read" :  data.employee.attendance.read,
        "employee_attendance_write" : data.employee.attendance.write,
        "employee_attendance_edit" : data.employee.attendance.edit,
        "employee_attendance_delete" : data.employee.attendance.delete,

        "employee_leave_read": data.employee.leave.read,
        "employee_leave_write": data.employee.leave.write,
        "employee_leave_edit": data.employee.leave.edit,
        "employee_leave_delete": data.employee.leave.delete,

        "employee_task_read": data.employee.task.read,
        "employee_task_write": data.employee.task.write,
        "employee_task_edit": data.employee.task.edit,
        "employee_task_delete": data.employee.task.delete,

        "employee_rolecreation_read": data.employee.rolecreation.read,
        "employee_rolecreation_write": data.employee.rolecreation.write,
        "employee_rolecreation_edit": data.employee.rolecreation.edit,
        "employee_rolecreation_delete": data.employee.rolecreation.delete,

        "employee_roleassignment_read": data.employee.roleassignment.read,
        "employee_roleassignment_write": data.employee.roleassignment.write,
        "employee_roleassignment_edit": data.employee.roleassignment.edit,
        "employee_roleassignment_delete": data.employee.roleassignment.delete,


        "config_termandcondition_read": data.config.termandcondition.read,
        "config_termandcondition_write": data.config.termandcondition.write,
        "config_termandcondition_edit": data.config.termandcondition.edit,
        "config_termandcondition_delete": data.config.termandcondition.delete,

        "config_brochure_read": data.config.brochure.read,
        "config_brochure_write": data.config.brochure.write,
        "config_brochure_edit": data.config.brochure.edit,
        "config_brochure_delete": data.config.brochure.delete,

        "config_series_read": data.config.series.read,
        "config_series_write": data.config.series.write,
        "config_series_edit": data.config.series.edit,
        "config_series_delete": data.config.series.delete,

        "config_timeconfig_read": data.config.timeconfig.read,
        "config_timeconfig_write": data.config.timeconfig.write,
        "config_timeconfig_edit": data.config.timeconfig.edit,
        "config_timeconfig_delete": data.config.timeconfig.delete,


        "employee_read": data.employee.employee.read,
        "employee_write": data.employee.employee.write,
        "employee_edit": data.employee.employee.edit,
        "employee_delete": data.employee.employee.delete,

        "config_read": data.config.config.read,
        "config_write": data.config.config.write,
        "config_edit": data.config.config.edit,
        "config_delete": data.config.config.delete,

        "config_bank_read": data.config.bank.read,
        "config_bank_write": data.config.bank.write,
        "config_bank_edit": data.config.bank.edit,
        "config_bank_delete": data.config.bank.delete,
        
        
        
        
        
        
        "admin_mobile_read" : data.mobile_admin.mobileadmin.read,
        "admin_mobile_write" : data.mobile_admin.mobileadmin.write,
        "admin_mobile_edit" : data.mobile_admin.mobileadmin.edit,
        "admin_mobile_delete" : data.mobile_admin.mobileadmin.delete,
        
        
        'admin_mobile_attendance_read' : data.mobile_admin.mobileattendance.read,
        'admin_mobile_attendance_write' :data.mobile_admin.mobileattendance.write,
        'admin_mobile_attendance_edit' : data.mobile_admin.mobileattendance.edit,
        'admin_mobile_attendance_delete' : data.mobile_admin.mobileattendance.delete,
    
    
        'admin_mobile_task_read': data.mobile_admin.mobiletask.read,
        'admin_mobile_task_write':data.mobile_admin.mobiletask.write,
        'admin_mobile_task_edit': data.mobile_admin.mobiletask.edit,
        'admin_mobile_task_delete': data.mobile_admin.mobiletask.delete,
    
    
        'admin_mobile_leave_read': data.mobile_admin.mobileleave.read,
        'admin_mobile_leave_write': data.mobile_admin.mobileleave.write,
        'admin_mobile_leave_edit': data.mobile_admin.mobileleave.edit,
        'admin_mobile_leave_delete':data.mobile_admin.mobileleave.delete,
        
        
        'admin_mobile_lead_read':data.mobile_admin.mobilelead.read,
        'admin_mobile_lead_write': data.mobile_admin.mobilelead.write,
        'admin_mobile_lead_edit': data.mobile_admin.mobilelead.edit,
        'admin_mobile_lead_delete':data.mobile_admin.mobilelead.delete,

    }

    return AdminRoleCreationCreate(**flat_data)


@router.post("/")
def create_role_details(
    role_input: RoleInput,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    exist = db.query(AdminRoleCreation).filter(
        AdminRoleCreation.admin_id == role_input.admin_id,
        AdminRoleCreation.role_name == role_input.role_name
        ).first()
    if exist:
        return {"status": "false", "message": "Role Name Already Exist "}

    flat_model = convert_to_flat_model(role_input)
    
    
    if role_input.employe_id:
        created_by_type = "employee"
        admin_emp_id = role_input.employe_id
    else:
        created_by_type = "admin"
        admin_emp_id = role_input.admin_id

    data = flat_model.dict()
    data["created_by_type"] = created_by_type
    data["admin_emp_id"] = admin_emp_id

    db_admin_role_creation = AdminRoleCreation(**data)
    db.add(db_admin_role_creation)
    db.commit()
    db.refresh(db_admin_role_creation)

    return {
        "status": "true",
        "message": "Role Creation Details Added Successfully",
        "data": db_admin_role_creation
    }


    
@router.get("/ShowRoleCreation/{admin_id}")
def read_plan_by_id(admin_id: int, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
        def inner_get_plan(auth_token: str):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return get_role_by_admin_id(admin_id=admin_id, db=db)
    
        return inner_get_plan(auth_token)
     
@router.get("get_role_detail_by_id")
def get_role_detail(
    admin_id: int, 
    role_id: int, 
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), 
    db: Session = Depends(get_db)):

    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_role_detail_by_id(admin_id=admin_id, role_id=role_id,db=db)
    
    return inner_get_plan(auth_token)       

   
from sqlalchemy import func
   
@router.put("/update/{role_id}")
def update_role_details(
    role_id: int,
    role_input: RoleInput,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    existing_role = db.query(AdminRoleCreation).filter(AdminRoleCreation.id == role_id).first()
    if not existing_role:
        return {"status": "false", "message": "Role not found"}

    normalized_input_name = role_input.role_name.strip().lower()
    
    exist = db.query(AdminRoleCreation).filter(
        AdminRoleCreation.admin_id == role_input.admin_id,
        func.lower(func.trim(AdminRoleCreation.role_name)) == normalized_input_name,
        AdminRoleCreation.id != role_id  # exclude current role from the check
    ).first()
    
    if exist:
        return {"status": "false", "message": "Role Name Already Exist"}
        
    flat_model = convert_to_flat_model(role_input)

    if role_input.employe_id:
        updated_by_type = "employee"
        updated_admin_emp_id = role_input.employe_id
    else:
        updated_by_type = "admin"
        updated_admin_emp_id = role_input.admin_id

    data = flat_model.dict()
    data["updated_by_type"] = updated_by_type
    data["updated_admin_emp_id"] = updated_admin_emp_id
    data["updated_at"] = get_current_datetime()
    data["status"] = data.get("status") or existing_role.status or "active"

    for key, value in data.items():
        setattr(existing_role, key, value)

    db.commit()
    db.refresh(existing_role)

    return {
        "status": "true",
        "message": "Role Creation Details Updated Successfully",
        "data": existing_role
    }   

   
@router.post("/DeactivateRole/")
def Deactivate_role_by_admin_id(role_id: int = Body(...), authenticated_admin_id: int = Body(...), status: str = Body(...),auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
    def inner_get_plan(auth_token: str):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return deactivate_role(db=db, role_id=role_id, authenticated_admin_id=authenticated_admin_id, status=status)
    
    return inner_get_plan(auth_token)

@router.delete("/DeleteRole/{id}")
def delete_admin_role_details(id:int,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db:Session=Depends(get_db)):
       def inner_get_plan(auth_token: str):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return delete_admin_role(id=id,db=db)
    
       return inner_get_plan(auth_token)