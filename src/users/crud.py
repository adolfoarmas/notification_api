
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.users.models import User
from src.categories.models import UserCategory
from src.channels.models import UserChannel, Channel
from .schemas import UserCreate

def create_user(user: UserCreate, db: Session):

    existing_user = db.query(User).filter(
        (User.email == user.email) | (User.phone == user.phone)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="A user with the provided email or phone already exists."
        )

    db_user = User(name=user.name, email=user.email, phone=user.phone)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Add user subscriptions
    if user.subscribed_categories:
        for category_id in user.subscribed_categories:
            db.add(UserCategory(user_id=db_user.id, category_id=category_id))
    
    if user.subscribed_channels:
        for channel_id in user.subscribed_channels:
            db.add(UserChannel(user_id=db_user.id, channel_id=channel_id))
    
    db.commit()
    return db_user

def read_users(db: Session):
    return db.query(User).all()

def read_user(user_id: int, db: Session):
    return db.query(User).filter(User.id == user_id).first()

def update_user(user_id: int, user: UserCreate, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.name = user.name
        db_user.email = user.email
        db_user.phone = user.phone

        if user.subscribed_categories:
            db.query(UserCategory).filter(UserCategory.user_id == user_id).delete()
            for category_id in user.subscribed_categories:
                db.add(UserCategory(user_id=user_id, category_id=category_id))

        if user.subscribed_categories:
            db.query(UserChannel).filter(UserChannel.user_id == user_id).delete()
            for channel_id in user.subscribed_channels:
                # Check if the channel_id exists
                if db.query(Channel).filter(Channel.id == channel_id).first() is None:
                    raise ValueError(f"Channel with ID {channel_id} does not exist")
                db.add(UserChannel(user_id=user_id, channel_id=channel_id))

        db.commit()
        return db_user
    return None

def delete_user(user_id: int, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        # Remove subscriptions
        db.query(UserCategory).filter(UserCategory.user_id == user_id).delete()
        db.query(UserChannel).filter(UserChannel.user_id == user_id).delete()
        db.delete(db_user)
        db.commit()
        return db_user
    return None
