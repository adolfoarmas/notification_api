from pydantic import BaseModel
from typing import List, Optional

class TopicBase(BaseModel):
    name: str

class TopicCreate(TopicBase):
    pass

class Topic(TopicBase):
    id: int

    class Config:
        orm_mode = True

class ChannelBase(BaseModel):
    type: str

class ChannelCreate(ChannelBase):
    pass

class Channel(ChannelBase):
    id: int
    
    class Config:
        orm_mode = True

class UserTopicBase(BaseModel):
    topic_type: str
    topic_id: int

class UserChannelBase(BaseModel):
    channel_type: str
    channel_id: int

class UserTopic(UserTopicBase):
    user_id: int

    class Config:
        orm_mode = True

class UserChannel(UserChannelBase):
    user_id: int

    class Config:
        orm_mode = True

class NotificationBase(BaseModel):
    category: int
    message: str
    
