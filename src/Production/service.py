import json
from sqlalchemy.orm import Session
from typing import Dict, List
from sqlalchemy import desc
from src.Production.models import ProductionCreate,Production,ProductionStatusUpdate
from typing import Optional, List
from datetime import datetime
from src.AdminAddEmployee.models import AdminAddEmployee
from src.ProductionRequest.models import ProductionRequest
from src.ProductStages.models import ProductStages
from src.ProjectManagerOrder.models import ProjectManagerOrder

from src.StoreCheckPoint.models import StoreCheckPoint
from src.StoreSubProductEmployee.models import StoreSubProductEmployee
from src.StoreTemplates.models import StoreTemplate
from src.StoreProductTemplates_key.models import StoreProductTemplateKey





def create_multiple_products(db: Session, products: List[ProductionCreate]) -> Dict:
    db_products = []

    for product_data in products:
        db_product = Production(
            admin_id=product_data.admin_id,
            from_employee=product_data.from_employee,
            stage_name=product_data.stage_name,
            assign_employee=product_data.assign_employee,
            ideal_time=product_data.ideal_time,
            custom_time=product_data.custom_time,
            deadline=product_data.deadline,
            priority=product_data.priority,
            type=product_data.type,
            quote_id=product_data.quote_id,
            lead_id=product_data.lead_id,
            product_name=product_data.product_name,
            product_code=product_data.product_code,
            hsn_code=product_data.hsn_code,
            rate_per_unit=product_data.rate_per_unit,
            quantity=product_data.quantity,
            total=product_data.total,
            gst_percentage=product_data.gst_percentage,
            gross_total=product_data.gross_total,
            availability=product_data.availability,
            purchase_request_id=product_data.purchase_request_id,
            categories=product_data.categories,
            sub_categories=product_data.sub_categories,
            gst_rate=product_data.gst_rate,
            discription=product_data.discription,
            price_per_product=product_data.price_per_product,
            unit=product_data.unit,
            sold_as=product_data.sold_as,
            pack_of=product_data.pack_of,
            steps=product_data.steps,
            time_riquired_for_this_process=product_data.time_riquired_for_this_process,
            day=product_data.day,
            minimum_requuired_quantity_for_low_stock=product_data.minimum_requuired_quantity_for_low_stock,
            document=product_data.document,
            opening_stock=product_data.opening_stock,
            internal_manufacturing=product_data.internal_manufacturing,
            status=product_data.status,
            comment_mark=product_data.comment_mark,
            order_id=product_data.order_id,
            stage_id=product_data.stage_id,
            from_status=product_data.from_status,
            quotation_id=product_data.quotation_id,
            
            production_engeneer=product_data.production_engeneer,
            doc_no=product_data.doc_no,
            doc_date=product_data.doc_date,
            rec_date=product_data.rec_date,
            exp_date=product_data.exp_date,
            product_similar_stages=product_data.product_similar_stages,
            subproduct_list_ids=product_data.subproduct_list_ids,

        )
        db.add(db_product)
        db.flush()
        db_products.append(db_product)

        if product_data.product_sub_products:
            for subproduct in product_data.product_sub_products:
                for sp_item in subproduct.sub_products:
                    subproduct_instance = StoreSubProductEmployee(
                        admin_id=subproduct.admin_id,
                        emp_id=subproduct.emp_id,
                        product_id=subproduct.product_id,
                        add_remark=sp_item.add_remark,
                        sub_product_name=sp_item.sub_product_name,
                        quantity=str(sp_item.quantity),
                        production_id=db_product.id,
                        parent_subproduct_id=sp_item.parent_subproduct_id


                    )
                    db.add(subproduct_instance)
                    db.flush()

                    if sp_item.checkpoints:
                        for cp_item in sp_item.checkpoints:
                            checkpoint_instance = StoreCheckPoint(
                                admin_id=subproduct.admin_id,
                                emp_id=subproduct.emp_id,
                                subproduct_id=subproduct_instance.id,
                                stage_id=product_data.stage_id,
                                check_point_name=cp_item.check_point_name,
                                check_point_status=cp_item.check_point_status,
                                production_id=db_product.id

                            )
                            db.add(checkpoint_instance)



        if product_data.product_templates:
            for template_group in product_data.product_templates:
                for template in template_group.templates:
                    db_template = StoreTemplate(
                        admin_id=template_group.admin_id,
                        emp_id=template_group.emp_id,
                        product_id=template_group.product_id,
                        template_name=template.template_name,
                        production_id=db_product.id
                    )
                    db.add(db_template)
                    db.flush()

                    if template.template_key_value:
                        for kv in template.template_key_value:
                            db_kv = StoreProductTemplateKey(
                                admin_id=template_group.admin_id,
                                emp_id=template_group.emp_id,
                                template_id=db_template.id,
                                temp_key_name=kv.temp_key_name,
                                temp_value=kv.temp_value,
                                production_id=db_product.id
                            )
                            db.add(db_kv)

    db.commit()

    for product in db_products:
        db.refresh(product)

    return {
        'status': 'true',
        'message': f"{len(db_products)} Production Products Added Successfully",
        'data': db_products
    }



        
from src.Quotation.models import Quotation
from src.cre_upd_name import get_creator_updator_info,get_creator_info
from src.QuotationProductEmployee.models import QuotationProductEmployee

def fetch_products_by_admin(db: Session, admin_id: int, employee_id: Optional[str], stage_id: Optional[str]) -> dict:
    try:
        query = db.query(Production).filter(Production.admin_id == admin_id)

        if employee_id:
            query = query.filter(Production.assign_employee == employee_id)

        if stage_id:
            query = query.filter(Production.stage_id == stage_id)

        db_products = query.order_by(desc(Production.id)).all()

        if not db_products:
            return {
                "status": "false",
                "message": "Products not found for the provided admin_id and employee_id",
            }

        result_data = []

        for product in db_products:
            employee = db.query(AdminAddEmployee).filter(
                AdminAddEmployee.id == product.from_employee
            ).first()

            sale_order_id = None
            if product.quotation_id:
                quotation = db.query(Quotation).filter(
                    Quotation.id == product.quotation_id
                ).first()
                sale_order_id = quotation.pi_number if quotation else None


            order_record = db.query(ProjectManagerOrder.order_id).filter(
                ProjectManagerOrder.id == product.order_id
            ).first()

            stage = db.query(ProductStages).filter(ProductStages.id == product.stage_id).first() if product.stage_id else None

            product_quantity = None
            if stage:
                product_q = db.query(QuotationProductEmployee).filter(QuotationProductEmployee.id == int(stage.product_id)).first()
                product_quantity = product_q.quantity

            if product.product_similar_stages:
                product_similar_stages_temp = db.query(ProductStages).filter(
                    ProductStages.id.in_(list(map(int, product.product_similar_stages)))
                ).all()
                product_similar_stages = []
                parent_stage = None
                
                for similar_stage in product_similar_stages_temp:
                    production_status = ""
                    production_engeneer_status = ""
                    production_engeneer = ""
                    if similar_stage:
                        production_products = db.query(Production).filter(Production.stage_id == str(similar_stage.id)).first()
                        if production_products:
                            production_status = production_products.status if production_products.status else ""
                            production_engeneer_status = production_products.production_engeneer_status if production_products.production_engeneer_status else ""
                            production_engeneer = production_products.production_engeneer if production_products.production_engeneer else ""

                        parent_stage = db.query(ProductStages).filter(ProductStages.id == similar_stage.parent_stage_id).first()
                    if similar_stage.assign_employee:
                        created_updated = get_creator_info(admin_emp_id=similar_stage.assign_employee, created_by_type="employee", db=db)

                    sub_product_list = []
                    sub_pro = db.query(Production).filter(Production.stage_id == str(similar_stage.id)).first()

                    if sub_pro:
                        sub_products = db.query(StoreSubProductEmployee).filter(
                            StoreSubProductEmployee.production_id == str(sub_pro.id)
                        ).all()
                        sub_product_list.extend(sub_products) 
                        
                    product_similar_stages.append(
                        {**similar_stage.__dict__,
                         "parent_stage": parent_stage.__dict__ if parent_stage else {},
                         "assign_employee_details": created_updated if created_updated else {},
                         "production_status": production_status if production_status else "",
                         "production_engeneer_status": production_engeneer_status if production_engeneer_status else "",
                         "production_engeneer": production_engeneer if production_engeneer else "",
                         "subproduct_list": sub_product_list if sub_product_list else [],
                         }
                    )
            else:
                product_similar_stages = []

            order_code = order_record.order_id if order_record else None

            product_data = product.dict()
            if isinstance(product.subproduct_list_ids, str):
                try:
                    product_data["subproduct_list_ids"] = json.loads(product.subproduct_list_ids)
                except json.JSONDecodeError:
                    product_data["subproduct_list_ids"] = []
            elif isinstance(product.subproduct_list_ids, list):
                product_data["subproduct_list_ids"] = product.subproduct_list_ids
            else:
                product_data["subproduct_list_ids"] = []
            product_data["sale_order_id"] = sale_order_id if sale_order_id else None
            product_data["employee_details"] = employee.dict() if employee else None
            product_data["order_code"] = order_code
            
            stage_data = stage.dict()
            data = db.query(ProductStages).filter(ProductStages.id == int(stage.parent_stage_id)).first()
            stage_data["serial_number"] = data.serial_number


            product_data["stage_details"] = stage_data if stage else None
            product_data["product_quantity"] = product_quantity if stage else None
            
            #product_data["stage_details"] = stage.dict() if stage else None
            product_data["product_similar_stages"] = product_similar_stages if product.product_similar_stages else []
            # Handle stage_id to fetch parent_stage if exists
            try:
                stage_id_int = int(product.stage_id) if product.stage_id is not None else None
            except ValueError:
                stage_id_int = None

            if stage_id_int:
                child_stage = db.query(ProductStages).filter(ProductStages.id == stage_id_int).first()
                if child_stage and child_stage.parent_stage_id is not None:
                    stage = db.query(ProductStages).filter(ProductStages.id == int(child_stage.parent_stage_id)).first()
                    if stage:
                        product_data["selected_product_ids"] = [] if not stage.selected_product_ids else list(map(int, stage.selected_product_ids.split(",")))
                    else:
                        product_data["selected_product_ids"] = []
                else:
                    product_data["selected_product_ids"] = []
            else:
                product_data["selected_product_ids"] = []

            # Sub-products
            sub_products = db.query(StoreSubProductEmployee).filter(
                StoreSubProductEmployee.admin_id == admin_id,
                StoreSubProductEmployee.production_id == str(product.id)
            )

            subproduct_list = []
            for sub in sub_products.all():
                sub_dict = sub.__dict__

                checkpoints = db.query(StoreCheckPoint).filter(
                    StoreCheckPoint.admin_id == admin_id,
                    StoreCheckPoint.subproduct_id == sub.id
                ).all()
                checkpoint_list = []
                for ck in checkpoints:
                    created_updated_data = get_creator_updator_info(
                        admin_emp_id=ck.admin_emp_id,
                        created_by_type=ck.created_by_type,
                        updated_admin_emp_id=ck.updated_admin_emp_id,
                        updated_by_type=ck.updated_by_type,
                        db=db
                    )
                    # You can include both checkpoint info and creator/updator info
                    checkpoint_list.append({**ck.__dict__,**created_updated_data})

                sub_dict["checkpoints"] = checkpoint_list
                
                subproduct_list.append(sub_dict)

            product_data["sub_products"] = subproduct_list

            # Templates
            templates = db.query(StoreTemplate).filter(
                StoreTemplate.admin_id == admin_id,
                StoreTemplate.production_id == str(product.id)
            )

            template_list = []
            for temp in templates.all():
                temp_dict = temp.__dict__

                keys = db.query(StoreProductTemplateKey).filter(
                    StoreProductTemplateKey.admin_id == admin_id,
                    StoreProductTemplateKey.template_id == temp.id
                )
                temp_dict["template_keys"] = [key.__dict__ for key in keys.all()]
                template_list.append(temp_dict)

            product_data["templates"] = template_list

            result_data.append(product_data)

        return {
            "status": "true",
            "message": "Products retrieved successfully with details",
            "data": result_data,
        }

    except Exception as e:
        return {
            "status": "false",
            "message": f"An error occurred: {str(e)}",
        }


def update_production_status(db: Session, status_update: ProductionStatusUpdate):
    # Find the production record
    production = db.query(Production).filter(
        Production.admin_id == status_update.admin_id,
        Production.id == status_update.production_id
    ).first()

    if not production:
        return {
            "status": "false",
            "message": "Production record not found for the provided admin_id and production_id."
        }

    # Check if the assigned employee matches
    if status_update.employee_id and production.assign_employee != status_update.employee_id:
        return {
            "status": "false",
            "message": "Employee ID does not match the assigned employee for this production."
        }

    # Ensure all related ProductionRequests are completed before marking Production as 'Completed'
    if status_update.status == "Completed":
        related_request = db.query(ProductionRequest).filter(
            ProductionRequest.production_id == production.id,
            ProductionRequest.admin_id == production.admin_id,
            ProductionRequest.status != "Completed" 
        ).first()

        if related_request:
            return {
                "status": "false",
                "message": "Production cannot be marked as 'Completed' until all related production requests are completed."
            }
        # Find the related ProductStages record
        product_stage = db.query(ProductStages).filter(
            ProductStages.id == production.stage_id
        ).first()

        if product_stage:
            product_stage.status = "Completed"
            product_stage.updated_at = datetime.utcnow()
            db.add(product_stage)

    # Update Production status and comment mark
    if status_update.status:
        production.status = status_update.status

    if status_update.comment_mark:
        production.comment_mark = status_update.comment_mark

    # Update timestamps
    production.updated_at = datetime.utcnow()

    db.add(production)
    db.commit()
    db.refresh(production)

    return {
        "status": "true",
        "message": "Production record updated successfully.",
        "data": {
            "production_id": production.id,
            "status": production.status,
            "comment_mark": production.comment_mark,
            "updated_at": production.updated_at
        }
    }
