from .models import Invoice, InvoiceCreate
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status, HTTPException
from src.Settings.models import Setting
from sqlalchemy import func
from src.StoreManagerProduct.models import storeManagerProduct
from src.AdminSales.models import AdminSales
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew
import requests
import json


def get_all_invoice(db: Session):
    data = db.query(Invoice).order_by(Invoice.id.desc()).all()
    response = {'status': 'true',
                'message': "Data Received Successfully", 'data': data}
    return response


def create(db: Session, invoice_create: InvoiceCreate):
    admin_id = invoice_create.admin_id

    
    setting = db.query(Setting).filter(Setting.admin_id == admin_id).first()

    
    if not setting or not setting.custom_series:
        
        return {'status': 'false',
                'message': "Please add custom_series in settings first"}

    
    custom_series = setting.custom_series

    
    latest_invoice = (
        db.query(func.max(Invoice.invoice_number))
        .filter(Invoice.admin_id == admin_id)
        .scalar()
    )

    
    if latest_invoice and '-' in latest_invoice:
        existing_invoice_number = int(latest_invoice.split('-')[-1])
    else:
        existing_invoice_number = 0

    
    new_invoice_number = f"{custom_series}-INV-{existing_invoice_number + 1:04d}"

    
    invoice_create.invoice_number = new_invoice_number

    
    db_invoice_create = Invoice(**invoice_create.dict())
    db.add(db_invoice_create)
    db.commit()
    db.refresh(db_invoice_create)

    response = {'status': 'true',
                'message': "Invoice Details Added Successfully",
                'data': db_invoice_create}
    return response

# def get_invoice_by_admin_id(admin_id: str, lead_id: str, db: Session):
#     data = db.query(Invoice).filter(Invoice.admin_id == admin_id, Invoice.admin_sales_id == lead_id).all()
#     response_data = []

#     for item in data:
#         product_ids = [int(pid) for pid in item.product_id.split(',')]
#         quantities = [int(qty) for qty in item.quantity.split(',')]
#         product_details = []

#         total_amount = 0
#         lead_details = db.query(AdminSales).filter(
#                 AdminSales.id == lead_id).first()

#         for pid, qty in zip(product_ids, quantities):
#             product = db.query(storeManagerProduct).filter(
#                 storeManagerProduct.id == pid).first()
#             if product:
#                 price_per_product = float(product.price_per_product)
#                 # Converting percentage to decimal
#                 gst_rate = float(product.gst_rate.replace('%', '')) / 100
#                 total_product_amount = price_per_product + \
#                     (price_per_product * gst_rate)  # Your calculation here
#                 total_quntity_amount = total_product_amount * qty

#                 total_amount += total_quntity_amount

#                 product_detail = {
#                     **product.__dict__,
#                     'price_per_product': price_per_product,
#                     'quantity': qty,
#                     'total_product_amount': total_product_amount,
#                     'total_quntity_amount': total_quntity_amount
#                 }
#                 product_details.append(product_detail)

#         quotation_data = {
#             'order': item.order,
#             'billing_country': item.billing_country,
#             'cgst': item.cgst,
#             'company_name': item.company_name,
#             'bank_charges': item.bank_charges,
#             'reference': item.reference,
#             'billing_pincode': item.billing_pincode,
#             'igst': item.igst,
#             'date': item.date,
#             'employe_id': item.employe_id,
#             'sales_persone': item.sales_persone,
#             'shipping_address': item.shipping_address,
#             'rounding': item.rounding,
#             'payment_mode': item.payment_mode,
#             'admin_id': item.admin_id,
#             'subject': item.subject,
#             'shipping_city': item.shipping_city,
#             'quantity': item.quantity,
#             'discount': item.discount,
#             'admin_sales_id': item.admin_sales_id,
#             'gst_treatment': item.gst_treatment,
#             'shipping_state': item.shipping_state,
#             'total': item.total,
#             'id': item.id,
#             'product_id': item.product_id,
#             'billing_address': item.billing_address,
#             'shipping_country': item.shipping_country,
#             'payment_made': item.payment_made,
#             'created_at': item.created_at,
#             'invoice_date': item.invoice_date,
#             'billing_city': item.billing_city,
#             'shipping_pincode': item.shipping_pincode,
#             'payment_option': item.payment_option,
#             'updated_at': item.updated_at,
#             'invoice_number': item.invoice_number,
#             'billing_state': item.billing_state,
#             'sgst': item.sgst,
#             'notes': item.notes,
#             'lead_details': lead_details,
#             'product_details': product_details,
#             'total_amount': total_amount
#         }

#         response_data.append(quotation_data)

#     response = {'status': 'true',
#                 'message': "Data Received Successfully",
#                 'data': response_data}
#     return response

def get_invoice_by_admin_id(admin_id: str, lead_id: str, db: Session):
    
    data = db.query(Invoice).filter(Invoice.admin_id == admin_id, Invoice.admin_sales_id == lead_id).all()
    
    
    super_admin = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == admin_id).first()
    if not super_admin:
        return {'status': 'false', 'message': "Admin ID not found"}

    
    gst_number_admin = super_admin.gst_number

    response_data = []

    for item in data:
        product_ids = [int(pid) for pid in item.product_id.split(',')]
        quantities = [int(qty) for qty in item.quantity.split(',')]
        product_details = []
        total_amount = 0

        for i in range(len(product_ids)):
            pid = product_ids[i]
            qty = quantities[i]
            
           
            product = db.query(storeManagerProduct).filter(storeManagerProduct.id == pid).first()
            if product:
                price_per_product = float(product.price_per_product)
                gst_rate = float(product.gst_rate.replace('%', '')) / 100
                
                state_admin = super_admin.state
                if not state_admin:
                    
                    gst_api_url_admin = f"http://sheet.gstincheck.co.in/check/5f7c17d9191442e48fe2e8dd43367a57/{gst_number_admin}/"
                    gst_response_admin = requests.get(gst_api_url_admin)
                    
                    if gst_response_admin.status_code == 200:
                        gst_details_admin = gst_response_admin.json()
                        state_admin = get_state_from_gst_api_response(gst_details_admin)
                        if state_admin:
                            super_admin.state = state_admin
                            db.commit()
                    else:
                        return {'status': 'false', 'message': "Failed to fetch GST details from API for admin"}

                sgst = cgst = igst = 0
                if state_admin:
                    
                    lead = db.query(AdminSales).filter(AdminSales.id == lead_id).first()
                    if lead:
                        state_lead = lead.state
                        if not state_lead:
                            
                            gst_number_lead = lead.gst_number

                           
                            gst_api_url_lead = f"http://sheet.gstincheck.co.in/check/5f7c17d9191442e48fe2e8dd43367a57/{gst_number_lead}/"
                            gst_response_lead = requests.get(gst_api_url_lead)

                            if gst_response_lead.status_code == 200:
                                gst_details_lead = gst_response_lead.json()
                                state_lead = get_state_from_gst_api_response(gst_details_lead)
                                if state_lead:
                                    lead.state = state_lead
                                    db.commit()
                            else:
                                return {'status': 'false', 'message': "Failed to fetch GST details from API for lead"}

                        
                        if state_admin == state_lead:
                            sgst = cgst = gst_rate / 2
                        else:
                            igst = gst_rate
                    else:
                        return {'status': 'false', 'message': "Lead ID not found"}

                
                total_product_amount = price_per_product * (1 + gst_rate)
                total_quantity_amount = total_product_amount * qty

                total_amount += total_quantity_amount
                
                
                sgst_amount = price_per_product * sgst if sgst != 0 else 0
                cgst_amount = price_per_product * cgst if cgst != 0 else 0
                igst_amount = price_per_product * igst if igst != 0 else 0

                
                product_detail = {
                    **product.__dict__,
                    'price_per_product': price_per_product,
                    'quantity': qty,
                    'total_product_amount': total_product_amount,
                    'total_quantity_amount': total_quantity_amount,
                    'sgst': sgst,
                    'cgst': cgst,
                    'igst': igst,
                    'sgst_amount': sgst_amount,
                    'cgst_amount': cgst_amount,
                    'igst_amount': igst_amount,
                }
                product_details.append(product_detail)

       
        quotation_data = {
            'order': item.order,
            'billing_country': item.billing_country,
            'cgst': item.cgst,
            'company_name': item.company_name,
            'bank_charges': item.bank_charges,
            'reference': item.reference,
            'billing_pincode': item.billing_pincode,
            'igst': item.igst,
            'date': item.date,
            'employe_id': item.employe_id,
            'sales_persone': item.sales_persone,
            'shipping_address': item.shipping_address,
            'rounding': item.rounding,
            'payment_mode': item.payment_mode,
            'admin_id': item.admin_id,
            'subject': item.subject,
            'shipping_city': item.shipping_city,
            'quantity': item.quantity,
            'discount': item.discount,
            'admin_sales_id': item.admin_sales_id,
            'gst_treatment': item.gst_treatment,
            'shipping_state': item.shipping_state,
            'total': item.total,
            'id': item.id,
            'product_id': item.product_id,
            'billing_address': item.billing_address,
            'shipping_country': item.shipping_country,
            'payment_made': item.payment_made,
            'created_at': item.created_at,
            'invoice_date': item.invoice_date,
            'billing_city': item.billing_city,
            'shipping_pincode': item.shipping_pincode,
            'payment_option': item.payment_option,
            'updated_at': item.updated_at,
            'invoice_number': item.invoice_number,
            'billing_state': item.billing_state,
            'sgst': item.sgst,
            'notes': item.notes,
            'lead_details': lead,
            'product_details': product_details,
            'total_amount': total_amount
        }

        response_data.append(quotation_data)

    
    response = {'status': 'true', 'message': "Data Received Successfully", 'data': response_data}
    return response

def get_state_from_gst_api_response(gst_details):
    try:
        state_info = gst_details.get('data', {}).get('stj', None)
        if state_info:
            state = state_info.split(',')[0].split('-')[-1].strip()
            return state
        else:
            return None
    except:
      return None

def update(invoice_id: int, invoice: Invoice, db: Session):
    invoice_update = invoice.dict(exclude_unset=True)
    db.query(Invoice).filter(Invoice.id == invoice_id).update(invoice_update)
    db.commit()
    response = {'status': 'true',
                'message': "Invoice Details Updated Successfully", 'data': invoice_update}
    return response


def delete_invoice(invoice_id: int, db: Session):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if invoice:
        db.delete(invoice)
        db.commit()
        return {'status': 'true', 'message': "Invoice deleted successfully", 'data': invoice}
    return {"status": 'false',  'message': "Invoice Plan not found"}
