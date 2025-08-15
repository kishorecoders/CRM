from typing import List,Optional
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlmodel import Session
from src.database import get_db
from .models import  InventoryOutward,InventoryOutwardCreate,UpdateStatusRequest,InventoryFilterRequest,BookStatusRequest,UpdateDispatchStatusRequest,AddDispatchOrderRequest
from .service import create,get_all_inventory_outward,get_inventory_outward_by_admin,delete_inventory_outward_by_id,update,create_inventory_outward_record,update_inventory_status,get_inventory_outward_list,update_book_status
from src.parameter import get_token
from datetime import datetime
from src.ProjectManagerOrder.models import ProjectManagerOrder




import os
import base64
from uuid import uuid4


router = APIRouter()

@router.get("/showAllInventoryOutward")
def read_all_inventory_outward_details(auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_all_inventory_outward(db=db)
        
@router.get("/showInventoryOutwardByAdmin/{admin_id}")
def read_inventory_outward_by_admin(admin_id:str,search: Optional[str] = None,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
             db: Session = Depends(get_db)):
        if auth_token != get_token():
            return {"status": "false", "message": "Unauthorized Request"}
        else:
            return get_inventory_outward_by_admin(db=db, admin_id=admin_id, search=search)

@router.post("/createInventoryOutward")
def create_inventory_outward(
    outward_data: InventoryOutwardCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    
    
    return create_inventory_outward_record(outward_data=outward_data, db=db)
# def create_inventory_outward_details(inventory_outward_create: InventoryOutwardCreate,
#                 auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
#                 db: Session = Depends(get_db)):
#         if auth_token != get_token():
#             return {"status": "false", "message": "Unauthorized Request"}
#         else:
#             return create(db=db, inventory_outward_create=inventory_outward_create)

@router.post("/createInventoryOutwardNew")
def create_inventory_outward(
    outward_data: InventoryOutwardCreate,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    
    
    return create_inventory_outward_record(outward_data=outward_data, db=db)
        

     
@router.put("/updateInventoryOutward/{inventory_outward_id}")
def update_inventory_outward_details(inventory_outward_id:int,inventory_outward_update:InventoryOutwardCreate,auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db:Session=Depends(get_db)):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return update(inventory_outward_id=inventory_outward_id,inventory_outward_update=inventory_outward_update,db=db)

@router.delete("/deleteInventoryOutward/{inventory_outward_id}")
def delete_inventory_outward_by_id(inventory_outward_id: int, auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"), db: Session = Depends(get_db)):
            if auth_token != get_token():
                return {"status": "false", "message": "Unauthorized Request"}
            else:
                return delete_inventory_outward_by_id(inventory_outward_id=inventory_outward_id, db=db)
            


@router.post("/update_status")
def update_status(
    request: UpdateStatusRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    return update_inventory_status(request, db)






@router.post("/update_book_status")
def update_booked_status(
    request: BookStatusRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    return update_book_status(request, db)





@router.post("/inventory_outward_list", response_model=dict)
def get_inventory_list(
    request: InventoryFilterRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}
    
    return get_inventory_outward_list(request, db)
    
    






def save_base64_file(base64_str: str, filename: str) -> str:
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    file_path = os.path.join("uploads", filename)
    with open(file_path, "wb") as file:
        file.write(base64.b64decode(base64_str))
    return file_path
    
    
    
from src.parameter import get_current_datetime




@router.post("/update_dispatch_status")
def update_dispatch_status(
    request: UpdateDispatchStatusRequest, 
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):

    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    inventory = db.query(InventoryOutward).filter(
        InventoryOutward.id == request.inventory_id,
        InventoryOutward.admin_id == request.admin_id
    ).first()
    
    

    #if not inventory:
      #  raise HTTPException(status_code=404, detail="Inventory record not found")

    if request.employee_id:
        dispatch_by_type = "employee"
        dispatch_admin_emp_id = request.employee_id
    else:
        dispatch_by_type = "admin"
        dispatch_admin_emp_id = request.admin_id  

    if request.employee_id:
        dispatch_approve_by_type = "employee"
        dispatch_approve_by_id = request.employee_id
    else:
        dispatch_approve_by_type = "admin"
        dispatch_approve_by_id = request.admin_id  


    if request.dispatch_status =="Requested":
         inventory.dispatch_status = request.dispatch_status
         inventory.dispatch_by_type = dispatch_by_type
         inventory.dispatch_admin_emp_id = dispatch_admin_emp_id
         inventory.dispatch_created_at = get_current_datetime()
         inventory.today_dispatch_date = get_current_datetime()
         inventory.dispatch_type = "Product"
         
    elif request.dispatch_status =="Requested_Unhold" :
        inventory.dispatch_status = "Requested"
        inventory.dispatch_approve_by_type = dispatch_approve_by_type
        inventory.dispatch_approve_by_id = dispatch_approve_by_id
        inventory.dispatch_remark = request.dispatch_remark
        inventory.dispatch_updated_at = get_current_datetime()

    else:
        inventory.dispatch_status = request.dispatch_status
        inventory.dispatch_approve_by_type = dispatch_approve_by_type
        inventory.dispatch_approve_by_id = dispatch_approve_by_id
        inventory.dispatch_remark = request.dispatch_remark
        inventory.dispatch_updated_at = get_current_datetime()



    #inventory.dispatch_status = request.dispatch_status
    
    inventory.updated_at = datetime.now()

    # Handle image saving only if status is "Completed"
    if request.dispatch_status.lower() == "completed":
        if request.authorized_img:
            inventory.authorized_img = request.authorized_img
            #filename = f"authorized_{uuid4().hex}.png"
            #inventory.authorized_img = save_base64_file(request.authorized_img, filename)
        if request.dispatch_img:
            inventory.dispatch_img = request.dispatch_img
            #filename = f"dispatch_{uuid4().hex}.png"
            #inventory.dispatch_img = save_base64_file(request.dispatch_img, filename)
        if request.challan_date:
            inventory.challan_date = request.challan_date
        if request.eway_bill_no:
             inventory.eway_bill_no = request.eway_bill_no

    db.commit()
    db.refresh(inventory)

    return {
        "status": "true",
        "message": "Dispatch status updated successfully",
        "data": {
            "inventory_id": inventory.id,
            "dispatch_status": inventory.dispatch_status,
            "authorized_img": inventory.authorized_img,
            "dispatch_img": inventory.dispatch_img
        }
    }
    
    
    
@router.post("/add_dispatch_order")
def add_dispatch_order(
    request: AddDispatchOrderRequest,
    auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),
    db: Session = Depends(get_db)
):
    if auth_token != get_token():
        return {"status": "false", "message": "Unauthorized Request"}

    if request.employee_id:
        dispatch_by_type = "employee"
        dispatch_admin_emp_id = request.employee_id
    else:
        dispatch_by_type = "admin"
        dispatch_admin_emp_id = request.admin_id

    new_dispatch = InventoryOutward(
        admin_id=request.admin_id,
        order_id_id=request.order_id_id,
        dispatch_type=request.dispatch_type,
        status= "Approved",
        dispatch_status="Requested",
        dispatch_by_type=dispatch_by_type,
        dispatch_admin_emp_id=dispatch_admin_emp_id,
        dispatch_created_at=get_current_datetime(),
        outward_datetime=get_current_datetime(),
        product_id=request.product_id,
        ask_qty=request.ask_qty,
        given_qty=request.given_qty,
        released_to_person=request.released_to_person,
        created_at=get_current_datetime(),
        updated_at=get_current_datetime()
    )

    db.add(new_dispatch)
    db.commit()
    db.refresh(new_dispatch)
    
    
    pm_order = db.query(ProjectManagerOrder).filter(
        ProjectManagerOrder.id == request.order_id_id
    ).first()

    if pm_order:
        pm_order.stage_status = "Order Dispatch"
        pm_order.dispatch_by_type = dispatch_by_type
        pm_order.dispatch_admin_emp_id = dispatch_admin_emp_id
        pm_order.dispatch_at = get_current_datetime()
        pm_order.updated_at = get_current_datetime()
        db.commit()

    return {
        "status": "true",
        "message": "Dispatch Order created successfully",
        "data": {
            "inventory_id": new_dispatch.id,
            "dispatch_status": new_dispatch.dispatch_status,
            "dispatch_type": new_dispatch.dispatch_type,
            "order_id_id": new_dispatch.order_id_id
        }
    }




