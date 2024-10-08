from abc import ABC, abstractmethod
from fastapi import HTTPException
from typing import List, Tuple, Any, Generator
from src.users.models import User
from src.categories.schemas import UserCategory as UserCategorySchema
from src.categories.models import UserCategory
from src.channels.models import UserChannel
from src.celery import celery_app
from src.tasks import send_sms_task, send_email_task, send_push_task
import asyncio
import logging

logger = logging.getLogger(__name__)

class NotificationStrategy(ABC):
    message_dict = {}
    user: User = None
    contact_attribute=''
    contact_attr_value=''

    def __init__(self, message: str):
        self.message = message

    @abstractmethod
    async def process_notification(self, user: User):
        pass
    
    @abstractmethod
    def send_notification_to_channel_service(self) -> bool:
        pass

    async def set_message_dict(self) -> None:
        self.message_dict = {
            'user_id': self.user.id, 
            'user_name': self.user.name, 
            'contact_attr': self.contact_attribute, 
            'contact_attr_value': self.contact_attr_value, 
            'notification_message': self.message 
        }
    async def get_message_dict(self) -> dict:
        return self.message_dict
                
    async def get_status_object(self, channel, status) -> dict:
        return {
            'user_id': self.user.id, 
            'channel': channel,
            'status': status
        }   
    
    async def handle_notification_list(self, users_notification_list: list) -> List[dict]:
        tasks = [self.process_notification(user) for _, user in users_notification_list]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def validate_contact_attribute(self) -> None:
        if self.contact_attr_value:
            return
        raise ValueError(f"{self.contact_attribute} = '{self.contact_attr_value}' for user {self.user.id}")

class SMSNotification(NotificationStrategy):
    
    def send_notification_to_channel_service(self) -> bool:
        return send_sms_task.delay(self.message_dict)

    async def process_notification(self, user: User):
        self.user = user
        self.contact_attr_value = self.user.phone
        self.contact_attribute = "phone"
    
        try:
            await self.set_message_dict()
            await self.validate_contact_attribute()
            message_dict = await self.get_message_dict()
            success = self.send_notification_to_channel_service()
            logger.info(f"SENT: Email notification: {message_dict}")
            return await self.get_status_object("Email", "ok") if success else await self.get_status_object("Email", "failed")

        except ValueError as e:
            logger.error(f"FAIL: SMS notification: {e}")
        except Exception as e:
            logger.error(f"An error has ocurred when trying to send the SMS notification to user {self.user.id}")
        
        return await self.get_status_object("SMS", "failed")        
        
class EmailNotification(NotificationStrategy):

    def send_notification_to_channel_service(self) -> bool:
        return send_email_task.delay(self.message_dict)
    
    async def process_notification(self, user: User):
        self.user = user
        self.contact_attribute = 'email'
        self.contact_attr_value = self.user.email
        try:
            await self.set_message_dict()
            await self.validate_contact_attribute()
            message_dict = await self.get_message_dict()
            success = self.send_notification_to_channel_service()
            logger.info(f"Email: Push notification: {message_dict}")
            return await self.get_status_object("Email", "ok") if success else await self.get_status_object("Email", "failed")
        except ValueError as e:
            logger.error(f"FAIL: Email notification: {e}")
        except Exception as e:
            logger.error(f"An error has ocurred when trying to send the Email notification to user {self.user.id}")
        
        return await self.get_status_object("Email", "failed")  
    
    

class PushNotification(NotificationStrategy):

    def send_notification_to_channel_service(self) -> bool:
        return send_push_task.delay(self.message_dict)

    async def process_notification(self, user: User):
        self.user = user
        self.contact_attribute = 'email'
        self.contact_attr_value = self.user.email
        try:
            await self.set_message_dict()
            await self.validate_contact_attribute()
            message_dict = await self.get_message_dict()
            success = self.send_notification_to_channel_service()
            logger.info(f"SENT: Push notification: {message_dict}")
            return await self.get_status_object("Push", "ok") if success else await self.get_status_object("Push", "failed")
        
        except ValueError as e:
            logger.error(f"FAIL: Push notification: {e}")
        except Exception as e:
            print("Error: ", e)
            logger.error(f"An error has ocurred when trying to send the Email notification to user {self.user.id}")
        
        return await self.get_status_object("Push", "failed") 
    
    
    
async def select_notification_strategy(channel_id, message) -> NotificationStrategy:
    if channel_id == 1:
        return SMSNotification(message)
    elif channel_id == 2:
        return EmailNotification(message)
    elif channel_id == 3:
        return PushNotification(message)
    else:
        raise ValueError(f"Channel id {channel_id} is not registered.")

def extract_channel_groups(users_and_channels: List[Tuple[Any, Any, int]]) -> Generator[Tuple[int, List[Tuple[Any, Any]]], None, None]:

    if not users_and_channels:
        return
    
    current_group = []
    current_last_element = users_and_channels[0][2]

    for item in users_and_channels:
        if item[2] == current_last_element:
            current_group.append(item[:-1])
        else:
            yield (current_last_element, current_group)
            current_group = [item[:-1]]
            current_last_element = item[2]
    
    if current_group:
        yield (current_last_element, current_group)

async def send_notification(notification, db) -> list[dict]:
    notification_category = notification.category
    selected_users_channel = (
    db.query(UserCategory, User, UserChannel.channel_id)
    .join(User, User.id == UserCategory.user_id)
    .join(UserChannel, User.id == UserChannel.user_id)
    .filter(UserCategory.category_id == notification_category)
    .order_by(UserChannel.channel_id)
    .all()
    )

    if not selected_users_channel:
        raise HTTPException(status_code=404, detail=f"Users to notify not found, ensure the category id {notification_category} is correct")
    
    results = []

    for channel, users_notification_list in extract_channel_groups(selected_users_channel):
        notification_strategy = await select_notification_strategy(channel, notification.message)
        returns = await notification_strategy.handle_notification_list(users_notification_list)
        results.extend(returns)
    return results