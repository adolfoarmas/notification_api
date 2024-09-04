
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.notifications.service import send_notification as service_send_notification
from src.notifications.models import (
    Topic, 
    Channel, 
    )
from src.notifications.schemas import (
    TopicCreate, 
    ChannelCreate, 
    Topic as 
    TopicSchema, 
    NotificationBase
    )
from src.database import get_db
from typing import List
import logging

router = APIRouter()

# Routes for Topic
@router.post("/topics/", response_model=TopicCreate)
def create_topic(topic: TopicCreate, db: Session = Depends(get_db)):
    db_topic = Topic(name=topic.name)
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

@router.get("/topics/", response_model=List[TopicSchema])
def read_topics(db: Session = Depends(get_db)):
    return db.query(Topic).all()

@router.get("/topics/{topic_id}", response_model=TopicSchema)
def read_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@router.delete("/topics/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    db.delete(topic)
    db.commit()
    return None

# Routes for Channel
@router.post("/channels/", response_model=ChannelCreate)
def create_channel(channel: ChannelCreate, db: Session = Depends(get_db)):
    db_channel = Channel(type=channel.type)
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel

@router.get("/channels/", response_model=List[ChannelCreate])
def read_channels(db: Session = Depends(get_db)):
    return db.query(Channel).all()

@router.get("/channels/{channel_id}", response_model=ChannelCreate)
def read_channel(channel_id: int, db: Session = Depends(get_db)):
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")
    return channel

@router.delete("/channels/{channel_id}", response_model=ChannelCreate)
def delete_channel(channel_id: int, db: Session = Depends(get_db)):
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")
    db.delete(channel)
    db.commit()
    return channel

#Route for Notification Sending
@router.post("/send/")
async def send_notification(notification: NotificationBase, db: Session = Depends(get_db)):
    await service_send_notification(notification, db)