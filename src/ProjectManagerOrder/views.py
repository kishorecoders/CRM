from typing import List,Optional
from fastapi import APIRouter, Depends, HTTPException, status,Header,Query
from sqlmodel import Session
from src.database import get_db
from .models import  ProjectManagerOrderCreate,StatusUpdate,FetchOrdersRequest,ProjectManagerOrder,UpdateStageStatusRequest,UpdateHoldStatus,AccepetIntentryQuantity
from .service import create,delete_project_manager_order_by_id,get_all_project_manager_order,get_project_manager_order_by_admin,update,update_status,show_all_count,get_project_manager_order_by_order_id,get_pending_orders_for_admin,fetch_by_admin_and_employee,fetch_by_admin,update_hold_status
from src.parameter import get_token
from typing import List, Dict, Any
from src.AdminAddEmployee.models import AdminAddEmployee
from src.ProductStages.models import ProductStages
from src.Quotation.models import Quotation
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew


router = APIRouter()

@router.get("/showAllProjectManagerOrder")
def read_all_project_manager_order_details(auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_all_project_manager_order(db=db)
        

@router.get("/showProjectManagerOrderByAdmin/{admin_id}")
def read_project_manager_order_by_admin(admin_id:str, search: Optional[str] = None , emp_id: Optional[str] = None,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_project_manager_order_by_admin(db=db, admin_id=admin_id, search=search , emp_id = emp_id)
        
    



@router.post("/createProjectManagerOrder")
def create_project_manager_order_details(
    project_manager_order_create: ProjectManagerOrderCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    return create(db=db, project_manager_order_create=project_manager_order_create)

     
@router.put("/updateProjectManagerOrder/{project_manager_id}")
def update_project_manager_order_details(project_manager_id:int,project_manager_order:ProjectManagerOrderCreate,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db:Session=Depends(get_db)):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return update(project_manager_id=project_manager_id,project_manager_order=project_manager_order,db=db)

@router.delete("/DeleteProjectManager/{id}")
def delete_project_manager_order_details(id:int,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db:Session=Depends(get_db)):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return delete_project_manager_order_by_id(id=id,db=db)
            
@router.put("/updateStatus/{project_manager_order_id}")
def update_status_route(
    project_manager_order_id: int,
    request_data: StatusUpdate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    else:
        return update_status(project_manager_order_id=project_manager_order_id, request_data=request_data, db=db)
    
@router.get("/ProjectManagerDeshbordCount/{admin_id}")
def read_all_deshbord_count_details(admin_id: str,emp_id: Optional[str] = None, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db: Session = Depends(get_db)):
       def inner_get_plan(auth_token: str):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return show_all_count(db=db, admin_id=admin_id, emp_id = emp_id)
    
       return inner_get_plan(auth_token)   
   
@router.get("/ProjectManagerOrderByOrderId/{admin_id}/{order_id}")
def read_project_manager_order_by_order_id(admin_id: str, order_id: str, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db: Session = Depends(get_db)):
       def inner_get_plan(auth_token: str):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return get_project_manager_order_by_order_id(db=db, admin_id=admin_id, order_id=order_id)
    
       return inner_get_plan(auth_token)  
   
@router.get("/PendingOrder/{admin_id}")
def read_pending_orders_for_admin(admin_id: str, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db: Session = Depends(get_db)):
       def inner_get_plan(auth_token: str):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return get_pending_orders_for_admin(db=db, admin_id=admin_id)
    
       return inner_get_plan(auth_token)        



from src.Quotation_stages.models import QuotationStages
from datetime import datetime, date, time

today = date.today()
start_of_day = datetime.combine(today, time.min)
end_of_day = datetime.combine(today, time.max)





@router.post("/getProjectManagerOrders", response_model=Dict[str, Any])
def fetch_project_manager_orders(
    request: FetchOrdersRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db),
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request", "data": None}

    orders = fetch_by_admin_and_employee(
        db=db,
        admin_id=request.admin_id,
        employee_id=request.employee_id,
        availability=request.availability,
        order_id=request.order_id,
        is_stage_clear=request.is_stage_clear, 
        product_type=request.product_type,
        status=request.status,

        from_date=request.from_date,
        to_date=request.to_date,
        dispatch_at=request.dispatch_at
        
        
    )


    today_dispatch_count = db.query(ProjectManagerOrder).filter(
        ProjectManagerOrder.admin_id == request.admin_id,
        ProjectManagerOrder.status == "Won",
        ProjectManagerOrder.stage_status == "Order Dispatch",
        ProjectManagerOrder.dispatch_at.between(start_of_day, end_of_day)
    )
    if request.employee_id:
       today_dispatch_count = today_dispatch_count.filter(ProjectManagerOrder.emplpoyee_id == request.employee_id)
    today_dispatch_count = today_dispatch_count.count()

    transit_count = db.query(ProjectManagerOrder).filter(
        ProjectManagerOrder.admin_id == request.admin_id,
        ProjectManagerOrder.status == "Won",
        ProjectManagerOrder.stage_status == "Order Dispatch",
    )
    if request.employee_id:
        transit_count = transit_count.filter(ProjectManagerOrder.emplpoyee_id == request.employee_id)
    transit_count = transit_count.count()

    complete_count = db.query(ProjectManagerOrder).filter(
        ProjectManagerOrder.admin_id == request.admin_id,
        ProjectManagerOrder.status == "Won",
        ProjectManagerOrder.stage_status == "Dispatch Completed"
    )
    if request.employee_id:
        complete_count = complete_count.filter(ProjectManagerOrder.emplpoyee_id == request.employee_id)
    complete_count = complete_count.count()



    employee_ids = [order["emplpoyee_id"] for order in orders if order.get("emplpoyee_id")]
    assign_employee_ids = set()
    previous_employee_ids = set()

    for order in orders:
        all_products_completed = all(
            product.get("stage_status") == "Completed" for product in order.get("products", [])
        )
        #if all_products_completed:
        #    order["stage_status"] = "Completed"

        quotation_id = order.get("quotation_id")
        if quotation_id:
            quotation = db.query(Quotation).filter(Quotation.id == quotation_id).first()
            order["delevery_date"] = str(quotation.delevery_date) if quotation and quotation.delevery_date else None
        else:
            order["delevery_date"] = None

        for product in order.get("products", []):
            for stage in product.get("stage", []):
                if stage.get("assign_employee"):
                    assign_employee_ids.add(stage["assign_employee"])
                if stage.get("previous_employee"):
                    previous_employee_ids.add(stage["previous_employee"])

    all_employee_ids = list(set(employee_ids) | assign_employee_ids | previous_employee_ids)

    employees = db.query(AdminAddEmployee).filter(
        AdminAddEmployee.id.in_(all_employee_ids)
    ).all()

    employee_map = {
        str(emp.id): {
            "employee_name": emp.employe_name,
            "employee_id": emp.employee_id,
        }
        for emp in employees
    }

    # ? FETCH ADMIN FULL NAME
    admin = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == request.admin_id).first()
    admin_name = admin.full_name if admin else "Unknown"

    for order in orders:
        if not order.get("emplpoyee_id"):  # ? Admin case
            order["employee_name"] = admin_name.split(" ")[0]
            order["employee_id"] = "Admin"
        else:
            employee_data = employee_map.get(str(order.get("emplpoyee_id")), {})
            order["employee_name"] = employee_data.get("employee_name", "Unknown")
            order["employee_id"] = employee_data.get("employee_id", "Unknown")

        for product in order.get("products", []):
            for stage in product.get("stage", []):
                stage_employee = employee_map.get(str(stage.get("assign_employee")), {})
                previous_employee = employee_map.get(str(stage.get("previous_employee")), {})

                stage["employee_name"] = stage_employee.get("employee_name", "Unknown")
                stage["employee_id"] = stage_employee.get("employee_id", "Unknown")
                stage["previous_employee_name"] = previous_employee.get("employee_name", "Unknown")
                stage["previous_employee_id"] = previous_employee.get("employee_id", "Unknown")

            quotation_stages = db.query(QuotationStages).filter(
                QuotationStages.product_id == product.get("id")
            ).all()

            product["quotation_stages"] = []

            for qstage in quotation_stages:
                product_stage = db.query(ProductStages).filter(ProductStages.id == qstage.stage_id).first()

                if product_stage:
                    quotation_stages_by_stage_id = db.query(QuotationStages).filter(
                        QuotationStages.product_id == product.get("id"),
                        QuotationStages.stage_id == product_stage.id
                    ).first()

                    if quotation_stages_by_stage_id:
                        product["quotation_stages"].append({
                            "id": product_stage.id,
                            "steps": product_stage.steps,
                            "time_riquired_for_this_process": product_stage.time_riquired_for_this_process,
                            "day": product_stage.day,
                            "quotation_stages_list": quotation_stages_by_stage_id,
                        })

            if not product["quotation_stages"]:
                product["quotation_stages"] = None
                

    if not orders:
        return {"status": "false", 
                "message": "No orders found", 
                "transit_count":transit_count,
                "complete_count": complete_count,
                "today_dispatch_count": today_dispatch_count,
                "data": None
                }

    return {
        "status": "true",
        "message": "Orders fetched successfully",
        "transit_count":transit_count,
        "complete_count": complete_count,
        "today_dispatch_count": today_dispatch_count,
        "data": orders,
    }








@router.get("/get_poject_manager_order", response_model=Dict[str, Any])
def fetch_project_manager_orders(
    order_id: str = Query(..., description="Order ID to filter orders"),
    db: Session = Depends(get_db),
):
    

    orders = fetch_by_admin(
        db=db,
        order_id=order_id
    )

    if not orders:
        return {"status": "false", "message": "No orders found", "data": None}

    return {
        "status": "true",
        "message": "Orders fetched successfully",
        "data": orders
    }


from src.parameter import get_current_datetime


@router.post("/update_stage_status")
def update_stage_status(
    request_data: UpdateStageStatusRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    
    order_data = db.query(ProjectManagerOrder).filter(ProjectManagerOrder.id == request_data.order_id).first()
    
    if not order_data:
        raise HTTPException(status_code=404, detail="Project Manager Order not found")


    if request_data.employee_id:
        hold_by_type = "employee"
        hold_admin_emp_id = request_data.employee_id
    else:
        hold_by_type = "admin"
        hold_admin_emp_id = request_data.admin_id


    if request_data.status is not None:
        order_data.stage_status = request_data.status
        order_data.dispatch_at = get_current_datetime()  if request_data.status == "Order Dispatch" else order_data.dispatch_at

        
    if request_data.hold_status is not None:
        order_data.hold_status = request_data.hold_status
        order_data.hold_at = get_current_datetime()
        order_data.hold_by_type = hold_by_type
        order_data.hold_admin_emp_id = hold_admin_emp_id
    
    if request_data.hold_status_remark is not None:
        order_data.hold_status_remark = request_data.hold_status_remark
    if request_data.authorized_img is not None:
        order_data.authorized_img = request_data.authorized_img
    if request_data.dispatch_img is not None:
        order_data.dispatch_img = request_data.dispatch_img
    if request_data.eway_bill_no is not None:
        order_data.eway_bill_no = request_data.eway_bill_no
    if request_data.challan_date is not None:
        order_data.challan_date = request_data.challan_date

 

    db.commit()
    db.refresh(order_data)
    
    return {
        "status": "true",
        "message": "Project Manager Order Stage Status Updated Successfully"
    }

@router.post("/update_hold_re_status")
def update_hold_re_status(
    request_data: UpdateHoldStatus,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    else:
        return update_hold_status( request_data=request_data, db=db)



from src.QuotationProductEmployee.models import QuotationProductEmployee
from src.ProjectManagerOrder.models import ProjectManagerOrder  # Assuming this is your model
from sqlalchemy.orm.attributes import flag_modified
from src.StoreManagerProduct.models import storeManagerProduct 
@router.post("/accepet_intentry_quantity")
def accepet_intentry_quantity(
    request_data: AccepetIntentryQuantity,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    project_manager = db.query(ProjectManagerOrder).filter(
        ProjectManagerOrder.id == int(request_data.projectmanager_id)
    ).first()

    if not project_manager:
        return {"status": "false", "message": "Project Manager not found"}

    try:
        quantity = int(request_data.productquantity)

        if project_manager.status == "Won":
            product = db.query(QuotationProductEmployee).filter(
                QuotationProductEmployee.id == int(request_data.product_id)
            ).first()

            if not product:
                return {"status": "false", "message": "Product not found in QuotationProductEmployee"}

            product.manufacture_quantity = str(
                int(product.manufacture_quantity or 0) - quantity
            )
            product.available_quantity = str(
                int(product.available_quantity or 0) + quantity
            )
            db.add(product)


            store = db.query(storeManagerProduct).filter(storeManagerProduct.item_code == product.product_code).first()
            if store:
                store.opening_stock = str(int(store.opening_stock) - quantity)
            db.add(store)

        elif project_manager.status == "Manual":
            store = db.query(storeManagerProduct).filter(storeManagerProduct.id == int(request_data.product_id)).first()
            if store:
                store.opening_stock = str(int(store.opening_stock) - quantity)
            db.add(store)

            updated = False
            for data in project_manager.product_id_and_quantity:
                if str(data.get('product_id')) == str(request_data.product_id):
                    data['available_quantity'] = str(
                        int(data.get('available_quantity', 0)) + quantity
                    )
                    data['manufacture_quantity'] = str(
                        int(data.get('manufacture_quantity', 0)) - quantity
                    )
                    flag_modified(project_manager, "product_id_and_quantity")  
                    db.add(project_manager)
                    updated = True
                    break

            if not updated:
                return {
                    "status": "false",
                    "message": f"Product ID {request_data.product_id} not found in project_id_and_quantity"
                }

        db.commit()

        return {
            "status": "true",
            "message": "Quantity accepted and updated successfully"
        }

    except Exception as e:
        db.rollback()
        return {
            "status": "false",
            "message": f"An error occurred: {str(e)}"
        }



