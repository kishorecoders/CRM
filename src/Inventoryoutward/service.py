from .models import InventoryOutward,InventoryOutwardCreate,UpdateStatusRequest,InventoryFilterRequest,BookStatusRequest
from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime
from fastapi import status,HTTPException
from src.Productwisestock.models import ProductWiseStock
from src.StoreManagerProduct.models import storeManagerProduct
from src.AdminAddEmployee.models import AdminAddEmployee
from src.QuotationProductEmployee.models import QuotationProductEmployee
from sqlalchemy import func, cast, String
from typing import Dict
from src.ProjectManagerOrder.models import ProjectManagerOrder
from src.DeliveryChallan.models import DeliveryChallan
from src.DispatchVendor.models import DispatchVendor


from datetime import datetime, date
today = date.today()


def get_all_inventory_outward(db: Session):
    data = db.query(InventoryOutward).order_by(InventoryOutward.id.desc()).all()
    response = {'status': 'true', 'message': "Data Received Successfully", 'data': data}
    return response


def get_inventory_outward_by_admin(db: Session, admin_id: str, search: Optional[str] = None):
    array = []
    
    
    inventoryOutwardListQuery = db.query(InventoryOutward).filter(InventoryOutward.admin_id == admin_id)

    
    if search:
        inventoryOutwardListQuery = inventoryOutwardListQuery.filter(
            (InventoryOutward.order_id.ilike(f"%{search}%")) |
            (InventoryOutward.outward_id.ilike(f"%{search}%"))
        )

    
    inventoryOutwardList = inventoryOutwardListQuery.all()

    for inventoryOutward in inventoryOutwardList:
        

       
        if inventoryOutward.product_id:
            
            product_ids = inventoryOutward.product_id.split(',')
            employee_ids = inventoryOutward.released_to_person.split(',')
            ask_qty_list = list(map(int, inventoryOutward.ask_qty.split(',')))
            given_qty_list = list(map(int, inventoryOutward.given_qty.split(',')))
            left_qty_list = list(map(int, inventoryOutward.left.split(',')))
            
            
            employee_name_map = {}
            
            for employee_id in employee_ids:
            
                employeeDetails = db.query(AdminAddEmployee).filter(AdminAddEmployee.employee_id == employee_id).first()
                if employeeDetails:
                   employee_name_map[employee_id] = employeeDetails.employe_name
    
           
            product_details = []

           
            for product_id, ask_qty, given_qty, left_qty, employee_id in zip(product_ids, ask_qty_list, given_qty_list, left_qty_list, employee_ids):
                employee_name = employee_name_map.get(employee_id)
                productDetails = db.query(storeManagerProduct).filter(storeManagerProduct.id == product_id).first()
                product_detail = {
                    "ask_qty": ask_qty,
                    "given_qty": given_qty,
                    "left": left_qty,
                    "employe_name": employee_name,
                    "product_details_2": productDetails.__dict__ if productDetails else None
                }
                product_details.append(product_detail)

        status = "Pending"
        if (
            inventoryOutward.order_id
            and inventoryOutward.ask_qty
            and inventoryOutward.given_qty
            and inventoryOutward.left
        ):
            order_id = str(inventoryOutward.order_id)
            ask_qty = int(inventoryOutward.ask_qty)
            given_qty = int(inventoryOutward.given_qty)
            left_qty = int(inventoryOutward.left)

            if left_qty == 0:
                status = "Complete"
            elif left_qty < ask_qty:
                status = "Persioli"

        temp = {
            "inventory_outward_details": {**inventoryOutward.__dict__, "status": status},
            "product_details": product_details
        }
        array.append(temp)

    response = {'status': 'true', 'message': "Data Received Successfully", 'data': array}
    return response



def create(outward_data: InventoryOutwardCreate, db: Session):
   
    product_details = db.query(ProductWiseStock).filter(ProductWiseStock.product_id == outward_data.product_id).first()
    if not product_details:
        return {"status": "false", "message": "Product ID does not exist in ProductWiseStock"}
    
    
    new_outward = InventoryOutward.from_orm(outward_data)
    
  
    db.add(new_outward)
    db.commit()
    db.refresh(new_outward)
    
    
    return {"status": "true", "message": "Inventory Outward created successfully", "data": new_outward}


def create_inventory_outward_record(outward_data: InventoryOutwardCreate, db: Session):
   
    product_details = db.query(ProductWiseStock).filter(ProductWiseStock.product_id == outward_data.product_id).first()
    
    if not product_details:
        return {"status": "false", "message": "Product ID does not exist in ProductWiseStock"}
    
    new_outward = InventoryOutward.from_orm(outward_data)
    db.add(new_outward)
    db.commit()
    db.refresh(new_outward)
    
    return {"status": "true", "message": "Inventory Outward created successfully", "data": new_outward}




def generate_new_outward_id(db: Session, admin_id: int) -> str:
    latest_outward = (
        db.query(func.max(InventoryOutward.outward_id))
        .filter(InventoryOutward.admin_id == admin_id)
        .scalar()
    )
    existing_outward_number = int(latest_outward.split('-')[1]) if (latest_outward and '-' in latest_outward) else 0
    new_outward_number = existing_outward_number + 1
    new_outward_id = f"OWR-{new_outward_number:04d}"  
    return new_outward_id
   
# def update(inventory_outward_id:int, inventory_outward:InventoryOutward,db:Session):
#     inventory_outward_update = inventory_outward.dict(exclude_unset=True)
#     db.query(InventoryOutward).filter(InventoryOutward.id == inventory_outward_id).update(inventory_outward_update)
#     db.commit()
#     response = {'status': 'true','message':"Inventory Outward Details Updated Successfully",'data':inventory_outward_update}
#     return response


def update(inventory_outward_id:int, inventory_outward_update:InventoryOutward, db:Session):
    response = {}
    product_ids = inventory_outward_update.product_id.split(',')
    ask_qty_list = list(map(int, inventory_outward_update.ask_qty.split(',')))
    given_qty_list = list(map(int, inventory_outward_update.given_qty.split(',')))
    released_to_person_list = inventory_outward_update.released_to_person.split(',')

    if len(product_ids) == len(ask_qty_list) == len(given_qty_list) == len(released_to_person_list):
        
        
        existing_outward = (
            db.query(InventoryOutward)
            .filter(InventoryOutward.id == inventory_outward_id)
            .first()
        )

        if existing_outward:
            
            if existing_outward.admin_id == inventory_outward_update.admin_id:
                
                existing_outward.ask_qty = ', '.join(map(str, ask_qty_list))
                existing_outward.given_qty = ', '.join(map(str, given_qty_list))
                existing_outward.left = ', '.join(map(str, [ask - given for ask, given in zip(ask_qty_list, given_qty_list)]))

                
                for product_id, given_qty in zip(product_ids, given_qty_list):
                    
                    product_stock = db.query(ProductWiseStock).filter(ProductWiseStock.product_id == product_id).first()
                    if product_stock:
                       
                        product_stock.total_quantity -= given_qty
                    else:
                        
                        response = {'status': 'false', 'message': f'Product ID {product_id} does not exist', 'data': None}
                        return response

                db.commit()
                response = {'status': 'true', 'message': "Inventory Outward Updated Successfully", 'data': None}
            else:
                response = {'status': 'false', 'message': 'Admin ID does not match', 'data': None}
        else:
            response = {'status': 'false', 'message': 'Inventory Outward not found', 'data': None}
    else:
        response = {'status': 'false', 'message': 'Mismatch in product information', 'data': None}

    return response

def delete_inventory_outward_by_id(inventory_outward_id: int, db: Session):
    inventory_outward_details = db.query(InventoryOutward).filter(InventoryOutward.id == inventory_outward_id).first()
    if inventory_outward_details:
        db.delete(inventory_outward_details)
        db.commit()
        return {'status':'true', 'message':"Inventory Outward Details deleted successfully", 'data':inventory_outward_details}
    return {"status":'false',  'message':"Inventory Outward not found"}



from src.InventoryOutwardRemark.models import InventoryOutwardRemark


def update_inventory_status(request: UpdateStatusRequest, db: Session):
    inventory_item = db.query(InventoryOutward).filter(
        InventoryOutward.id == request.inventory_id,
        InventoryOutward.admin_id == request.admin_id
    ).first()

    if not inventory_item:
        raise HTTPException(status_code=404, detail="Inventory record not found")

    if request.employee_id:
        approve_by_type = "employee"
        approve_by_id = request.employee_id
    else:
        approve_by_type = "admin"
        approve_by_id = request.admin_id  

    if request.type and request.add_remark:
        new_outward_remark = InventoryOutwardRemark(
            admin_id=request.admin_id,
            employee_id=request.employee_id,
            add_remark=request.add_remark,
            type=request.type,
            InventoryOutward_id=inventory_item.id,
        )
        db.add(new_outward_remark)


    inventory_item.approve_by_id = approve_by_id
    inventory_item.approve_by_type = approve_by_type

    if inventory_item.order_id:
        sale_order = db.query(ProjectManagerOrder).filter(
            ProjectManagerOrder.id == int(inventory_item.order_id)
        ).first()
        if sale_order.status == 'Won':
            inventory_item.status = request.status
            inventory_item.updated_at = datetime.now()
        elif sale_order.status == 'Manual':
            inventory_item.status = request.status 
            inventory_item.updated_at = datetime.now()
            if request.status == 'Approved':
                product = db.query(QuotationProductEmployee).filter(QuotationProductEmployee.id == int(inventory_item.product_id)).first()
                if product:
                    product.dispatch_status = 'Approved'
                    db.add(product)
                    
    db.add(inventory_item)
    db.commit()
    db.refresh(inventory_item)

    product_item = db.query(QuotationProductEmployee).filter(
        QuotationProductEmployee.id == inventory_item.product_id
    ).first()

    if product_item:
    
        if product_item.dispatch_status == "Disapproved":
            product_item.dispatch_status = "Pending"
    
        product_item.status = request.status
        db.add(product_item)
        db.commit()
        db.refresh(product_item)

    return {"status": "true", "message": "Status updated successfully"}
    
    
    
    
    

def update_book_status(request: BookStatusRequest, db: Session):
    inventory_item = db.query(InventoryOutward).filter(
        InventoryOutward.id == request.inventory_id,
        InventoryOutward.admin_id == request.admin_id
    ).first()

    if not inventory_item:
        raise HTTPException(status_code=404, detail="Inventory record not found")

    if request.employee_id:
        approve_by_type = "employee"
        approve_by_id = request.employee_id
    else:
        approve_by_type = "admin"
        approve_by_id = request.admin_id  

    if request.type and request.add_remark:
        new_outward_remark = InventoryOutwardRemark(
            admin_id=request.admin_id,
            employee_id=request.employee_id,
            add_remark=request.add_remark,
            type=request.type,
            InventoryOutward_id=inventory_item.id,
        )
        db.add(new_outward_remark)


    inventory_item.approve_by_id = approve_by_id
    inventory_item.approve_by_type = approve_by_type
               
    inventory_item.book_status = request.book_status
    inventory_item.updated_at = datetime.now()
    db.add(inventory_item)
    db.commit()
    db.refresh(inventory_item)

    product_item = db.query(QuotationProductEmployee).filter(
        QuotationProductEmployee.id == inventory_item.product_id
    ).first()

    if product_item:
        product_item.booked_status = request.book_status
        db.add(product_item)
        db.commit()
        db.refresh(product_item)

    return {"status": "true", "message": "Status updated successfully"}



from src.InventoryOutwardRemark.models import InventoryOutwardRemark

from src.AdminAddEmployee.models import AdminAddEmployee
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew
from src.cre_upd_name import get_creator_updator_info



from src.Quotation.models import Quotation
from src.AdminSales.models import AdminSales

def get_inventory_outward_list(request: InventoryFilterRequest, db: Session):
    query = select(InventoryOutward).where(InventoryOutward.admin_id == request.admin_id,InventoryOutward.dispatch_type == "Product")

    if request.employee_id:
        query = query.where(InventoryOutward.emplpoyee_id == request.employee_id)
    if request.status:
        query = query.where(InventoryOutward.status == request.status)

    if request.dispatch_status:
        query = query.where(InventoryOutward.dispatch_status == request.dispatch_status)


    
    if request.from_date and request.to_date:
        start_datetime = datetime.combine(request.from_date, datetime.min.time())
        end_datetime = datetime.combine(request.to_date, datetime.max.time())
        query = query.where(
            InventoryOutward.outward_datetime.between(start_datetime, end_datetime)
        )
    elif request.outward_date:
       
        start_datetime = datetime.combine(request.outward_date, datetime.min.time())
        end_datetime = datetime.combine(request.outward_date, datetime.max.time())
        query = query.where(
            InventoryOutward.outward_datetime.between(start_datetime, end_datetime)
        )

    if request.today_dispatch_date:
        start_datetime = datetime.combine(request.today_dispatch_date, datetime.min.time())
        end_datetime = datetime.combine(request.today_dispatch_date, datetime.max.time())
        query = query.where(
            InventoryOutward.today_dispatch_date.between(start_datetime, end_datetime)
        )



    today_dispatch_count = db.query(InventoryOutward).filter(
        InventoryOutward.admin_id == request.admin_id,
        InventoryOutward.status == "Approved",
        InventoryOutward.dispatch_status.in_(["Hold", "Requested"]),

        InventoryOutward.today_dispatch_date >= datetime.combine(today, datetime.min.time()),
        InventoryOutward.today_dispatch_date <= datetime.combine(today, datetime.max.time())
    )
    if request.employee_id:
        today_dispatch_count = today_dispatch_count.filter(InventoryOutward.emplpoyee_id == request.employee_id)
    #today_dispatch_count = today_dispatch_count.count()


    transit_count = db.query(InventoryOutward).filter(
        InventoryOutward.admin_id == request.admin_id,
        InventoryOutward.status == "Approved",
        InventoryOutward.dispatch_status.in_(["Hold", "Requested"]),
        InventoryOutward.dispatch_type == "Product"
    )
    if request.employee_id:
        transit_count = transit_count.filter(InventoryOutward.emplpoyee_id == request.employee_id)
    #transit_count = transit_count.count()


    complete_count = db.query(InventoryOutward).filter(
        InventoryOutward.admin_id == request.admin_id,
        InventoryOutward.status == "Approved",
        InventoryOutward.dispatch_status == "Completed"
    )
    if request.employee_id:
        complete_count = complete_count.filter(InventoryOutward.emplpoyee_id == request.employee_id)
    #complete_count = complete_count.count()

        
    inventory_list = db.execute(query.order_by(InventoryOutward.created_at.desc())).scalars().all()

    complete_count = 0
    transit_count = 0
    today_dispatch_count = 0

    if not inventory_list:
        return {"status": "false", 
                "message": "No records found",
                "today_dispatch_count": today_dispatch_count,
                "transit_count": transit_count,
                "complete_count": complete_count,
                "data" : None
                }

    response_data = []
    delivery_address = None
    sales_order_id = None
    po_number = None
    customer = None    
    share_by_email = None
    share_by_whatsapp = None

    for inventory in inventory_list:
        product_details = db.query(QuotationProductEmployee).filter(
            QuotationProductEmployee.id == inventory.product_id
        ).first()
        if product_details is not None:
            if product_details.dispatch_status in ['Approved' , 'Give Credit']:
                if (
                    inventory
                    and inventory.status == "Approved"
                    and inventory.dispatch_status in ["Hold", "Requested"]
                ):
                    try:
                        # Convert to datetime if it's a string
                        dispatch_datetime = inventory.today_dispatch_date
                        if isinstance(dispatch_datetime, str):
                            dispatch_datetime = datetime.fromisoformat(dispatch_datetime)

                        if (
                            dispatch_datetime >= datetime.combine(today, datetime.min.time())
                            and dispatch_datetime <= datetime.combine(today, datetime.max.time())
                        ):
                            today_dispatch_count += 1
                    except Exception as e:
                        print("Invalid dispatch date:", inventory.today_dispatch_date, e)
                
                if inventory  and inventory.status == "Approved" and inventory.dispatch_status in ["Hold", "Requested"] and inventory.dispatch_type == "Product":
                    transit_count += 1
                
                if inventory and inventory.status == "Approved" and inventory.dispatch_status == "Completed":
                    complete_count += 1    
    
            created_updated_data_pro = get_creator_updator_info(
                admin_emp_id=inventory.dispatch_admin_emp_id,
                created_by_type=inventory.dispatch_by_type,
                updated_admin_emp_id=inventory.dispatch_approve_by_id,
                updated_by_type=inventory.dispatch_approve_by_type,
                db=db
                )
            updated_at = inventory.dispatch_updated_at
            created_at = inventory.dispatch_created_at

            created_updated_data_pro["creator_info"]["created_at"] = created_at
            created_updated_data_pro["updater_info"]["updated_at"] = updated_at
            created_updated_data_pro["updater_info"]["dispatch_remark"] = inventory.dispatch_remark if inventory.dispatch_remark else None

            if inventory.order_id:
                sale_order = db.query(ProjectManagerOrder).filter(
                    ProjectManagerOrder.id == int(inventory.order_id)
                ).first()
                if sale_order.status == 'Won':
                    quot = db.query(Quotation).filter(Quotation.id == product_details.quote_id).first()
                    if quot is not None:
                        delivery_address = quot.delevery_address if quot else None
                        sales_order_id = quot.pi_number if quot else None
                        po_number = quot.po_number if quot else None
                        share_by_email = quot.share_by_email
                        share_by_whatsapp = quot.share_by_whatsapp
                        if quot.lead_id is not None:
                            admin = db.query(AdminSales).filter(AdminSales.id == quot.lead_id).first()
                            if admin is not None:
                                customer = admin.name
                elif sale_order.status == 'Manual':
                    sales_order_id = sale_order.manual_sale_order_id
                    quot = db.query(Quotation).filter(Quotation.id == product_details.quote_id).first()
                    if quot is not None:
                        delivery_address = quot.delevery_address if quot else None
                        po_number = quot.po_number if quot else None
                        share_by_email = quot.share_by_email
                        share_by_whatsapp = quot.share_by_whatsapp
                        if quot.lead_id is not None:
                            admin = db.query(AdminSales).filter(AdminSales.id == quot.lead_id).first()
                            if admin is not None:
                                customer = admin.name


        order = db.query(ProjectManagerOrder).filter(
            ProjectManagerOrder.id == inventory.order_id
        ).first()

        remarks = db.query(InventoryOutwardRemark).filter(
            InventoryOutwardRemark.InventoryOutward_id == inventory.id
        ).all()

        remark_list = []

        for r in remarks:
            remark_data = r.dict()
            if r.emplpoyee_id:
                employee = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == r.employee_id).first()
                if employee:
                    remark_data["admin_emp_short_name"] = f"{employee.employe_name.split()[0]}({employee.employee_id})"
            else:
                admin = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == r.admin_id).first()
                if admin:
                    remark_data["admin_emp_short_name"] = f"{admin.full_name} (Admin)"
            remark_list.append(remark_data)


        Challans = db.query(DeliveryChallan).filter(DeliveryChallan.inventryoutword_id == inventory.id).all()
        
        created_updated_data = {}
        vendor = {}

        for challan in Challans:
            vendor = db.query(DispatchVendor).filter(DispatchVendor.id == int(challan.vendor_id)).first()

            created_updated_data = get_creator_updator_info(
                admin_emp_id=challan.admin_emp_id,
                created_by_type=challan.created_by_type,
                updated_admin_emp_id=challan.updated_admin_emp_id,
                updated_by_type=challan.updated_by_type,
                db=db
                )
            updated_at = challan.updated_at
            created_at = challan.created_at

            created_updated_data["creator_info"]["created_at"] = updated_at
            created_updated_data["updater_info"]["updated_at"] = created_at

        # Creator details
        creator_info = {
            "name": "",
            "id": None,
            "employee_id": ""
        }
        if inventory.admin_emp_id:
            if inventory.created_by_type == 'employee':
                empd = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == int(inventory.admin_emp_id)).first()
                if empd:
                    creator_info = {
                        "name": empd.employe_name,
                        "id": empd.id,
                        "employee_id": empd.employee_id
                    }
            elif inventory.created_by_type == 'admin':
                empd = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == int(inventory.admin_emp_id)).first()
                if empd:
                    creator_info = {
                        "name": empd.full_name,
                        "id": empd.id,
                        "employee_id": "Admin"
                    }

        # Approver details
        approver_info = {
            "name": "",
            "id": None,
            "employee_id": ""
        }
        if inventory.approve_by_id:
            if inventory.approve_by_type == 'employee':
                empd = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == int(inventory.approve_by_id)).first()
                if empd:
                    approver_info = {
                        "name": empd.employe_name,
                        "id": empd.id,
                        "employee_id": empd.employee_id
                    }
            elif inventory.approve_by_type == 'admin':
                empd = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == int(inventory.approve_by_id)).first()
                if empd:
                    approver_info = {
                        "name": empd.full_name,
                        "id": empd.id,
                        "employee_id": "Admin"
                    }

        # ? Get Delivery Challan
        delivery_challan = db.query(DeliveryChallan).filter(
            DeliveryChallan.inventryoutword_id == str(inventory.id)
        ).first()

        inventory_dict = inventory.dict()
        inventory_dict["order_code"] = order.order_id if order else None
        inventory_dict["delivery_address"] = delivery_address if delivery_address else None
        inventory_dict["sales_order_id"] = sales_order_id if sales_order_id else None
        inventory_dict["po_number"] = po_number if po_number else None
        inventory_dict["customer"] = customer if customer else None
        inventory_dict["share_by_email"] = share_by_email if share_by_email else None
        inventory_dict["share_by_whatsapp"] = share_by_whatsapp if share_by_whatsapp else None
        
        if product_details is not None:
            data = vars(product_details.copy())
        else:
            data = {}

        # Only include created_updated_data_pro if data exists
        product_details_response = {}
        if data:
            product_details_response = {**data, **created_updated_data_pro}
        else:
            product_details_response = {}

        response_data.append({
            "inventory": inventory_dict,
            "inventory_remark": remark_list if remark_list else [],
            "Created_by": creator_info,
            "approved_by": approver_info,
            "product_details": product_details_response,
            "delivery_challan": {
            **(delivery_challan.dict() if delivery_challan else {}),
            **created_updated_data
            },
            "vendor": vendor
        })

    return {
    "status": "true", 
    "message": "Data Retrieved Successfully", 
    "today_dispatch_count": today_dispatch_count,
    "transit_count": transit_count,
    "complete_count": complete_count,
    "data": response_data}

    
    
    