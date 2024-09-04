from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base
from src.notifications.models import UserTopic, UserChannel

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, unique=True, index=True, nullable=True)
    #relationships
    subscribed_topics = relationship('UserTopic', back_populates="user")
    subscribed_channels = relationship('UserChannel', back_populates="user")