from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from src.database import Base

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    #relationships
    users = relationship("UserCategory", back_populates="category")

class UserCategory(Base):
    __tablename__ = 'user_categories'

    #relationships
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)
    user = relationship("User", back_populates="subscribed_categories")
    category = relationship("Category", back_populates="users")