
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.notifications.models import Channel
from src.notifications.schemas import ChannelCreate
from src.database import get_db
from typing import List

router = APIRouter()

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