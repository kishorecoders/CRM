from sqlalchemy.orm import Session
from src.QuotationTemplate.models import QuotationTemplateCreate,QuotationTemplate
from datetime import datetime
from src.QuotationProduct.models import QuotationProduct
from typing import Optional,List

def create_quotation_template(db: Session, template_data: QuotationTemplateCreate):
   
    if template_data.employee_id:
        created_by_type = "employee"
        admin_emp_id = template_data.employee_id
    else:
        created_by_type = "admin"
        admin_emp_id = template_data.admin_id  


    new_template = QuotationTemplate(
        admin_id=template_data.admin_id,
        employee_id=template_data.employee_id,
        template_name=template_data.template_name,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        created_by_type=created_by_type,
        admin_emp_id=admin_emp_id
    )
    db.add(new_template)
    db.commit()
    db.refresh(new_template)
    return new_template


from src.AdminAddEmployee.models import AdminAddEmployee
from src.SuperAdminUserAddNew.models import SuperAdminUserAddNew

def get_quotation_templates_by_admin(db: Session, admin_id: str, emp_id: Optional[str] = None):
    query = db.query(QuotationTemplate).filter(QuotationTemplate.admin_id == admin_id)
    
    if emp_id:
        query = query.filter(QuotationTemplate.employee_id == emp_id)
    
    templates = db.execute(query).scalars().all()

    result = []

    for template in templates:
        creator_info = {
            "name": "",
            "id": None,
            "employee_id": ""
        }

        if template.admin_emp_id:
            if template.created_by_type == 'employee':
                empd = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == int(template.admin_emp_id)).first()
                if empd:
                    creator_info = {
                        "name": empd.employe_name,
                        "id": empd.id,
                        "employee_id": empd.employee_id
                    }
            elif template.created_by_type == 'admin':
                empd = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == int(template.admin_emp_id)).first()
                if empd:
                    creator_info = {
                        "name": empd.full_name,
                        "id": empd.id,
                        "employee_id": "Admin"
                    }

        result.append({
            "id": template.id,
            "admin_id": template.admin_id,
            "employee_id": template.employee_id,
            "template_name": template.template_name, 
            "admin_emp_id": template.admin_emp_id,
            "created_by_type": template.created_by_type,
            "updated_at": template.updated_at,
            "created_at": template.created_at,
            "creator_info": creator_info or {}
        })

    return result


# def get_quotation_templates_by_admin(db: Session, admin_id: str , emp_id :str):
#     query = db.query(QuotationTemplate).filter(QuotationTemplate.admin_id == admin_id)
#     if emp_id:
#        query = db.query(QuotationTemplate).filter(QuotationTemplate.employee_id == emp_id)
    
#     templates = db.execute(query).scalars().all()

#     # Creator details
#     creator_info = {
#         "name": "",
#         "id": None,
#         "employee_id": ""
#     }
#     if templates.admin_emp_id:
#         if templates.created_by_type == 'employee':
#             empd = db.query(AdminAddEmployee).filter(AdminAddEmployee.id == int(templates.admin_emp_id)).first()
#             if empd:
#                 creator_info = {
#                     "name": empd.employe_name,
#                     "id": empd.id,
#                     "employee_id": empd.employee_id
#                 }
#         elif templates.created_by_type == 'admin':
#             empd = db.query(SuperAdminUserAddNew).filter(SuperAdminUserAddNew.id == int(templates.admin_emp_id)).first()
#             if empd:
#                 creator_info = {
#                     "name": empd.full_name,
#                     "id": empd.id,
#                     "employee_id": "Admin"
#                 }

#     return templates


def delete_quotation_templates(db: Session, template_id: str):
    templates_to_delete = db.query(QuotationTemplate).filter(
        QuotationTemplate.id == template_id,
    ).first()

    if not templates_to_delete:
        return {
            "status": "false",
            "message": "No matching templates found for deletion.",
            "data": []
        }
    is_used = db.query(QuotationProduct).filter(
        QuotationProduct.template_id == template_id
    ).first()

    if is_used:
        return {
            "status": "false",
            "message": "This template is used in QuotationProduct. You can't delete this template.",
        }

    db.delete(templates_to_delete)
    db.commit()

    return {
        "status": "true",
        "message": f"Quotation Template(s) deleted successfully.",
    }
