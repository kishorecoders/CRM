from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
from src.parameter import get_current_datetime

class AdminRoleCreationBase(SQLModel):
    admin_id : int = Field(nullable=False,default=0)
    employe_id : Optional[str] = Field(nullable=True,default=None)
    role_name : str = Field(nullable=False,default=0)
    admin_read : int = Field(nullable=False,default=0)
    admin_write : int = Field(nullable=False,default=0)
    admin_edit : int = Field(nullable=False,default=0)
    admin_delete : int = Field(nullable=False,default=0) 
    sales_read : int = Field(nullable=False,default=0)
    sales_write : int = Field(nullable=False,default=0)
    sales_edit : int = Field(nullable=False,default=0)
    sales_delete : int = Field(nullable=False,default=0) 
    sales_attendance : int =Field(nullable=True,default=0)
    sales_task : int =Field(nullable=True,default=0)
    sales_leave : int =Field(nullable=True,default=0)
    project_manager_read : int = Field(nullable=False,default=0)
    project_manager_write : int = Field(nullable=False,default=0)
    project_manager_edit : int = Field(nullable=False,default=0)
    project_manager_delete : int = Field(nullable=False,default=0) 
    store_engineer_read : int = Field(nullable=False,default=0)
    store_engineer_write : int = Field(nullable=False,default=0)
    store_engineer_edit : int = Field(nullable=False,default=0)
    store_engineer_delete : int = Field(nullable=False,default=0) 
    purchase_read : int = Field(nullable=False,default=0)
    purchase_write : int = Field(nullable=False,default=0)
    purchase_edit : int = Field(nullable=False,default=0)
    purchase_delete : int = Field(nullable=False,default=0)
    dispatch_read : int = Field(nullable=False,default=0)
    dispatch_write : int = Field(nullable=False,default=0)
    dispatch_edit : int = Field(nullable=False,default=0)
    dispatch_delete : int = Field(nullable=False,default=0) 
    account_read : int = Field(nullable=False,default=0)
    account_write : int = Field(nullable=False,default=0)
    account_edit : int = Field(nullable=False,default=0)
    account_delete : int = Field(nullable=False,default=0) 
    customer_read : int = Field(nullable=False,default=0)
    customer_write : int = Field(nullable=False,default=0)
    customer_edit : int = Field(nullable=False,default=0)
    customer_delete : int = Field(nullable=False,default=0)
    
    employee_read : int = Field(nullable=False,default=0)
    employee_write : int = Field(nullable=False,default=0)
    employee_edit : int = Field(nullable=False,default=0)
    employee_delete : int = Field(nullable=False,default=0)

    config_read : int = Field(nullable=False,default=0)
    config_write : int = Field(nullable=False,default=0)
    config_edit : int = Field(nullable=False,default=0)
    config_delete : int = Field(nullable=False,default=0)    
    

    config_bank_read: int = Field(nullable=True, default=0)
    config_bank_write: int = Field(nullable=True, default=0)
    config_bank_edit: int = Field(nullable=True, default=0)
    config_bank_delete: int = Field(nullable=True, default=0)    

    status : str = Field(nullable=False,default='True')
    status_update_read : int = Field(nullable=False,default=0)
    status_update_write : int = Field(nullable=False,default=0)
    status_update_edit : int = Field(nullable=False,default=0)
    status_update_delete : int = Field(nullable=False,default=0)
    
    
    sale_integration_read : int =Field(nullable=True,default=0)
    sale_integration_write : int = Field(nullable=True,default=0)
    sale_integration_edit : int = Field(nullable=True,default=0)
    sale_integration_delete : int = Field(nullable=True,default=0)

    sale_lead_read : int = Field(nullable=True,default=0)
    sale_lead_write : int = Field(nullable=True,default=0)
    sale_lead_edit : int = Field(nullable=True,default=0)
    sale_lead_delete : int = Field(nullable=True,default=0)

    sale_quotation_read : int = Field(nullable=True,default=0)
    sale_quotation_write : int = Field(nullable=True,default=0)
    sale_quotation_edit : int = Field(nullable=True,default=0)
    sale_quotation_delete : int = Field(nullable=True,default=0)

    sale_assign_employee_read : int = Field(nullable=True,default=0)
    sale_assign_employee_write : int = Field(nullable=True,default=0)
    sale_assign_employee_edit : int = Field(nullable=True,default=0)
    sale_assign_employee_delete : int = Field(nullable=True,default=0) 

    project_manager_jobcard_read : int = Field(nullable=True,default=0)
    project_manager_jobcard_write : int = Field(nullable=True,default=0)
    project_manager_jobcard_edit : int = Field(nullable=True,default=0)
    project_manager_jobcard_delete : int = Field(nullable=True,default=0)


    project_manager_orderhistory_read : int = Field(nullable=True,default=0)
    project_manager_orderhistory_write : int = Field(nullable=True,default=0)
    project_manager_orderhistory_edit : int = Field(nullable=True,default=0)
    project_manager_orderhistory_delete : int = Field(nullable=True,default=0)


    project_manager_upcomingorder_read : int = Field(nullable=True,default=0)
    project_manager_upcomingorder_write : int = Field(nullable=True,default=0)
    project_manager_upcomingorder_edit : int = Field(nullable=True,default=0)
    project_manager_upcomingorder_delete : int = Field(nullable=True,default=0)



    project_manager_allocatedwork_read : int = Field(nullable=True,default=0)
    project_manager_allocatedwork_write : int = Field(nullable=True,default=0)
    project_manager_allocatedwork_edit : int = Field(nullable=True,default=0)
    project_manager_allocatedwork_delete : int = Field(nullable=True,default=0)


    employee_attendance_read : int = Field(nullable=True,default=0)
    employee_attendance_write : int = Field(nullable=True,default=0)
    employee_attendance_edit : int = Field(nullable=True,default=0)
    employee_attendance_delete : int = Field(nullable=True,default=0)


    employee_roleassignment_read: int = Field(nullable=True, default=0)
    employee_roleassignment_write: int = Field(nullable=True, default=0)
    employee_roleassignment_edit: int = Field(nullable=True, default=0)
    employee_roleassignment_delete: int = Field(nullable=True, default=0)



    employee_rolecreation_read: int = Field(nullable=True, default=0)
    employee_rolecreation_write: int = Field(nullable=True, default=0)
    employee_rolecreation_edit: int = Field(nullable=True, default=0)
    employee_rolecreation_delete: int = Field(nullable=True, default=0)



    employee_task_read: int = Field(nullable=True, default=0)
    employee_task_write: int = Field(nullable=True, default=0)
    employee_task_edit: int = Field(nullable=True, default=0)
    employee_task_delete: int = Field(nullable=True, default=0)



    employee_leave_read: int = Field(nullable=True, default=0)
    employee_leave_write: int = Field(nullable=True, default=0)
    employee_leave_edit: int = Field(nullable=True, default=0)
    employee_leave_delete: int = Field(nullable=True, default=0)
    
    
    
    
    
    
    admin_mobile_read : int = Field(nullable=False,default=0)
    admin_mobile_write : int = Field(nullable=False,default=0)
    admin_mobile_edit : int = Field(nullable=False,default=0)
    admin_mobile_delete : int = Field(nullable=False,default=0)
    
    
    
    
    admin_mobile_attendance_read : int = Field(nullable=True,default=0)
    admin_mobile_attendance_write : int = Field(nullable=True,default=0)
    admin_mobile_attendance_edit : int = Field(nullable=True,default=0)
    admin_mobile_attendance_delete : int = Field(nullable=True,default=0)


    admin_mobile_task_read: int = Field(nullable=True, default=0)
    admin_mobile_task_write: int = Field(nullable=True, default=0)
    admin_mobile_task_edit: int = Field(nullable=True, default=0)
    admin_mobile_task_delete: int = Field(nullable=True, default=0)



    admin_mobile_leave_read: int = Field(nullable=True, default=0)
    admin_mobile_leave_write: int = Field(nullable=True, default=0)
    admin_mobile_leave_edit: int = Field(nullable=True, default=0)
    admin_mobile_leave_delete: int = Field(nullable=True, default=0)
    
    
    admin_mobile_lead_read: int = Field(nullable=True, default=0)
    admin_mobile_lead_write: int = Field(nullable=True, default=0)
    admin_mobile_lead_edit: int = Field(nullable=True, default=0)
    admin_mobile_lead_delete: int = Field(nullable=True, default=0)
    
    
    
    
    
    
    
    
    
    



    config_termandcondition_read: int = Field(nullable=True, default=0)
    config_termandcondition_write: int = Field(nullable=True, default=0)
    config_termandcondition_edit: int = Field(nullable=True, default=0)
    config_termandcondition_delete: int = Field(nullable=True, default=0)

    config_brochure_read: int = Field(nullable=True, default=0)
    config_brochure_write: int = Field(nullable=True, default=0)
    config_brochure_edit: int = Field(nullable=True, default=0)
    config_brochure_delete: int = Field(nullable=True, default=0)

    config_series_read: int = Field(nullable=True, default=0)
    config_series_write: int = Field(nullable=True, default=0)
    config_series_edit: int = Field(nullable=True, default=0)
    config_series_delete: int = Field(nullable=True, default=0)

    config_timeconfig_read: int = Field(nullable=True, default=0)
    config_timeconfig_write: int = Field(nullable=True, default=0)
    config_timeconfig_edit: int = Field(nullable=True, default=0)
    config_timeconfig_delete: int = Field(nullable=True, default=0)



    project_manager_designhandover_read : int = Field(nullable=True,default=0)
    project_manager_designhandover_write : int = Field(nullable=True,default=0)
    project_manager_designhandover_edit : int = Field(nullable=True,default=0)
    project_manager_designhandover_delete : int = Field(nullable=True,default=0)


    purchase_request_from_store_read : int = Field(nullable=True,default=0)
    purchase_request_from_store_write : int = Field(nullable=True,default=0)
    purchase_request_from_store_edit : int = Field(nullable=True,default=0)
    purchase_request_from_store_delete : int = Field(nullable=True,default=0)


    purchase_issue_order_read : int = Field(nullable=True,default=0)
    purchase_issue_order_write : int = Field(nullable=True,default=0)
    purchase_issue_order_edit : int = Field(nullable=True,default=0)
    purchase_issue_order_delete : int = Field(nullable=True,default=0)


    purchase_vender_list_read : int = Field(nullable=True,default=0)
    purchase_vender_list_write : int = Field(nullable=True,default=0)
    purchase_vender_list_edit : int = Field(nullable=True,default=0)
    purchase_vender_list_delete : int = Field(nullable=True,default=0)


    purchase_order_history_read : int = Field(nullable=True,default=0)
    purchase_order_history_write : int = Field(nullable=True,default=0)
    purchase_order_history_edit : int = Field(nullable=True,default=0)
    purchase_order_history_delete : int = Field(nullable=True,default=0)


    purchase_inventory_alert_read : int = Field(nullable=True,default=0)
    purchase_inventory_alert_write : int = Field(nullable=True,default=0)
    purchase_inventory_alert_edit : int = Field(nullable=True,default=0)
    purchase_inventory_alert_delete : int = Field(nullable=True,default=0)
    
    
    purchase_grn_read : int = Field(nullable=True,default=0)
    purchase_grn_write : int = Field(nullable=True,default=0)
    purchase_grn_edit : int = Field(nullable=True,default=0)
    purchase_grn_delete : int = Field(nullable=True,default=0)


    inventory_upload_product_read : int = Field(nullable=True,default=0)
    inventory_upload_product_write : int = Field(nullable=True,default=0)
    inventory_upload_product_edit : int = Field(nullable=True,default=0)
    inventory_upload_product_delete : int = Field(nullable=True,default=0)

    inventory_requestbyteam_read : int = Field(nullable=True,default=0)
    inventory_requestbyteam_write : int = Field(nullable=True,default=0)
    inventory_requestbyteam_edit : int = Field(nullable=True,default=0)
    inventory_requestbyteam_delete : int = Field(nullable=True,default=0)


    inventory_inword_read : int = Field(nullable=True,default=0)
    inventory_inword_write : int = Field(nullable=True,default=0)
    inventory_inword_edit : int = Field(nullable=True,default=0)
    inventory_inword_delete : int = Field(nullable=True,default=0)


    inventory_outword_read : int = Field(nullable=True,default=0)
    inventory_outword_write : int = Field(nullable=True,default=0)
    inventory_outword_edit : int = Field(nullable=True,default=0)
    inventory_outword_delete : int = Field(nullable=True,default=0)



    inventory_export_read : int = Field(nullable=True,default=0)
    inventory_export_write : int = Field(nullable=True,default=0)
    inventory_export_edit : int = Field(nullable=True,default=0)
    inventory_export_delete : int = Field(nullable=True,default=0)

    inventory_category_read : int = Field(nullable=True,default=0)
    inventory_category_write : int = Field(nullable=True,default=0)
    inventory_category_edit : int = Field(nullable=True,default=0)
    inventory_category_delete : int = Field(nullable=True,default=0)


    inventory_steps_read : int = Field(nullable=True,default=0)
    inventory_steps_write : int = Field(nullable=True,default=0)
    inventory_steps_edit : int = Field(nullable=True,default=0)
    inventory_steps_delete : int = Field(nullable=True,default=0)


    inventory_req_purchase_read : int = Field(nullable=True,default=0)
    inventory_req_purchase_write : int = Field(nullable=True,default=0)
    inventory_req_purchase_edit : int = Field(nullable=True,default=0)
    inventory_req_purchase_delete : int = Field(nullable=True,default=0)


    inventory_order_read : int = Field(nullable=True,default=0)
    inventory_order_write : int = Field(nullable=True,default=0)
    inventory_order_edit : int = Field(nullable=True,default=0)
    inventory_order_delete : int = Field(nullable=True,default=0)


    dispatch_transport_read : int = Field(nullable=True,default=0)
    dispatch_transport_write : int = Field(nullable=True,default=0)
    dispatch_transport_edit : int = Field(nullable=True,default=0)
    dispatch_transport_delete : int = Field(nullable=True,default=0)

    
    dispatch_current_read : int = Field(nullable=True,default=0)
    dispatch_current_write : int = Field(nullable=True,default=0)
    dispatch_current_edit : int = Field(nullable=True,default=0)
    dispatch_current_delete : int = Field(nullable=True,default=0)
    
    dispatch_dashboard_read : int = Field(nullable=True,default=0)
    dispatch_dashboard_write : int = Field(nullable=True,default=0)
    dispatch_dashboard_edit : int = Field(nullable=True,default=0)
    dispatch_dashboard_delete : int = Field(nullable=True,default=0)
    
    
    task_manager_read : int = Field(nullable=True,default=0)
    task_manager_write : int = Field(nullable=True,default=0)
    task_manager_edit : int = Field(nullable=True,default=0)
    task_manager_delete : int = Field(nullable=True,default=0)
    
    
    created_by_type : Optional[str] = Field(nullable=True,default=None)
    admin_emp_id : Optional[str] = Field(nullable=True,default=None)

    updated_by_type : Optional[str] = Field(nullable=True,default=None)
    updated_admin_emp_id : Optional[str] = Field(nullable=True,default=None)

    
    
    
    
    
class AdminRoleCreation(AdminRoleCreationBase,table = True):
    __tablename__ = "admin_role_creation"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    ccreated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class AdminRoleCreationCreate(BaseModel):
    admin_id : int = 0
    employe_id : Optional[str] = None
    role_name : Optional[str] = None
    admin_read : int = 0
    admin_write : int = 0
    admin_edit : int = 0
    admin_delete : int = 0 
    sales_read : int = 0
    sales_write : int = 0
    sales_edit : int = 0
    sales_delete : int = 0 
    sales_attendance : int = 0
    sales_task : int = 0
    sales_leave : int = 0
    project_manager_read : int = 0
    project_manager_write : int = 0
    project_manager_edit : int = 0
    project_manager_delete : int = 0 
    store_engineer_read : int = 0
    store_engineer_write : int = 0
    store_engineer_edit : int = 0
    store_engineer_delete : int = 0 
    purchase_read : int = 0
    purchase_write : int = 0
    purchase_edit : int = 0
    purchase_delete : int = 0
    dispatch_read : int = 0
    dispatch_write : int = 0
    dispatch_edit : int = 0
    dispatch_delete : int = 0 
    account_read : int = 0
    account_write : int = 0
    account_edit : int = 0
    account_delete : int = 0 

    customer_read : int = 0
    customer_write : int = 0
    customer_edit : int = 0
    customer_delete : int = 0

    
    employee_read : int = 0
    employee_write : int = 0
    employee_edit : int = 0
    employee_delete : int = 0

    config_read : int = 0
    config_write : int = 0
    config_edit : int = 0
    config_delete : int = 0

    status : Optional[str] = None
    status_update_read : int = 0
    status_update_write : int = 0
    status_update_edit : int = 0
    status_update_delete : int = 0


    sale_integration_read : int = 0
    sale_integration_write : int = 0
    sale_integration_edit : int = 0
    sale_integration_delete : int = 0

    sale_lead_read : int = 0
    sale_lead_write : int = 0
    sale_lead_edit : int = 0
    sale_lead_delete : int = 0

    sale_quotation_read : int = 0
    sale_quotation_write : int = 0
    sale_quotation_edit : int = 0
    sale_quotation_delete : int = 0

    sale_assign_employee_read : int = 0
    sale_assign_employee_write : int = 0
    sale_assign_employee_edit : int = 0
    sale_assign_employee_delete : int = 0 

    project_manager_jobcard_read : int = 0
    project_manager_jobcard_write : int = 0
    project_manager_jobcard_edit : int = 0
    project_manager_jobcard_delete : int = 0
    
    


    project_manager_orderhistory_read : int = 0
    project_manager_orderhistory_write : int = 0
    project_manager_orderhistory_edit : int = 0
    project_manager_orderhistory_delete : int = 0


    project_manager_upcomingorder_read : int = 0
    project_manager_upcomingorder_write : int = 0
    project_manager_upcomingorder_edit : int = 0
    project_manager_upcomingorder_delete : int = 0


    project_manager_allocatedwork_read : int = 0
    project_manager_allocatedwork_write : int = 0
    project_manager_allocatedwork_edit : int = 0
    project_manager_allocatedwork_delete : int = 0


    employee_attendance_read : int = 0
    employee_attendance_write : int = 0
    employee_attendance_edit : int = 0
    employee_attendance_delete : int = 0


    employee_roleassignment_read: int = 0
    employee_roleassignment_write: int = 0
    employee_roleassignment_edit: int = 0
    employee_roleassignment_delete: int = 0



    employee_rolecreation_read: int = 0
    employee_rolecreation_write: int = 0
    employee_rolecreation_edit: int = 0
    employee_rolecreation_delete: int = 0



    employee_task_read: int = 0
    employee_task_write: int = 0
    employee_task_edit: int = 0
    employee_task_delete: int = 0



    employee_leave_read: int = 0
    employee_leave_write: int = 0
    employee_leave_edit: int = 0
    employee_leave_delete: int = 0



    config_termandcondition_read: int = 0
    config_termandcondition_write: int = 0
    config_termandcondition_edit: int = 0
    config_termandcondition_delete: int = 0

    config_brochure_read: int = 0
    config_brochure_write: int = 0
    config_brochure_edit: int = 0
    config_brochure_delete: int = 0

    config_series_read: int = 0
    config_series_write: int = 0
    config_series_edit: int = 0
    config_series_delete: int = 0

    config_timeconfig_read: int = 0
    config_timeconfig_write: int = 0
    config_timeconfig_edit: int = 0
    config_timeconfig_delete: int = 0

    config_bank_read: int = 0
    config_bank_write: int = 0
    config_bank_edit: int = 0
    config_bank_delete: int = 0


    project_manager_designhandover_read : int = 0
    project_manager_designhandover_write : int = 0
    project_manager_designhandover_edit : int = 0
    project_manager_designhandover_delete : int = 0


    purchase_request_from_store_read : int = 0
    purchase_request_from_store_write : int = 0
    purchase_request_from_store_edit : int = 0
    purchase_request_from_store_delete : int = 0


    purchase_issue_order_read : int = 0
    purchase_issue_order_write : int = 0
    purchase_issue_order_edit : int = 0
    purchase_issue_order_delete : int = 0


    purchase_vender_list_read : int = 0
    purchase_vender_list_write : int = 0
    purchase_vender_list_edit : int = 0
    purchase_vender_list_delete : int = 0


    purchase_order_history_read : int = 0
    purchase_order_history_write : int = 0
    purchase_order_history_edit : int = 0
    purchase_order_history_delete : int = 0


    purchase_inventory_alert_read : int = 0
    purchase_inventory_alert_write : int = 0
    purchase_inventory_alert_edit : int = 0
    purchase_inventory_alert_delete : int = 0
    
    
    
    purchase_grn_read : int = 0
    purchase_grn_write : int = 0
    purchase_grn_edit : int = 0
    purchase_grn_delete : int = 0


    inventory_upload_product_read : int = 0
    inventory_upload_product_write : int = 0
    inventory_upload_product_edit : int = 0
    inventory_upload_product_delete : int = 0

    inventory_requestbyteam_read : int = 0
    inventory_requestbyteam_write : int = 0
    inventory_requestbyteam_edit : int = 0
    inventory_requestbyteam_delete : int = 0


    inventory_inword_read : int = 0
    inventory_inword_write : int = 0
    inventory_inword_edit : int = 0
    inventory_inword_delete : int = 0


    inventory_outword_read : int = 0
    inventory_outword_write : int = 0
    inventory_outword_edit : int = 0
    inventory_outword_delete : int = 0



    inventory_export_read : int = 0
    inventory_export_write : int = 0
    inventory_export_edit : int = 0
    inventory_export_delete : int = 0

    inventory_category_read : int = 0
    inventory_category_write : int = 0
    inventory_category_edit : int = 0
    inventory_category_delete : int = 0


    inventory_steps_read : int = 0
    inventory_steps_write : int = 0
    inventory_steps_edit : int = 0
    inventory_steps_delete : int = 0


    inventory_req_purchase_read : int = 0
    inventory_req_purchase_write : int = 0
    inventory_req_purchase_edit : int = 0
    inventory_req_purchase_delete : int = 0


    inventory_order_read : int = 0
    inventory_order_write : int = 0
    inventory_order_edit : int = 0
    inventory_order_delete : int = 0


    dispatch_transport_read : int = 0
    dispatch_transport_write : int = 0
    dispatch_transport_edit : int = 0
    dispatch_transport_delete : int = 0


    dispatch_current_read : int = 0
    dispatch_current_write : int = 0
    dispatch_current_edit : int = 0
    dispatch_current_delete : int = 0
    
    
    dispatch_dashboard_read : int = 0
    dispatch_dashboard_write : int = 0
    dispatch_dashboard_edit : int = 0
    dispatch_dashboard_delete : int = 0
    
    


    task_manager_read : int = 0
    task_manager_write : int = 0
    task_manager_edit : int = 0
    task_manager_delete : int = 0
    
    
    
    
    
    admin_mobile_read : int = 0
    admin_mobile_write : int = 0
    admin_mobile_edit : int = 0
    admin_mobile_delete : int = 0
    
    
    admin_mobile_attendance_read : int = 0
    admin_mobile_attendance_write : int = 0
    admin_mobile_attendance_edit : int = 0
    admin_mobile_attendance_delete : int = 0


    admin_mobile_task_read: int = 0
    admin_mobile_task_write: int = 0
    admin_mobile_task_edit: int = 0
    admin_mobile_task_delete: int = 0


    admin_mobile_leave_read: int = 0
    admin_mobile_leave_write: int = 0
    admin_mobile_leave_edit: int = 0
    admin_mobile_leave_delete: int = 0
    
    
    admin_mobile_lead_read: int = 0
    admin_mobile_lead_write: int = 0
    admin_mobile_lead_edit: int = 0
    admin_mobile_lead_delete: int = 0



class AdminRoleCreationRead(AdminRoleCreationBase):
    id : int    
    
    
    
    


class PermissionSet(BaseModel):
    read: int = 0
    write: int = 0
    edit: int = 0
    delete: int = 0

# Sales section: sale has additional fields
class SalePermissionSet(PermissionSet):
    attendance: Optional[int] = 0
    task: Optional[int] = 0
    leave: Optional[int] = 0

# Sales category
class SalesPermissions(BaseModel):
    integration: PermissionSet
    lead: PermissionSet
    quotation: PermissionSet
    assign_employee: PermissionSet
    sale: SalePermissionSet  # Only this has the 3 extra fields

# Project Manager category
class ProjectManagerPermissions(BaseModel):
    projectmanager:PermissionSet
    jobcard: PermissionSet
    orderhistory: PermissionSet
    upcomingorder: PermissionSet
    designhandover: PermissionSet
    allocatedwork: PermissionSet


class InventoryPermissions(BaseModel):
    requestbyteam:PermissionSet
    storeengineer : PermissionSet
    uploadproduct : PermissionSet
    inword : PermissionSet
    outword: PermissionSet
    outword: PermissionSet
    export: PermissionSet
    category: PermissionSet
    steps: PermissionSet
    reqpurchase: PermissionSet
    order: PermissionSet


class PurchasePermissions(BaseModel):
    purchase : PermissionSet
    requestfromstore : PermissionSet
    issueorder:PermissionSet
    venderlist:PermissionSet
    orderhistory:PermissionSet
    inventoryalert:PermissionSet
    grn:PermissionSet


class DispatchPermissions(BaseModel):
    dispatch : PermissionSet
    transport: PermissionSet
    current : PermissionSet
    dashboard : PermissionSet


class AccountPermissions(BaseModel):
    account : PermissionSet


class EmployeePermissions(BaseModel):
    employee : PermissionSet
    attendance : PermissionSet
    leave : PermissionSet
    task : PermissionSet
    rolecreation : PermissionSet
    roleassignment : PermissionSet
    
    
    
class MobileAdminPermissions(BaseModel):
    mobileadmin : PermissionSet
    mobileattendance : PermissionSet
    mobileleave : PermissionSet
    mobiletask : PermissionSet
    mobilelead : PermissionSet
       
    
    
    
    

class ConfigPermissions(BaseModel):
    config : PermissionSet
    termandcondition : PermissionSet
    brochure : PermissionSet
    series : PermissionSet
    timeconfig : PermissionSet
    bank : PermissionSet

class TaskManagerPermissions(BaseModel):
    taskmanager : PermissionSet


    

# Top-level input model
class RoleInput(BaseModel):
    admin_id: int
    employe_id : Optional[str] = None
    role_name: str
    sales: SalesPermissions
    project_manager: ProjectManagerPermissions
    inventory :  InventoryPermissions
    purchase : PurchasePermissions
    dispatch : DispatchPermissions
    account : AccountPermissions
    #task_manager : TaskManagerPermissions
    employee : EmployeePermissions
    config : ConfigPermissions
    mobile_admin : MobileAdminPermissions


