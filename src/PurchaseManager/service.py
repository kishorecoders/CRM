from .models import PurchaseManger,PurchaseMangerCreate
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status,HTTPException
from sqlalchemy import func
from src.StoreManagerProduct.models import storeManagerProduct
from src.Category.models import Category
from src.Productwisestock.models import ProductWiseStock
from src.StoreManagerPurchase.models import StoreManagerPurchase
from src.PurchaseOrderIssue.models import PurchaseOrderIssue
from sqlalchemy import and_

def get_all_purcahse_manager(db: Session):
    data = db.query(PurchaseManger).order_by(PurchaseManger.id.desc()).all()
    response = {'status': 'true', 'message': "Data Received Successfully", 'data': data}
    return response

# def create(db: Session, purcahse_manager_create: PurchaseMangerCreate):
#     db_purcahse_manager = PurchaseManger(**purcahse_manager_create.dict())
#     db.add(db_purcahse_manager)
#     db.commit()
#     db.refresh(db_purcahse_manager)
#     response = {'status': 'true','message':"Purchase Manager Details Added Successfully",'data':db_purcahse_manager}
#     return response

# def create(db: Session, purchase_manager_create: PurchaseMangerCreate):
#         # Extract necessary information from purchase_manager_create
#         admin_id = purchase_manager_create.admin_id
#         request_id = purchase_manager_create.request_id
#         product_id = purchase_manager_create.product_id
#         store_manager_order_id = purchase_manager_create.store_manager_order_id
#         take_action = purchase_manager_create.take_action

#         # Check if the provided admin_id, request_id, and any of the product_ids exist in store_manager_purchase
#         existing_entry = db.query(StoreManagerPurchase).filter(StoreManagerPurchase.admin_id == admin_id).filter(StoreManagerPurchase.request_id == request_id).first()
#         if not existing_entry:
#             return {"No matching entry found in store_manager_purchase for provided admin_id and request_id."}

#         # Split the stored product_ids into a list
#         stored_product_ids = list(map(int, existing_entry.product_id.split(',')))
        
#         same_product_entry = db.query(PurchaseManger).filter(PurchaseManger.admin_id == admin_id).filter(PurchaseManger.request_id == request_id).filter(PurchaseManger.product_id == product_id).first()
#         if same_product_entry:
#             return {f"Product_id {product_id} is already used for admin_id {admin_id} and request_id {request_id}."}

#         # Create a new row in the purchase_manager table
#         db_purchase_manager = PurchaseManger(admin_id=admin_id,
#                                               request_id=request_id,
#                                               product_id=product_id,
#                                               store_manager_order_id=store_manager_order_id,
#                                               take_action=take_action)

#         # Add the new row to the database session
#         db.add(db_purchase_manager)

#         # Update the entry in store_manager_purchase
#         existing_entry.admin_id = admin_id
#         existing_entry.request_status = 1

#         # Commit the changes to the database
#         db.commit()

#         # Refresh the db_purchase_manager instance to get the updated values
#         db.refresh(db_purchase_manager)

#         # Prepare the response
#         response = {
#             'status': 'true',
#             'message': "Purchase Manager Details Added Successfully",
#             'data': db_purchase_manager
#         }

#         return response

def create(db: Session, purchase_manager_create: PurchaseMangerCreate):
    admin_id = purchase_manager_create.admin_id
    request_id = purchase_manager_create.request_id
    product_id = purchase_manager_create.product_id
    store_manager_order_id = purchase_manager_create.store_manager_order_id
    request_purchase_quntity = purchase_manager_create.request_purchase_quntity
    take_action = purchase_manager_create.take_action

    
    existing_entry = db.query(StoreManagerPurchase).filter(
        StoreManagerPurchase.admin_id == admin_id,
        StoreManagerPurchase.request_id == request_id
    ).first()

    if not existing_entry:
        return {"status": "false", "message": "No matching entry found in store_manager_purchase for provided admin_id and request_id."}

    
    stored_product_ids = [pid.strip() for pid in existing_entry.product_id.split(',')]
    
    product_id = product_id.strip()

    
    if product_id not in stored_product_ids:
        return {"status": "false", "message": f"Product_id {product_id} is not associated with admin_id {admin_id} and request_id {request_id}."}

    
    same_product_entry = db.query(PurchaseManger).filter(
        PurchaseManger.admin_id == admin_id,
        PurchaseManger.request_id == request_id,
        PurchaseManger.product_id == product_id
    ).first()

    if same_product_entry:
        return {"status": "false", "message": f"Product_id {product_id} is already used for admin_id {admin_id} and request_id {request_id}."}

    
    db_purchase_manager = PurchaseManger(
        admin_id=admin_id,
        request_id=request_id,
        product_id=product_id,
        store_manager_order_id=store_manager_order_id,
        request_purchase_quntity=request_purchase_quntity,
        take_action=take_action
    )

    
    db.add(db_purchase_manager)   
    db.commit()
    
    db.refresh(db_purchase_manager)

    
    response = {
        'status': 'true',
        'message': "Purchase Manager Details Added Successfully",
        'data': db_purchase_manager
    }

    return response

def get_purcahse_manager_by_admin_id(admin_id: str, db: Session):
    data = db.query(PurchaseManger).filter(PurchaseManger.admin_id == admin_id).all()
    response = {'status': 'true','message':"Data Recived Successfully",'data':data}
    return response  

# def get_purcahse_manager_by_request_id(admin_id: str, request_id: str, db: Session):
#     array = []
#     PurchaseMangerList = db.query(PurchaseManger).filter(PurchaseManger.admin_id == admin_id).filter(PurchaseManger.request_id == request_id).filter(PurchaseManger.take_action == "1").all()
#     for purchaseManger in PurchaseMangerList:
#         productDetails = db.query(storeManagerProduct).filter(storeManagerProduct.id == purchaseManger.product_id).all()
#         storeManagerDetails = db.query(StoreManagerPurchase).filter(StoreManagerPurchase.id == purchaseManger.store_manager_order_id).all()
#         temp = {"purchase_manager_details":PurchaseMangerList,"product_details":productDetails, "store_manager_order_details":storeManagerDetails}
#         array.append(temp)
#     response = {'status': 'true','message':"Data Recived Successfully",'data':array}
#     return response


# def get_purcahse_manager_by_request(admin_id: str, request_id:str, db: Session):
#     array = []
#     grand_total = 0
    
#     # Querying PurchaseManager instances based on admin_id, request_id, and take_action
#     purchase_manager_list = db.query(PurchaseManger)\
#         .filter(PurchaseManger.admin_id == admin_id,
#                 PurchaseManger.request_id == request_id,
#                 PurchaseManger.take_action == "1")\
#         .all()

#     # Iterating through PurchaseManager instances
#     for purchase_manager in purchase_manager_list:
#         # Querying product details based on product_id
#         product_details = db.query(storeManagerProduct)\
#             .filter(storeManagerProduct.id == purchase_manager.product_id)\
#             .first()

#         # Querying store manager details based on store_manager_order_id
#         store_manager_details = db.query(StoreManagerPurchase)\
#             .filter(StoreManagerPurchase.id == purchase_manager.store_manager_order_id)\
#             .first()

#         # Converting character_variyng values to appropriate numeric types
#         price_per_product = float(product_details.price_per_product)
#         gst_rate = float(product_details.gst_rate.replace('%', '')) / 100  # Converting percentage to decimal

#         # Calculating total_amount by adding price_per_product and gst_rate
#         total_amount = price_per_product + (price_per_product * gst_rate)
        
#         # Adding total_amount to the grand total
#         grand_total += total_amount

#         # Constructing the temporary dictionary
#         temp = {
#             "purchase_manager_details": {**purchase_manager.__dict__,"total_amount": total_amount},
#             "product_details": product_details,
#             "store_manager_order_details": store_manager_details
#         }
#         array.append(temp)

#     # Constructing the response dictionary with grand_total
#     response = {
#         'status': 'true',
#         'message': "Data Received Successfully",
#         'data': array,
#         'grand_total': grand_total
#     }

#     return response

def get_purcahse_manager_by_request(admin_id: str, request_id: str, db: Session):
    array = []
    grand_total = 0
    
    
    purchase_manager_list = db.query(PurchaseManger)\
        .filter(PurchaseManger.admin_id == admin_id,
                PurchaseManger.request_id == request_id,
                PurchaseManger.take_action == "1")\
        .all()

    
    for purchase_manager in purchase_manager_list:
        
        product_details = db.query(storeManagerProduct)\
            .filter(storeManagerProduct.id == purchase_manager.product_id)\
            .first()

        
        store_manager_details = db.query(StoreManagerPurchase)\
            .filter(StoreManagerPurchase.id == purchase_manager.store_manager_order_id)\
            .first()

        
        issue_exist = db.query(PurchaseOrderIssue)\
            .filter(and_(PurchaseOrderIssue.admin_id == purchase_manager.admin_id,
                         PurchaseOrderIssue.product_id == purchase_manager.product_id,
                         PurchaseOrderIssue.purchase_request_id == request_id))\
            .first()

        if issue_exist:
            
            continue

        
        price_per_product = float(product_details.price_per_product)
        gst_rate = float(product_details.gst_rate.replace('%', '')) / 100  

       
        total_amount = price_per_product + (price_per_product * gst_rate)

        
        grand_total += total_amount

       
        temp = {
            "purchase_manager_details": {**purchase_manager.__dict__, "total_amount": total_amount},
            "product_details": product_details,
            "store_manager_order_details": store_manager_details
        }
        array.append(temp)

    
    response = {
        'status': 'true',
        'message': "Data Received Successfully",
        'data': array,
        'grand_total': grand_total
    }

    return response

def get_purchase_manager_by_request_ids(admin_id: str, db: Session):
     
    purchase_manager_list = db.query(PurchaseManger) \
        .filter(PurchaseManger.admin_id == admin_id,
                PurchaseManger.take_action == "1") \
        .all()
    
    subquery = db.query(
        PurchaseOrderIssue.purchase_request_id,
        PurchaseOrderIssue.product_id,
        func.count().label('count')
    ).group_by(
        PurchaseOrderIssue.purchase_request_id,
        PurchaseOrderIssue.product_id
    ).subquery()

    
    data_list = []
    
    response = {
        'status': 'true',
        'message': "Data Received Successfully",
        'data': data_list
    }
    
    for purchase_manager in purchase_manager_list:
       
        request_id = purchase_manager.request_id
        product_id = purchase_manager.product_id

        
        query_result = db.query(
            PurchaseManger,
            subquery.c.count
        ).outerjoin(
            subquery,
            PurchaseManger.request_id == subquery.c.purchase_request_id
        ).filter(
            PurchaseManger.admin_id == admin_id,
            PurchaseManger.take_action == "1",
            PurchaseManger.request_id == request_id,
            PurchaseManger.product_id == product_id
        ).first()

        
        if query_result:
            purchase_manager_instance, match_count = query_result
            if match_count is not None and match_count > 0:
                matching_request_id = purchase_manager_instance.request_id
                matching_product_id = purchase_manager_instance.product_id
                match_found = True
            else:
                matching_request_id = None
                matching_product_id = None
                match_found = False

            data = {
                "admin_id": admin_id,
                "request_id": request_id,
                "product_id": product_id,
                "matching_request_id": matching_request_id,
                "matching_product_id": matching_product_id,
                "match_found": match_found
            }
        else:
           
            data = {
                "admin_id": admin_id,
                "request_id": request_id,
                "product_id": product_id,
                "matching_request_id": None,
                "matching_product_id": None,
                "match_found": False
            }

        data_list.append(data)
        response['data'] = data_list

    return response

# def get_purcahse_manager_by_request(admin_id: str, db: Session):
#     # Initialize an empty array to store the results
#     array = []
#     grand_total = 0

#     # Querying PurchaseManager instances based on admin_id, request_id, and take_action
#     purchase_manager_list = db.query(PurchaseManger)\
#         .filter(PurchaseManger.admin_id == admin_id,
#                 PurchaseManger.take_action == "1")\
#         .all()

#     # Iterating through PurchaseManager instances
#     for purchase_manager in purchase_manager_list:
#         # Extract product_ids from each purchase_manager entry
#         product_ids = purchase_manager.product_id.split(',')

#         # Initialize an empty array to store product details for each purchase_manager
#         product_detail_array = []

#         # Iterate through each product_id in the split product_ids
#         for product_id in product_ids:
#             # Querying product details based on product_id
#             product_details = db.query(storeManagerProduct)\
#                 .filter(storeManagerProduct.id == int(product_id))\
#                 .first()

#             # Check if the product_details exist
#             if product_details:
#                 # Converting character_variying values to appropriate numeric types
#                 price_per_product = float(product_details.price_per_product)
#                 gst_rate = float(product_details.gst_rate.replace('%', '')) / 100  # Converting percentage to decimal

#                 # Calculating total_amount by adding price_per_product and gst_rate
#                 total_amount = price_per_product + (price_per_product * gst_rate)

#                 # Adding total_amount to the grand total
#                 grand_total += total_amount

#                 # Constructing the dictionary for each product detail
#                 product_detail = {
#                     **product_details.__dict__,
#                     'total_amount': total_amount
#                 }

#                 # Append product_detail to product_detail_array
#                 product_detail_array.append(product_detail)

#         # Querying store manager details based on store_manager_order_id
#         store_manager_details = db.query(StoreManagerPurchase)\
#             .filter(StoreManagerPurchase.id == purchase_manager.store_manager_order_id)\
#             .first()

#         # Constructing the temporary dictionary
#         temp = {
#             "purchase_manager_details": {**purchase_manager.__dict__, "total_amount": total_amount},
#             "product_details": product_detail_array,
#             "store_manager_order_details": store_manager_details
#         }

#         # Append temp to array
#         array.append(temp)

#     # Constructing the response dictionary with grand_total
#     response = {
#         'status': 'true',
#         'message': "Data Received Successfully",
#         'data': array,
#         'grand_total': grand_total
#     }

#     return response

def update(purchase_manager_id:int,purchase_manager:PurchaseManger,db:Session):
    purchase_manager_update = purchase_manager.dict(exclude_unset=True)
    db.query(PurchaseManger).filter(PurchaseManger.id == purchase_manager_id).update(purchase_manager_update)
    db.commit()
    response = {'status': 'true','message':"Purchase Manager Details Updated Successfully",'data':purchase_manager_update}
    return response

def delete_purcahse_manager_by_id(purchase_manager_id: int, db: Session):
    purchase_manage = db.query(PurchaseManger).filter(PurchaseManger.id == purchase_manager_id).first()
    if purchase_manage:
        db.delete(purchase_manage)
        db.commit()
        return {'status':'true', 'message':"Purchase Manager Details deleted successfully", 'data':purchase_manage}
    return {"status":'false',  'message':"Purchase Manager Details not found"}