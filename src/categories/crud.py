from sqlalchemy.orm import Session
from src.categories.models import Category
from src.categories.schemas import CategoryCreate

def create_category(category: CategoryCreate, db: Session):
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def read_categories(db: Session):
    return db.query(Category).all()

def read_category(category_id: int, db: Session):
    return db.query(Category).filter(Category.id == category_id).first()

def delete_category(category_id: int, db: Session):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category:
        db.delete(category)
        db.commit()
        return category
    return None
