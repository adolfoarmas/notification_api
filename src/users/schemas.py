from pydantic import BaseModel, validator, root_validator, EmailStr
from typing import List, Optional
from src.categories.models import UserCategory
from src.channels.models import UserChannel

class UserBase(BaseModel):
    name: str | None
    email: str | None
    phone: str | None

class UserCreate(UserBase):
    email: Optional[EmailStr]
    subscribed_categories: Optional[List[int]] = []
    subscribed_channels: Optional[List[int]] = []

    @root_validator(pre=True)
    def ensure_one_of_email_or_phone(cls, values):
        email = values.get('email')
        phone = values.get('phone')
        if not email and not phone:
            raise ValueError('At least one of email or phone must be provided')
        return values
    
    @validator('email', 'phone', pre=True, always=True)
    def check_empty_values(cls, value):
        if value == "":
            return None
        return value
class User(UserBase):
    id: int
    subscribed_categories: List[int] = []
    subscribed_channels: List[int] = []

    class Config:
        orm_mode = True

    @validator('subscribed_categories', pre=True, each_item=True)
    def convert_categories_to_ids(cls, v):
        return v.category_id if isinstance(v, UserCategory) else v
    
    @validator('subscribed_channels', pre=True, each_item=True)
    def convert_channels_to_ids(cls, v):
        return v.channel_id if isinstance(v, UserChannel) else v