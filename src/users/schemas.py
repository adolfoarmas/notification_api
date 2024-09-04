from pydantic import BaseModel, validator
from typing import List, Optional
from src.notifications.schemas import UserTopicBase, UserChannelBase
from src.notifications.models import UserTopic, UserChannel

class UserBase(BaseModel):
    name: str
    email: str
    phone: str

class UserCreate(UserBase):
    subscribed_topics: Optional[List[int]] = []
    subscribed_channels: Optional[List[int]] = []   

class User(UserBase):
    id: int
    subscribed_topics: List[int] = []
    subscribed_channels: List[int] = []

    class Config:
        orm_mode = True

    @validator('subscribed_topics', pre=True, each_item=True)
    def convert_topics_to_ids(cls, v):
        return v.topic_id if isinstance(v, UserTopic) else v
    
    @validator('subscribed_channels', pre=True, each_item=True)
    def convert_channels_to_ids(cls, v):
        return v.channel_id if isinstance(v, UserChannel) else v