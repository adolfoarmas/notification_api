
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.categories.models import Category

session = SessionLocal()

def seed_categories():
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
    seed_categories()
    print("Categories seeded successfully.")

