
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.notifications.service import send_notification as service_send_notification
from src.notifications.schemas import NotificationBase, NotificationResponse
from src.database import get_db
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/send/", response_model=List[NotificationResponse])
async def send_notification(notification: NotificationBase, db: Session = Depends(get_db)):
    logger.info(f"Notification request for message '{notification.message}' received...")
    return await service_send_notification(notification, db)