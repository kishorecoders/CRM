from src.NotificationsReadStatus.models import NotificationReadStatus
from .models import NotificationRead,Notification
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from fastapi import status,HTTPException
from sqlalchemy import func
from typing import List

def get_notification(notification: NotificationRead, db: Session):
    base_query = db.query(Notification).filter(Notification.admin_id == notification.admin_id)

    if notification.user_type == "admin":
        base_query = base_query.filter(Notification.created_by_type == "employee")
        identity_filter = NotificationReadStatus.admin_id == notification.user_id
    else:
        base_query = base_query.filter(Notification.created_by_type == "admin")
        identity_filter = NotificationReadStatus.employee_id == notification.user_id

    notifications = base_query.order_by(Notification.created_at.desc()).all()

    unread_counts = {}
    known_types = [
        "lead_creation", "Account", "GRNOrder", "ProjectManagerOrder_Manual", "PurchaseOrder",
        "quotation", "ProjectManagerOrder", "RFQ", "storemanagerProduct", "StoreManagerPurchase", "Vendor"
    ]

    for notif in notifications:
        # Check if this notification is already read by this user
        read_status = db.query(NotificationReadStatus).filter(
            NotificationReadStatus.notification_id == notif.id,
            identity_filter
        ).first()

        if not read_status:
            # Count as unread
            unread_counts[notif.type] = unread_counts.get(notif.type, 0) + 1

            # Mark it as read now (insert read status)
            db.add(NotificationReadStatus(
                notification_id=notif.id,
                admin_id=notification.user_id if notification.user_type == "admin" else None,
                employee_id=notification.user_id if notification.user_type == "employee" else None,
                is_read=True
            ))

    db.commit()  
    


    notification_data = [
        {
            "id": n.id,
            "type": n.type,
            "title": n.title,
            "description": n.description,
            "created_at": n.created_at.isoformat() if n.created_at else None,
            "created_by_type": n.created_by_type,
            "created_by_id": n.created_by_id,
            "admin_id": n.admin_id,
            "object_id": n.object_id,
        }
        for n in notifications
    ]


    return {
        "status": "true",
        "message": "Fetched and marked notifications as read",
        "unread_counts": {t: unread_counts.get(t, 0) for t in known_types},
        "notifications": notification_data
    }




# def get_notifications(
#     user_type: str,
#     user_id: int,
#     admin_id: int,
#     db: Session,
#     notification_type: Optional[str] = None  # Optional: if provided, only this type is marked as read
# ):
#     base_query = db.query(Notification).filter(Notification.admin_id == admin_id)

#     if user_type == "admin":
#         base_query = base_query.filter(Notification.created_by_type == "employee")
#         identity_filter = NotificationReadStatus.admin_id == user_id
#         id_kwargs = {"admin_id": user_id, "employee_id": None}
#     else:
#         base_query = base_query.filter(Notification.created_by_type == "admin")
#         identity_filter = NotificationReadStatus.employee_id == user_id
#         id_kwargs = {"employee_id": user_id, "admin_id": None}

#     if notification_type:
#         base_query = base_query.filter(Notification.type == notification_type)

#     notifications = base_query.order_by(Notification.created_at.desc()).all()

#     unread_counts = {}
#     known_types = [
#         "lead_creation", "Account", "GRNOrder", "ProjectManagerOrder_Manual", "PurchaseOrder",
#         "quotation", "ProjectManagerOrder", "RFQ", "storemanagerProduct", "StoreManagerPurchase", "Vendor"
#     ]

#     for notif in notifications:
#         # Skip if not the selected type (only for counting purposes)
#         if not notification_type and notif.type not in known_types:
#             continue

#         # Check if already marked as read
#         read_status = db.query(NotificationReadStatus).filter(
#             NotificationReadStatus.notification_id == notif.id,
#             identity_filter
#         ).first()

#         if not read_status:
#             # Count as unread
#             unread_counts[notif.type] = unread_counts.get(notif.type, 0) + 1

#             # Mark as read only if the notification matches the selected type or no filter is provided
#             if not notification_type or notif.type == notification_type:
#                 db.add(NotificationReadStatus(
#                     notification_id=notif.id,
#                     is_read=True,
#                     **id_kwargs
#                 ))

#     db.commit()

#     return {
#         "status": "true",
#         "message": f"Fetched notifications. {'Marked only ' + notification_type + ' as read' if notification_type else 'All visible types marked as read'}",
#         "unread_counts": {t: unread_counts.get(t, 0) for t in known_types},
#         "notifications": notifications
#     }

