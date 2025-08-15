from fastapi.routing import APIRouter
from src.SuperAdminLogin.views import router as super_admin_router
from src.SuperAdminPlanAndPrice.views import router as super_admin_plan_price_router
from src.SuperAdminUserAddNew.views import router as super_admin_user_add_new_router
from src.SuperAdminReffralAndPlan.views import router as super_admin_reffral_plan_router
from src.SuperAdminBilling.views import router as super_admin_billing_router
from src.SuperAdminEnquiry.views import router as super_admin_enquiry_router
from src.AdminLogin.views import router as admin_login_router
from src.AdminAddEmployee.views import router as admin_add_employee_router
from src.AdminRoleCreation.views import router as admin_role_creation_router
from src.AdminAssignRoleEmployee.views import router as admin_assign_role_employee_router
from src.AdminSales.views import router as admin_sales_router
from src.Activity.views import router as activity_center_router
from src.Meetingplanned.views import router as meeting_planned_router
from src.EmployeeLogin.views import router as employee_login_router
from src.StoreManagerProduct.views import router as store_manager_product_router
from src.StoreManagerService.views import router as store_manager_service_router
from src.Category.views import router as catagory_router
from src.SubCategory.views import router as sub_catagory_router
from src.vendor.views import router as vendor_router
from src.PurchaseOrderIssue.views import router as purchase_order_issue_router
from src.ProjectManagerOrder.views import router as project_manager_order_router
from src.Inventoryoutward.views import router as inventory_outward_router
from src.Productwisestock.views import router as product_wise_stock_router
from src.StoreManagerPurchase.views import router as store_manager_purchase_router
from src.PurchaseManager.views import router as purchase_manager_router
from src.Ocr.views import router as ocr_router
from src.Settings.views import router as settings_router
from src.SettingsFiles.views import router as settings_files_router
from src.Quotation.views import router as quotation_router
from src.Invoice.views import router as invoice_router
from src.Leads.views import router as leads_router
from src.Integration.views import router as integration_router
from src.RoleAssignByLevel.views import router as role_assign_by_level_router
from src.EmployeeAssignRequest.views import router as employee_asssign_request
from src.Attendance.views import router as attendance
from src.EmployeeFiles.views import router as employee_files
from src.EmployeeTasks.views import router as employee_tasks
from src.TimeConfig.views import router as time_config
from src.ActivityComment.views import router as activity_comment
from src.EmployeeLeave.views import router as employee_leave
from src.PublicHoliday.views import router as public_holiday
from src.QuotationTemplate.views import router as quotation_template
from src.QuotationProduct.views import router as quotation_product
from src.QuotationProductEmployee.views import router as quotation_product_employee
from src.TermAndConditions.views import router as term_and_condition
from src.Brouncher.views import router as brouncher
from src.Production.views import router as production
from src.ProductionRequest.views import router as production_request
from src.LeadReminder.views import router as lead_reminder
from src.DispatchVendor.views import router as dispatch_vendor
from src.CreateDispatch.views import router as create_dispatch
from src.DeliveryChallan.views import router as delivery_challan
from src.ProductStages.views import router as product_stages
from src.ProductSteps.views import router as product_steps
from src.StepItems.views import router as step_items
from src.LateMark.views import router as late_mark
from src.OrderInProcess.views import router as order_in_process
from src.DesignHandover.views import router as design_handover
from src.QuotationCustomer.views import router as quotation_customer
from src.QuotationSeries.views import router as quotation_series
from src.Bank.views import router as bank
from src.PaymentTerm.views import router as payment_term
from src.Account.views import router as account
from src.AddPayment.views import router as add_payment
from src.QuotationSubProductEmployee.views import router as sub_product
from src.CheckPoint.views import router as checkPoint
from src.ProductTemplates.views import router as productTemplates
#from src.ProjectManagerResourseFile.views import router as ProjectManagerResourseFile
from src.ProductTemplates_key.views import router as ProductTemplates_key

from src.StoreCheckPoint.views import router as storeCheckPoint
from src.FaceBook.views import router as FaceBook
from src.PurchaseOrderProduct.views import router as PurchaseOrderProduct
from src.ProjectManagerResourseFile.views import router as ProjectManagerResourseFile
from src.CreateDispatchInfo.views import router as CreateDispatchInfo
from src.EmployeeTasksCustomer.views import router as EmployeeTasksCustomer
from src.ProductQuantityDetails.views import router as ProductQuantityDetails
from src.GrnOrderProduct.views import router as GrnOrderProduct
from src.GrnOrders.views import router as GrnOrders
from src.GrnInvoice.views import router as GrnInvoice
from src.Rfq.views import router as Rfq
from src.Subscribe.views import router as Subscribe
from src.ProjectTasks.views import router as project_tasks
from src.Notifications.views import router as notifications_router
from src.DailyTaskReport.views import router as DailyTaskReport
from src.FCM import router as fcm_router

api_router = APIRouter()

api_router.include_router(super_admin_router, prefix="/user", tags=["SuperAdmin"])

api_router.include_router(super_admin_plan_price_router, prefix="/SuperAdminPlanAndPrice",tags=["SuperAdminPlanAndPrice"])

api_router.include_router(super_admin_user_add_new_router, prefix="/SuperAdminUserAddNew", tags=["SuperAdminUserAddNew"])

api_router.include_router(super_admin_reffral_plan_router, prefix="/superadminreffralplan", tags=["SuperAdminReffralAndPlan"])

api_router.include_router(super_admin_billing_router, prefix="/superadminbilling", tags=["SuperAdminBilling"])

api_router.include_router(super_admin_enquiry_router, prefix="/superadminenquiry", tags=["SuperAdminEnquiry"])

api_router.include_router(admin_login_router, prefix="/adminlogin", tags=["AdminLogin"])

api_router.include_router(admin_add_employee_router, prefix="/adminaddemployee", tags=["AdminAddEmployee"])

api_router.include_router(admin_role_creation_router, prefix="/adminrolecreation", tags=["AdminRoleCreation"])

api_router.include_router(admin_assign_role_employee_router, prefix="/adminassignroleemployee",tags=["AdminRoleAssignEmployee"])

api_router.include_router(role_assign_by_level_router, prefix="/employeeassignbylevel", tags=["EmployeeAssignByLevel"])

api_router.include_router(employee_asssign_request, prefix="/employeeasignrequest", tags=["EmployeeAssignRequest"])

api_router.include_router(attendance, prefix="/attendance", tags=["EmployeeAttendance"])


api_router.include_router(employee_tasks, prefix="/employeetasks", tags=["EmployeeTasks"])

api_router.include_router(time_config, prefix="/timeconfig", tags=["TimeConfig"])

api_router.include_router(activity_comment, prefix="/activitycomment", tags=["ActivityComment"])


api_router.include_router(employee_leave, prefix="/employeeleave", tags=["EmployeeLeave"])


api_router.include_router(public_holiday, prefix="/publicholiday", tags=["PublicHoliday"])

api_router.include_router(quotation_template, prefix="/quotationtemplate", tags=["QuotationTemplate"])

api_router.include_router(quotation_product, prefix="/quotationproduct", tags=["QuotationProduct"])

api_router.include_router(quotation_product_employee, prefix="/quotationproductemployee", tags=["QuotationProductEmployee"])

api_router.include_router(term_and_condition, prefix="/termandcondition", tags=["TermAndConditions"])

api_router.include_router(brouncher, prefix="/brouncher", tags=["Brouncher"])

api_router.include_router(production, prefix="/production", tags=["Production"])

api_router.include_router(production_request, prefix="/productionrequest", tags=["ProductionRequest"])

api_router.include_router(lead_reminder, prefix="/leadreminder", tags=["LeadReminder"])

api_router.include_router(dispatch_vendor, prefix="/dispatchvendor", tags=["DispatchVendor"])

api_router.include_router(create_dispatch, prefix="/createdispatch", tags=["CreateDispatch"])

api_router.include_router(delivery_challan, prefix="/deliverychallan", tags=["DeliveryChallan"])

api_router.include_router(product_stages, prefix="/productstages", tags=["ProductStages"])

api_router.include_router(product_steps, prefix="/productsteps", tags=["ProductSteps"])

api_router.include_router(step_items, prefix="/stepitems", tags=["StepItems"])

api_router.include_router(late_mark, prefix="/latemark", tags=["LateMark"])

api_router.include_router(order_in_process, prefix="/orderinprocess", tags=["OrderInProcess"])

api_router.include_router(design_handover, prefix="/design_handover",tags=["DesignHandover"])

api_router.include_router(quotation_customer, prefix="/quotation_customer", tags=["QuotationCustomer"])

api_router.include_router(quotation_series, prefix="/quotation_series",tags=["QuotationSeries"])

api_router.include_router(bank, prefix="/bank", tags=["Bank"])

api_router.include_router(payment_term, prefix="/payment_term", tags=["PaymentTerm"])

api_router.include_router(account, prefix="/account", tags=["Account"])


api_router.include_router(add_payment, prefix="/add_payment", tags=["PaymentRequest"])

api_router.include_router(sub_product, prefix="/sub_product", tags=["QuotationSubProductEmployee"])


api_router.include_router(checkPoint, prefix="/checkPoint", tags=["CheckPoint"])

api_router.include_router(productTemplates, prefix="/productTemplates", tags=["ProductTemplates"])

api_router.include_router(ProductTemplates_key, prefix="/ProductTemplates_key", tags=["ProductTemplates_key"])


api_router.include_router(storeCheckPoint, prefix="/storeCheckPoint", tags=["StoreCheckPoint"])

api_router.include_router(FaceBook, prefix="/FaceBook", tags=["FaceBook"])


api_router.include_router(Subscribe, prefix="/Subscribe", tags=["Subscribe"])



api_router.include_router(PurchaseOrderProduct, prefix="/PurchaseOrderProduct", tags=["PurchaseOrderProduct"])


api_router.include_router(ProjectManagerResourseFile, prefix="/ProjectManagerResourseFile", tags=["ProjectManagerResourseFile"])


api_router.include_router(CreateDispatchInfo, prefix="/CreateDispatchInfo", tags=["CreateDispatchInfo"])


api_router.include_router(EmployeeTasksCustomer, prefix="/EmployeeTasksCustomer", tags=["EmployeeTasksCustomer"])


api_router.include_router(ProductQuantityDetails, prefix="/ProductQuantityDetails", tags=["ProductQuantityDetails"])


api_router.include_router(GrnOrders, prefix="/GrnOrders", tags=["GrnOrders"])

api_router.include_router(GrnOrderProduct, prefix="/GrnOrderProduct", tags=["GrnOrderProduct"])

api_router.include_router(GrnInvoice, prefix="/grn_invoice", tags=["GrnInvoice"])

api_router.include_router(Rfq, prefix="/rfq", tags=["Rfq"])


api_router.include_router(employee_files, prefix="/employee_files", tags=["EmployeeFiles"])

api_router.include_router(admin_sales_router, prefix="/adminsales", tags=["AdminSales"])

api_router.include_router(activity_center_router, prefix="/activity", tags=["Activity"])

api_router.include_router(meeting_planned_router, prefix="/meeting", tags=["MeetingPlanned"])

api_router.include_router(employee_login_router, prefix="/employeelogin", tags=["EmployeeLogin"])

api_router.include_router(store_manager_product_router, prefix="/product", tags=["StoreManagerProduct"])

api_router.include_router(store_manager_service_router, prefix="/service", tags=["StoreManagerService"])

api_router.include_router(catagory_router, prefix="/category", tags=["Category"])

api_router.include_router(sub_catagory_router, prefix="/sub_category", tags=["SubCategory"])

api_router.include_router(vendor_router, prefix="/vendor", tags=["Vendor"])

api_router.include_router(purchase_order_issue_router, prefix="/purchase_order_issue", tags=["PurchaseOrderIssue"])

api_router.include_router(project_manager_order_router, prefix="/project_mamager_order", tags=["ProjectManagerOrder"])

api_router.include_router(inventory_outward_router, prefix="/inventory_outward", tags=["InventoryOutward"])

api_router.include_router(product_wise_stock_router, prefix="/product_wise_stock", tags=["ProductWiseStock"])

api_router.include_router(store_manager_purchase_router, prefix="/store_manager_purchase",
                          tags=["StoreManagerPurchase"])

api_router.include_router(purchase_manager_router, prefix="/purchase_manager", tags=["PurchaseManager"])

api_router.include_router(ocr_router, prefix="/ocr", tags=["OCR"])

api_router.include_router(settings_router, prefix="/settings", tags=["Settings"])

api_router.include_router(settings_files_router, prefix="/settings_files", tags=["Settings Files"])

api_router.include_router(quotation_router, prefix="/quotation", tags=["Quotation"])

api_router.include_router(invoice_router, prefix="/invoice", tags=["Invoice"])

api_router.include_router(leads_router, prefix="/leads", tags=["Leads"])

api_router.include_router(integration_router, prefix="/integration", tags=["Integration"])

api_router.include_router(project_tasks, prefix="/project_tasks", tags=["ProjectTasks"])

api_router.include_router(notifications_router, prefix="/notifications", tags=["Notifications"])

api_router.include_router(DailyTaskReport, prefix="/DailyTaskReport", tags=["DailyTaskReport"])

api_router.include_router(fcm_router, prefix="/fcm", tags=["FCM"])