from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from src.database import Base

class Topic(Base):
    __tablename__ = 'topics'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    #relationships
    users = relationship("UserTopic", back_populates="topic")

class Channel(Base):
    __tablename__ = 'channels'
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)

    #relationships
    users = relationship("UserChannel", back_populates="channel")

class UserTopic(Base):
    __tablename__ = 'user_topics'

    #relationships
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    topic_id = Column(Integer, ForeignKey('topics.id'), primary_key=True)
    user = relationship("User", back_populates="subscribed_topics")
    topic = relationship("Topic", back_populates="users")

class UserChannel(Base):
    __tablename__ = 'user_channels'

    #relationships
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    channel_id = Column(Integer, ForeignKey('channels.id'), primary_key=True)
    user = relationship("User", back_populates="subscribed_channels")
    channel = relationship("Channel", back_populates="users")