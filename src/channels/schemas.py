from pydantic import BaseModel

class ChannelBase(BaseModel):
    type: str

class ChannelCreate(ChannelBase):
    pass

class Channel(ChannelBase):
    id: int
    
    class Config:
        orm_mode = True

class UserChannelBase(BaseModel):
    channel_type: str
    channel_id: int

class UserChannel(UserChannelBase):
    user_id: int

    class Config:
        orm_mode = True
    
