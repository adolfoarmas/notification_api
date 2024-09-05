from pydantic import BaseModel
from typing import List, Optional

class NotificationBase(BaseModel):
    category: int
    message: str

class NotificationResponse(BaseModel):
    user_id: int
    channel: str
    status: str
    
