# src/seeds/seed_categories.py

from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.categories.models import Category

def seed_categories(session: Session):
    categories = [
        {"name": "Sports"},
        {"name": "Finance"},
        {"name": "Films"},
    ]

    for category_data in categories:
        category = Category(**category_data)
        session.add(category)
    
    session.commit()

if __name__ == "__main__":
    session = SessionLocal()
    try:
        seed_categories(session)
        print("Categories seeded successfully.")
    finally:
        session.close()
