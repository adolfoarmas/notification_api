from sqlalchemy.orm import Session
from src.channels.models import Channel
from src.channels.schemas import ChannelCreate

def create_channel(channel: ChannelCreate, db: Session):
    db_channel = Channel(type=channel.type)
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel

def read_channels(db: Session):
    return db.query(Channel).all()

def read_channel(channel_id: int, db: Session):
    return db.query(Channel).filter(Channel.id == channel_id).first()

def delete_channel(channel_id: int, db: Session):
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if channel:
        db.delete(channel)
        db.commit()
        return channel
    return None
