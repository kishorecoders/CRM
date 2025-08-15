from .models import Quotation, QuotationCreate,Quotationupdate, Convertorder
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status, HTTPException
from src.Settings.models import Setting
from sqlalchemy import func
from src.StoreManagerProduct.models import storeManagerProduct
from src.AdminSales.models import AdminSales
from src.QuotationProductEmployee.models import QuotationProductEmployeeCreateList,QuotationProductEmployee
from src.ProductStages.models import ProductStages
from datetime import datetime, timedelta
from src.QuotationCustomer.models import QuotationCustomer
from datetime import date
from sqlalchemy import and_, extract
from src.Quotation_stages.models import QuotationStages
from src.AdminAddEmployee.models import AdminAddEmployee
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew
from src.cre_upd_name import get_creator_updator_info
from src.Notifications.models import Notification

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_all_quotation(db: Session):
    data = db.query(Quotation).order_by(Quotation.id.desc()).all()
    response = {'status': 'true',
                'message': "Data Received Successfully", 'data': data}
    return response





from src.Quotation_stages.models import QuotationStages
from src.StepItems.models import StepItems

def create(db: Session, quotation_create: QuotationCreate):
    if not quotation_create.lead_id:
        return {
            'status': 'false',
            'message': "Lead ID is required."
        }

    if not quotation_create.products:
        return {
            'status': 'false',
            'message': "Quotation cannot be created without products."
        }

    max_total_hours = 0  

    for product in quotation_create.products:
        total_hours = 0  

        for stage in product.stages:
            try:
                time_required = int(stage.time_riquired_for_this_process)
            except ValueError:
                return {
                    'status': 'false',
                    'message': f"Invalid time format for stage {stage.steps}. Must be a number."
                }

            if stage.day.lower() == "days":
                total_hours += time_required * 24
            elif stage.day.lower() == "week":
                total_hours += time_required * 7 * 24
            elif stage.day.lower() == "hours":
                total_hours += time_required
            else:
                return {
                    'status': 'false',
                    'message': f"Invalid time unit '{stage.day}' for stage {stage.steps}. Use 'Days', 'Hours', or 'Weeks'."
                }

        
        max_total_hours = max(max_total_hours, total_hours)

    
    required_delivery_date = datetime.today() + timedelta(hours=max_total_hours)
    delivery_date = datetime.strptime(quotation_create.delevery_date, "%Y-%m-%d")

    if delivery_date < required_delivery_date:
        return {
            'status': 'false',
            'message': f"Delivery date {delivery_date.strftime('%d-%m-%Y')} must be at least {required_delivery_date.strftime('%d-%m-%Y %H:%M:%S')} for the product requiring the longest time."
        }

    
    db_quotation = Quotation(**quotation_create.dict(exclude={"products"}))
    db.add(db_quotation)
    db.commit()
    db.refresh(db_quotation)

    empname = None
    if quotation_create.created_by_type == "employee":
        empname = db.query(AdminAddEmployee.employe_name).filter(AdminAddEmployee.id == quotation_create.employe_id).first()
    else:
        empname = db.query(SuperAdminUserAddNew.full_name).filter(SuperAdminUserAddNew.id == quotation_create.admin_id).first()
    # Create notification for the admin
    notification = Notification(
        admin_id=quotation_create.admin_id,
        title="New Quotation Created",
        description=f"A new quotation has been created by {empname}.",
        type="quotation",
        object_id=str(db_quotation.id),
        created_by_id=quotation_create.admin_emp_id,
        created_by_type=quotation_create.created_by_type
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)


    db_quotation.quotation_status = quotation_create.quotation_status
    db.commit()
    
    comments=[]

    for product in quotation_create.products:
        product_dict = product.dict(exclude={"stages"})
        product_dict["admin_id"] = quotation_create.admin_id
        product_dict["employee_id"] = quotation_create.employe_id
        product_dict["quote_id"] = db_quotation.id
        product_dict["lead_id"] = db_quotation.lead_id

        products = db.query(storeManagerProduct).filter(storeManagerProduct.item_code == product.product_code).first()
        if products is not None:
            product_dict["product_type"] = products.type

        db_product = QuotationProductEmployee(**product_dict)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)

        for stage in product.stages:
            stage_dict = stage.dict()
            stage_dict["admin_id"] = quotation_create.admin_id
            stage_dict["product_id"] = db_product.id

            db_stage = ProductStages(**stage_dict)
            db.add(db_stage)
            db.flush()

            if db_stage.parent_stage_id is not None:
                comments.append("This is an parent_stage_id log")
                logger.info("This is an parent_stage_id log", db_stage.parent_stage_id)
                query = db.query(ProductStages).filter(ProductStages.id == int(db_stage.parent_stage_id)).first()
                # comments.append(query)

                if query:
                    product_ids = [] if query.selected_product_ids is None else list(map(int,query.selected_product_ids.split(",")))
                    #comments.append(query.selected_product_ids)
                    # comments.append(product_ids)

                    products =[]
                    for product_id in product_ids:
                        comments.append(f"Product loop start {product_id}")
                    
                        # comments.append( type(product_id))
                        id = db.query(storeManagerProduct).filter(storeManagerProduct.id == (product_id)).first()
                        if id:
                            products.append(id)
                            comments.append("Product id found")
                    comments.append(f"Product loop end {len(products)}")
                    for product in products:
                        comments.append(f"Product loop start {product.id}")
                    
                        spitem = StepItems(
                            admin_id=quotation_create.admin_id,
                            employe_id=quotation_create.employe_id,
                            step_id=0,
                            item_name=product.product_tital,
                            discription=product.item_code,
                            product_id=product.id,
                            aval_quantity=product.opening_stock,
                            stage_id=db_stage.id,
                        )
                        
                        db.add(spitem)
                        db.flush()
                        
                        
                        comments.append(f"This is an StepItems log {spitem.id} ")
                        
                        
                        
                    db.commit() 

            product_stage = db.query(ProductStages).filter(ProductStages.id == stage.stage_id).first()
            if product_stage :
                db_quot_stage = QuotationStages(**stage_dict)
                db.add(db_quot_stage)
                db.commit()

    db.commit()

    get_quot_data = get_quotation_by_admin_id(
        admin_id=quotation_create.admin_id,
        emp_id=quotation_create.employe_id,
        db=db,
        quote_id=db_quotation.id
    )

    return {
        'status': 'true',
        'message': "Quotation, Products, and Stages Added Successfully",
        'comments':comments,
        "data": get_quot_data if get_quot_data else None
    }


from src.PaymentTerm.models import PaymentTerm
from src.TermAndConditions.models import TermAndCondition
from src.Bank.models import Bank


def safe_float(value):
    """Convert a value to float, default to 0 if conversion fails."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0

def get_quotation_by_admin_id(
        admin_id: str, 
        db: Session,        
        emp_id: Optional[str] = None,
        from_admin_id: Optional[str] = None,
        quote_id: Optional[int] = None, 
        month_year: Optional[str] = None ,
        quotation_status: Optional[int] = None ,
        page: int = 0, 
        page_size: int = 0, 
        status_filter: Optional[str] = None,
        date_filter: Optional[str] = None):  
      
      
    # from_admin_id takes priority, filter strictly by that and no employee
    if from_admin_id:
        query = db.query(Quotation).filter(
            Quotation.admin_id == from_admin_id,
            (Quotation.employe_id == None) | (Quotation.employe_id == "")
        )
    else:
        # Default case: admin_id is mandatory
        query = db.query(Quotation).filter(Quotation.admin_id == admin_id)

        if emp_id:
            query = query.filter(Quotation.employe_id == emp_id)


    #query = db.query(Quotation).filter(Quotation.admin_id == admin_id)

    #if emp_id:
    #    query = query.filter(Quotation.employe_id == emp_id)

    if quote_id:
        query = query.filter(Quotation.id == quote_id)

    if quotation_status is not None:  
        query = query.filter(Quotation.quotation_status == quotation_status)

    if month_year: 
        year, month = map(int ,month_year.split('-'))  
        query = query.filter(
            and_(
                extract('year', Quotation.created_at) == year,
                extract('month', Quotation.created_at) == month
            )
        )

    today = date.today()
    
    if status_filter == "This Month":
        query = query.filter(
            Quotation.delevery_date >= today.replace(day=1),
            Quotation.delevery_date < (today.replace(day=1).replace(month=today.month + 1) if today.month < 12 else today.replace(day=1, month=1, year=today.year + 1))
        )
    elif status_filter == "Last Month":
        last_month = today.replace(day=1).replace(month=today.month - 1) if today.month > 1 else today.replace(day=1, month=12, year=today.year - 1)
        query = query.filter(
            Quotation.delevery_date >= last_month,
            Quotation.delevery_date < today.replace(day=1)
        )
    elif status_filter == "Expired":
        query = query.filter(Quotation.delevery_date < today)
    elif status_filter == "Not Expired":
        query = query.filter(Quotation.delevery_date > today)
    elif status_filter == "Pending Approval":
        query = query.filter(Quotation.status == 1)

    elif status_filter == "Complete":
        query = query.filter(Quotation.status == 2,Quotation.comver_order_status == "Complete")


    # Apply filter for specific month and year in format "MMM YYYY"
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, "%b %Y")
            query = query.filter(
                Quotation.delevery_date >= filter_date.replace(day=1),
                Quotation.delevery_date < (filter_date.replace(day=1).replace(month=filter_date.month + 1) if filter_date.month < 12 else filter_date.replace(day=1, month=1, year=filter_date.year + 1))
            )
        except ValueError:
            pass  # Ignore invalid date format

    query = query.order_by(Quotation.id.desc())

    # Pagination logic
    if page > 0 and page_size > 0:
        total_count = query.count()
        data = query.offset((page - 1) * page_size).limit(page_size).all()
        has_previous = page > 1
        has_next = (page * page_size) < total_count
    else:
        data = query.all()
        has_previous = False
        has_next = False

    response_data = []
    total_amount_sum = sum(safe_float(item.total_amount) for item in data)
    total_pre_tax_sum = 0  # Pre-tax amount sum

    bank_details = {}
    term_and_condition_details = {}
    payment_term_details = []

    for item in data:
    

        bank = db.query(Bank).filter(Bank.id == item.bank_detail).first()
        if bank is not None:
            bank_details = {
                'id': bank.id,
                'bank_name': bank.bank_name,
                'branch': bank.branch,
                'account_number': bank.account_number,
                'ifsc_code': bank.ifsc_code,
                'is_default': bank.is_default
            }
        
        termAndConditions = db.query(PaymentTerm).filter(PaymentTerm.id == item.term_and_condition).first()
        if termAndConditions is not None:
            term_and_condition_details = {
                'id': termAndConditions.id,
                'admin_id': termAndConditions.admin_id,
                'type': termAndConditions.type,
                'file_path': termAndConditions.file_path,
                'content': termAndConditions.content
            }

        payment_term_details = []
        
        if item.payment_term:
            for id in item.payment_term.split(","):
                id = int(id.strip())
                payment = db.query(PaymentTerm).filter(PaymentTerm.id == id).first()
                if payment is not None:
                    payment_term_details.append({
                        'id': payment.id,
                        'admin_id': payment.admin_id,
                        'type': payment.type,
                        'file_path': payment.file_path,
                        'content': payment.content
                    })
                        

        created_updated_data = get_creator_updator_info(
            admin_emp_id=item.admin_emp_id,
            created_by_type=item.created_by_type,
            updated_admin_emp_id=item.updated_admin_emp_id,
            updated_by_type=item.updated_by_type,
          db=db
        )

        product_details = []  # Initialize empty list for products
        total_amount = 0
        pre_tax_amount = 0

        # Fetch all products for this quotation
        products = db.query(QuotationProductEmployee).filter(
            QuotationProductEmployee.quote_id == item.id
        ).all()

        for product in products:
            price_per_product = product.rate_per_unit
            gst_rate = product.gst_percentage / 100
            total_product_amount = price_per_product + (price_per_product * gst_rate)
            total_quantity_amount = total_product_amount * product.quantity
            total_amount += total_quantity_amount

            # Calculate Pre-tax amount
            pre_tax_amount += price_per_product * product.quantity  

            # Fetch product stages
            stages_query = db.query(ProductStages).filter(
                ProductStages.product_id == product.id
                #ProductStages.type == "Lead"
            )
            stages = stages_query.all()

            stage_details = [
                {
                    'id': stage.id,
                    'steps': stage.steps,
                    'time_riquired_for_this_process': stage.time_riquired_for_this_process,
                    'day': stage.day,
                    'assign_employee': stage.assign_employee,
                    'parent_stage_id': stage.parent_stage_id,
                    'type': stage.type
                }
                for stage in stages
            ]




            Quotation_stage_details = []
            quotation_stages = db.query(QuotationStages).filter(QuotationStages.product_id == product.id).all()
            for qstage in quotation_stages:
                 product_stage=db.query(ProductStages).filter(ProductStages.id== f'{qstage.stage_id}').first()
                 if product_stage :
                    # quotation_stages_by_stage_id=db.query(QuotationStages).filter(QuotationStages.product_id == f'{product.get("id")}' and f'{product_stage.id}'==qstage.stage_id).all()

                    # quotation_stages_by_stage_id=db.query(QuotationStages).filter(QuotationStages.product_id == product.id and f'{product_stage.id}'==qstage.stage_id).first()

                    quotation_stages_by_stage_id = db.query(QuotationStages).filter(QuotationStages.product_id == product.id,QuotationStages.stage_id == product_stage.id).first()
                    # Quotation_stage_details= {
                    #     "id":product_stage.id,
                    #     "steps": product_stage.steps,
                    #     "time_riquired_for_this_process": product_stage.time_riquired_for_this_process,
                    #     "day": product_stage.day,
                    #     "quotation_stages_list":quotation_stages_by_stage_id
                    # }
                    Quotation_stage_details.append({
                        "id": product_stage.id,
                        "steps": product_stage.steps,
                        "time_riquired_for_this_process": product_stage.time_riquired_for_this_process,
                        "day": product_stage.day,
                        "quotation_stages_list": quotation_stages_by_stage_id
                    })


            product_detail = {
                'id': product.id,
                'product_name': product.product_name,
                'product_code': product.product_code,
                'hsn_code': product.hsn_code,
                'rate_per_unit': price_per_product,
                'quantity': product.quantity,
                'total': product.total,
                'total_product_amount': total_product_amount,
                'total_quantity_amount': total_quantity_amount,
                'gst_percentage': product.gst_percentage,
                'gross_total': product.gross_total,
                'availability': product.availability,
                'discount_type': product.discount_type,
                'discount_amount': product.discount_amount,
                'discount_percent': product.discount_percent,
                'unit': product.unit,
                'discription': product.discription,
                'product_id': product.product_id,
                'product_payment_type': product.product_payment_type,
                'product_cash_balance': product.product_cash_balance,
                'product_account_balance': product.product_account_balance,
                'specification':product.specification,
                'available_quantity':product.available_quantity,
                'manufacture_quantity':product.manufacture_quantity,
                'stages': stage_details,
                'Quotation_stages': Quotation_stage_details if Quotation_stage_details else None
            }
            product_details.append(product_detail)  # Append each product correctly

        total_pre_tax_sum += pre_tax_amount

        admin_sales_details = db.query(AdminSales).filter(
            AdminSales.id == item.lead_id
        ).first()

        admin_sales_info = {}
        if admin_sales_details:
            admin_sales_info = {
                'id': admin_sales_details.id,
                'lead_source': admin_sales_details.lead_source,
                'name': admin_sales_details.name,
                'lead_status': admin_sales_details.lead_status,
                'allocated_employee_id': admin_sales_details.allocated_emplyee_id,
                'contact_details': admin_sales_details.contact_details,
                'business_name': admin_sales_details.business_name,
                'profile_image': admin_sales_details.profile_image,
                'status': admin_sales_details.status,
                'address': admin_sales_details.address,
                'description': admin_sales_details.discription,
                'gst_number': admin_sales_details.gst_number,
                'city': admin_sales_details.city,
                'pincode': admin_sales_details.pincode,
                'state': admin_sales_details.state,
                'mark_status': admin_sales_details.mark_status
            }

        customer_info = {}
        if item.customer_id:
            customer_details = db.query(QuotationCustomer).filter(
                QuotationCustomer.id == item.customer_id
            ).first()

            if customer_details:
                customer_info = {
                    'id': customer_details.id,
                    'first_name': customer_details.first_name,
                    'last_name': customer_details.last_name,
                    'gender': customer_details.gender,
                    'company_name': customer_details.company_name,
                    'contact_number': customer_details.contact_number,
                    'email': customer_details.email,
                    'customer_type': customer_details.customer_type,
                    'website': customer_details.website,
                    'industry_and_segment': customer_details.industry_and_segment,
                    'country': customer_details.country,
                    'state': customer_details.state,
                    'city': customer_details.city,
                    'receivables': customer_details.receivables
                }

        admin_emp_name = ''
        if item.admin_emp_id:
            if item.created_by_type == 'employee':
                empd = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == int(item.admin_emp_id)).first()
                if empd:
                    admin_emp_name=f"{empd.employe_name}({empd.employee_id})"
            if item.created_by_type == 'admin':
                empd = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == int(item.admin_emp_id)).first()
                if empd:
                    admin_emp_name=f"{empd.full_name}(Admin)"
            

        quotation_data = {
            'id': item.id,
            'quotation_date': item.quotation_date,
            'lead_id': item.lead_id,
            'quotation_number': item.quotation_number,
            'sales_person': item.sales_persone,
            'customer_notes': item.customer_notes,
            'description': item.discription,
            'discount': item.discount,
            'expiry_date': item.expiry_date,
            'employee_id': item.employe_id,
            'reference': item.reference,
            'subject': item.subject,
            'terms_condition': item.terms_condition,
            'created_at': item.created_at,
            'updated_at' : item.updated_at,
            "delivery_date": item.delevery_date,
            'delivery_address': item.delevery_address,
            'payment_term': item.payment_term,
            'product_details': product_details,
            'total_amount': item.total_amount,
            'admin_sales_details': admin_sales_info,
            'customer_detail': customer_info,
            'discount_percent': item.discount_percent,
            'series': item.series,
            'contact_person': item.contact_person,
            'sales_credit': item.sales_credit,
            'shipping_address': item.shipping_address,
            'note': item.note,
            'bank_detail': item.bank_detail,
            'file': item.file,
            'save_as_template': item.save_as_template,
            'share_by_email': item.share_by_email,
            'share_by_whatsapp': item.share_by_whatsapp,
            'site_name': item.site_name,
            'self_company': item.self_company,
            'customer_id': item.customer_id,
            'status':item.status,
            'account_status':item.account_status,
            'quotation_status': item.quotation_status,
            'created_by_type': item.created_by_type,
            'admin_emp_id': item.admin_emp_id,
            'admin_emp_name': admin_emp_name,
            'sales_credit_id':item.sales_credit_id,
            'comver_order_status': item.comver_order_status,
            'updated_by_type' : item.updated_by_type,
            'updated_admin_emp_id' : item.updated_admin_emp_id,
            'discount_type' : item.discount_type,
            'bank_details': bank_details if bank else None,
            'payment_term_details': payment_term_details if payment_term_details else None,
            'term_and_condition_details': term_and_condition_details if term_and_condition_details else None

        }
        response_data.append({**quotation_data,**created_updated_data})

    return {
        'status': 'true',
        'message': "Data Received Successfully",
        'previous': has_previous,
        'next': has_next,
        'total_records': total_count if page > 0 and page_size > 0 else len(response_data),  
        'total_amount': total_amount_sum,
        'pre_tax_amount': total_pre_tax_sum,
        'data': response_data,
    }







    
    
    
    
    
    
    
from src.parameter import get_current_datetime


def update_quotation(quotation_id: int, quotation: Quotationupdate, db: Session):


    max_total_hours = 0

    if quotation.delevery_date:
        for product in quotation.products:
            total_hours = 0

            for stage in product.stages:
                try:
                    time_required = int(stage.time_riquired_for_this_process)
                except ValueError:
                    return {
                        'status': 'false',
                        'message': f"Invalid time format for stage {stage.steps}. Must be a number."
                    }

                if stage.day.lower() == "days":
                    total_hours += time_required * 24
                elif stage.day.lower() == "week":
                    total_hours += time_required * 7 * 24
                elif stage.day.lower() == "hours":
                    total_hours += time_required
                else:
                    return {
                        'status': 'false',
                        'message': f"Invalid time unit '{stage.day}' for stage {stage.steps}. Use 'Days', 'Hours', or 'Weeks'."
                    }

            max_total_hours = max(max_total_hours, total_hours)

        required_delivery_date = datetime.today() + timedelta(hours=max_total_hours)
        try:
            delevery_date = datetime.strptime(quotation.delevery_date, "%Y-%m-%d")
        except ValueError:
            return {
                'status': 'false',
                'message': f"Invalid delivery date format: {quotation.delivery_date}. Use 'YYYY-MM-DD'."
            }

        if delevery_date < required_delivery_date:
            return {
                'status': 'false',
                'message': f"Delivery date {delevery_date.strftime('%d-%m-%Y')} must be at least {required_delivery_date.strftime('%d-%m-%Y %H:%M:%S')} for the product requiring the longest time."
            }  





   
    quotation_data = quotation.dict(exclude_unset=True, exclude={"products"})
    quotation_data["updated_at"] = get_current_datetime()

    db.query(Quotation).filter(Quotation.id == quotation_id).update(quotation_data)
    db.commit()

    
    existing_products = db.query(QuotationProductEmployee).filter(
        QuotationProductEmployee.quote_id == quotation_id
    ).all()

    existing_product_ids = {product.id for product in existing_products if product.id}
    incoming_product_ids = {product.id for product in quotation.products if product.id}

    for product in quotation.products:
        if product.id and product.id in existing_product_ids:
            
            existing_product = db.query(QuotationProductEmployee).filter(
                QuotationProductEmployee.id == product.id
            ).first()

            if existing_product:
                product_data = product.dict(exclude_unset=True, exclude={"stages"})
                for key, value in product_data.items():
                    setattr(existing_product, key, value)
                db.add(existing_product)

                
                for stage in product.stages:
                    if stage.id:  
                        existing_stage = db.query(ProductStages).filter(
                            ProductStages.id == stage.id
                        ).first()
                        if existing_stage:
                            stage_data = stage.dict(exclude_unset=True)
                            for key, value in stage_data.items():
                                setattr(existing_stage, key, value)
                            db.add(existing_stage)
                            
                        stage_dict = stage.dict()
                        stage_dict["admin_id"] = stage.admin_id
                        stage_dict["product_id"] = existing_product.id
                        product_stage = db.query(ProductStages).filter(ProductStages.id == stage.stage_id).first()

                        if product_stage :
                            db_quot_stage = QuotationStages(**stage_dict)
                            db.add(db_quot_stage)
                            db.commit()
                            
                            
                    else:  
                        new_stage = ProductStages(
                            admin_id=stage.admin_id,
                            product_id=existing_product.id,
                            assign_employee=stage.assign_employee,
                            steps=stage.steps,
                            time_riquired_for_this_process=stage.time_riquired_for_this_process,
                            day=stage.day,
                            type=stage.type,
                        )
                        db.add(new_stage)
                        
                        stage_dict = stage.dict()
                        stage_dict["admin_id"] = stage.admin_id
                        stage_dict["product_id"] = existing_product.id
                        product_stage = db.query(ProductStages).filter(ProductStages.id == stage.stage_id).first()

                        if product_stage :
                            db_quot_stage = QuotationStages(**stage_dict)
                            db.add(db_quot_stage)
                            db.commit()
        else:
           
            new_product = QuotationProductEmployee(
                admin_id=product.admin_id,
                employee_id=product.employee_id,
                quote_id=quotation_id,
                lead_id=product.lead_id,
                product_name=product.product_name,
                product_code=product.product_code,
                hsn_code=product.hsn_code,
                rate_per_unit=product.rate_per_unit,
                quantity=product.quantity,
                total=product.total,
                gst_percentage=product.gst_percentage,
                gross_total=product.gross_total,
                availability=product.availability,
                discount_type=product.discount_type,
                discount_amount=product.discount_amount,
                discount_percent=product.discount_percent,
                unit=product.unit,
                product_payment_type=product.product_payment_type,
                product_cash_balance=product.product_cash_balance,
                product_account_balance=product.product_account_balance,
                #product_type=product.product_type,
                manufacture_quantity=product.manufacture_quantity,
                available_quantity=product.available_quantity,
                
                product_id=product.product_id,
                specification=product.specification,


            )
            db.add(new_product)
            db.commit()

            
            for stage in product.stages:
                new_stage = ProductStages(
                    admin_id=stage.admin_id,
                    product_id=new_product.id,
                    assign_employee=stage.assign_employee,
                    steps=stage.steps,
                    time_riquired_for_this_process=stage.time_riquired_for_this_process,
                    day=stage.day,
                    type=stage.type,
                )
                db.add(new_stage)

                stage_dict = stage.dict()
                stage_dict["admin_id"] = stage.admin_id
                stage_dict["product_id"] = new_product.id
                product_stage = db.query(ProductStages).filter(ProductStages.id == stage.stage_id).first()

                if product_stage :
                    db_quot_stage = QuotationStages(**stage_dict)
                    db.add(db_quot_stage)
            db.commit()

    products_to_delete = existing_product_ids - incoming_product_ids
    if products_to_delete:
        db.query(ProductStages).filter(
            ProductStages.product_id.in_(products_to_delete)
        ).delete(synchronize_session=False)
        db.query(QuotationProductEmployee).filter(
            QuotationProductEmployee.id.in_(products_to_delete)
        ).delete(synchronize_session=False)

    db.commit()
    return {"status": "true", "message": f"Quotation, products, and stages updated successfully{quotation.quotation_status}"}






# def delete_quotation(quotation_id: int, db: Session):
#     quotation = db.query(Quotation).filter(
#         Quotation.id == quotation_id).first()
#     if quotation:
#         db.delete(quotation)
#         db.commit()
#         return {'status': 'true', 'message': "Quotation deleted successfully", 'data': quotation}
#     return {"status": 'false',  'message': "Quotation not found"}


def delete_quotation(quotation_id: int, db: Session):
    
    quotation = db.query(Quotation).filter(Quotation.id == quotation_id).first()
    if not quotation:
        return {"status": "false", "message": "Quotation not found"}

   
    db.query(QuotationProductEmployee).filter(
        QuotationProductEmployee.quote_id == quotation_id
    ).delete(synchronize_session=False)

   
    db.delete(quotation)
    db.commit()

    return {"status": "true", "message": "Quotation and its products deleted successfully"}
    

def generate_order_id(db: Session, admin_id: str):
    admin_company_name = db.query(SuperAdminUserAddNew.company_name).filter(SuperAdminUserAddNew.id == admin_id).scalar()
    short_name = admin_company_name[:4].upper()
    current_year = datetime.now().year % 100
    next_year = current_year + 1
    
    prefix = f"{short_name}/{current_year:02d}-{next_year:02d}/"
    latest_order = (
        db.query(func.max(ProjectManagerOrder.order_id))
        .filter(ProjectManagerOrder.order_id.like(f"{prefix}%"))
        .scalar()
    )

    existing_order_number = int(latest_order.split('/')[-1]) if latest_order else 0
    new_order_number = existing_order_number + 1
    return f"{prefix}{new_order_number:03d}"



import json
from src.Account.service import save_base64_file
from src.ProjectManagerResourseFile.models import ProjectManagerResourseFile
from src.AdminSales.models import AdminSales
from src.ProjectManagerOrder.models import ProjectManagerOrder

def convert_order(admin_sales_data: Convertorder, db: Session):

    # uploaded_files = []  # collect file info for the response

    if admin_sales_data.employe_id:
        created_by_type = "employee"
        admin_emp_id = admin_sales_data.employe_id
    else:
        created_by_type = "admin"
        admin_emp_id = admin_sales_data.admin_id  

    if admin_sales_data.Product_details:
        for pro in admin_sales_data.Product_details:
            prod = db.query(QuotationProductEmployee).filter(QuotationProductEmployee.id == int(pro.product_id)).first()
            std = db.query(storeManagerProduct).filter(storeManagerProduct.item_code == pro.product_code).first()

            if prod and std:
                prod.manufacture_quantity = pro.manufacture_quantity
                prod.available_quantity = pro.available_quantity
                std.opening_stock = str(int(std.opening_stock) - int(pro.available_quantity))
        db.commit()



    if admin_sales_data.files:
        file_data = []
        for f in admin_sales_data.files:
            current_datetime = datetime.now().strftime("%Y%m%d%H%M%S%f")
            # file_extension = "pdf" if f.file_type == "pdf" else "jpg"
            file_extension = "pdf"
            filename = f"{current_datetime}_{f.file_name}.{file_extension}"
            path = save_base64_file(f.file_path, filename)
            # Create file data dict
            file_info = {
                "file_name": f.file_name,
                "file_path": path
            }
            # uploaded_files.append(file_info)
            file_data.append(file_info)

            # Store file info in ProjectManagerResourseFile
            res_file = ProjectManagerResourseFile(
                admin_id=admin_sales_data.admin_id,
                emp_id=admin_sales_data.employe_id if admin_sales_data.employe_id else 0,
                lead_id=str(admin_sales_data.lead_id),
                quotation_id=str(admin_sales_data.quotation_id),
                file_path=json.dumps(file_info)
            )
            db.add(res_file)
            db.commit()
        
        quot = db.query(Quotation).filter(Quotation.id == admin_sales_data.quotation_id).first()
        if not quot:
            return {'status': 'false', 
                  'message': "Quotation not found"
                  }
    
        quot.comver_order_status = "Complete"
        quot.quotation_status = 5
        db.commit()

        admin_sales_record = db.query(AdminSales).filter(AdminSales.id == admin_sales_data.lead_id).first()
        admin_sales_record.status = "Won"
        db.add(admin_sales_record)
        
        project_order_data = ProjectManagerOrder(
            admin_id=admin_sales_record.admin_id,
            emplpoyee_id=admin_sales_record.allocated_emplyee_id,
            customer_name=admin_sales_record.name, 
            customer_email_id=admin_sales_record.email,
            customer_company=admin_sales_record.business_name,
            customer_contact=admin_sales_record.contact_details,
            order_id=generate_order_id(db, admin_sales_record.admin_id),
            product_id=str(admin_sales_data.lead_id),
            new_quantity="1",
            request_date=str(datetime.now()),
            sales_persone_name=quot.contact_person if quot.contact_person else "",
            status="Won",
            order_by="Lead",
            lead_id=admin_sales_record.id,
            quotation_id=admin_sales_data.quotation_id,
            admin_emp_id=admin_emp_id,
            created_by_type=created_by_type,
        )


        db.add(project_order_data)
        db.commit()
        db.refresh(project_order_data)

        empname = None
        if project_order_data.created_by_type == "employee":
            empname = db.query(AdminAddEmployee.employe_name).filter(AdminAddEmployee.id == project_order_data.admin_emp_id).first()
        else:
            empname = db.query(SuperAdminUserAddNew.full_name).filter(SuperAdminUserAddNew.id == project_order_data.admin_id).first()
        # Create notification for the admin
        notification = Notification(
            admin_id=project_order_data.admin_id,
            title="New ProjectManagerOrder Created",
            description=f"A new ProjectManagerOrder has been created by {empname}.",
            type="ProjectManagerOrder",
            object_id=str(project_order_data.id),
            created_by_id=project_order_data.admin_emp_id,
            created_by_type=project_order_data.created_by_type
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
            
            
    return {'status': 'true', 
            'message': "Data Updated Successfully", 
            }
    
    