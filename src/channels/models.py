from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from src.database import Base

class Channel(Base):
    __tablename__ = 'channels'
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)

    #relationships
    users = relationship("UserChannel", back_populates="channel")

class UserChannel(Base):
    __tablename__ = 'user_channels'

    #relationships
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    channel_id = Column(Integer, ForeignKey('channels.id'), primary_key=True)
    user = relationship("User", back_populates="subscribed_channels")
    channel = relationship("Channel", back_populates="users")