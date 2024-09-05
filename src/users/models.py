from sqlalchemy import Column, Integer, String, Index, text
from sqlalchemy.orm import relationship
from src.database import Base
from src.categories.models import UserCategory
from src.channels.models import UserChannel

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, unique=True, index=True, nullable=True)
    #relationships
    subscribed_categories = relationship('UserCategory', back_populates="user")
    subscribed_channels = relationship('UserChannel', back_populates="user")

    __table_args__ = (
        Index('ix_users_email_non_empty', 'email', unique=True, postgresql_where=text('email <> \'\'')),
        Index('ix_users_phone_non_empty', 'phone', unique=True, postgresql_where=text('phone <> \'\''))
    )