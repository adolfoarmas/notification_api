from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from .schemas import UserCreate, User as UserSchema
from .models import User
from src.notifications.models import UserChannel, UserTopic
from src.database import get_db
from .crud import create_user
from typing import List
import logging

router = APIRouter()

@router.post("/users/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logging.info(f"creating user {user.name}")
    try:
        with db.begin():
            db_user = User(name=user.name, email=user.email, phone=user.phone)
            db.add(db_user)
            db.flush()

            # Handle user subscriptions to topics
            if user.subscribed_topics:
                for topic_id in user.subscribed_topics:
                    db.add(UserTopic(user_id=db_user.id, topic_id=topic_id))

            # Handle user subscriptions to channels
            if user.subscribed_channels:
                for channel_id in user.subscribed_channels:
                    db.add(UserChannel(user_id=db_user.id, channel_id=channel_id))

            db.commit()

            return db_user
    except IntegrityError as e:
            logging.error(f"IntegrityError: {e}")
            raise HTTPException(status_code=400, detail="Integrity error occurred. Check your data.")
    except SQLAlchemyError as e:
        logging.error(f"SQLAlchemyError: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")

@router.get("/users/", response_model=List[UserSchema])
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/users/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=UserSchema)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.name = user.name
    db_user.email = user.email
    db_user.phone = user.phone

    # Update user subscriptions to topics
    if user.subscribed:
        db.query(UserTopic).filter(UserTopic.user_id == user_id).delete()
        for topic_id in user.subscribed:
            db.add(UserTopic(user_id=user_id, topic_id=topic_id))

    # Update user subscriptions to channels
    if user.channel:
        db.query(UserChannel).filter(UserChannel.user_id == user_id).delete()
        for channel_id in user.channel:
            db.add(UserChannel(user_id=user_id, channel_id=channel_id))

    db.commit()
    return db_user

@router.delete("/users/{user_id}", response_model=UserSchema)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Remove subscriptions
    db.query(UserTopic).filter(UserTopic.user_id == user_id).delete()
    db.query(UserChannel).filter(UserChannel.user_id == user_id).delete()

    db.delete(db_user)
    db.commit()
    return db_user
