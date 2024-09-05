# src/channels/routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .schemas import ChannelCreate
from .crud import create_channel as crud_create_channel, read_channels as crud_read_channels, read_channel as crud_read_channel, delete_channel as crud_delete_channel
from src.database import get_db

router = APIRouter()

@router.post("/channels/", response_model=ChannelCreate)
def create_channel(channel: ChannelCreate, db: Session = Depends(get_db)):
    return crud_create_channel(channel, db)

@router.get("/channels/", response_model=List[ChannelCreate])
def read_channels(db: Session = Depends(get_db)):
    return crud_read_channels(db)

@router.get("/channels/{channel_id}", response_model=ChannelCreate)
def read_channel(channel_id: int, db: Session = Depends(get_db)):
    channel = crud_read_channel(channel_id, db)
    if channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")
    return channel

@router.delete("/channels/{channel_id}", response_model=ChannelCreate)
def delete_channel(channel_id: int, db: Session = Depends(get_db)):
    deleted_channel = crud_delete_channel(channel_id, db)
    if deleted_channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")
    return deleted_channel
