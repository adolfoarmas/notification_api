from abc import ABC, abstractmethod
from fastapi import HTTPException
from typing import List, Tuple, Any, Generator
from src.users.models import User
from src.notifications.models import (
    UserTopic, 
    UserChannel
    )
import asyncio
import logging

class NotificationStrategy(ABC):
    log_message = {}
    user: User = None
    contact_attribute=''
    contact_attr_value=''

    def __init__(self, message: str):
        self.message = message

    @abstractmethod
    async def process_notification(self, user: User):
        pass
    
    async def handle_notification_list(self, users_notification_list: list):
        tasks = [self.process_notification(user) for _, user in users_notification_list]
        await asyncio.gather(*tasks)
        
    async def send_notification(self):
        try:
            self.log_message = {
            'user_id': self.user.id, 
            'user_name': self.user.name, 
            'contact_attr': self.contact_attribute, 
            'contact_attr_value': self.contact_attr_value, 
            'notification_message': self.message 
            }
        except Exception as e:
            raise RuntimeError(f"An error has ocurred when trying to send the notification {e} to user {self.user.id}")

class SMSNotification(NotificationStrategy):
    async def process_notification(self, user: User):
        self.user = user
        self.contact_attribute = 'phone'
        self.contact_attr_value = self.user.phone
        await self.send_notification()
        logging.info(f"SENT: SMS notification: {self.log_message} ")
    
    async def send_notification(self):
        #service connection logic here
        return await super().send_notification()

class EmailNotification(NotificationStrategy):
    async def process_notification(self, user: User):
        self.user = user
        self.contact_attribute = 'email'
        self.contact_attr_value = self.user.email
        await self.send_notification()
        logging.info(f"SENT: Email notification: {self.log_message} ")
    
    async def send_notification(self):
        #service connection logic here
        return await super().send_notification()

class PushNotification(NotificationStrategy):
    async def process_notification(self, user: User):
        self.user = user
        self.contact_attribute = 'email'
        self.contact_attr_value = self.user.email
        await self.send_notification()
        logging.info(f"SENT: Push notification: {self.log_message} ")
    
    async def send_notification(self):
        #service connection logic here
        return await super().send_notification()
    
async def select_notification_strategy(channel_id, message):
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

async def send_notification(notification, db):
    notification_category = notification.category
    selected_users_topic = (
    db.query(UserTopic, User, UserChannel.channel_id)
    .join(User, User.id == UserTopic.user_id)
    .join(UserChannel, User.id == UserChannel.user_id)
    .filter(UserTopic.topic_id == notification_category)
    .order_by(UserChannel.channel_id)
    .all()
    )

    if not selected_users_topic:
        raise HTTPException(status_code=404, detail=f"Users to notify not found, ensure the category id {notification_category} is correct")

    for key, users_notification_list in extract_channel_groups(selected_users_topic):
        notification_strategy = await select_notification_strategy(key, notification.message)
        await notification_strategy.handle_notification_list(users_notification_list)