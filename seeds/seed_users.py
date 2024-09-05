from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.users.schemas import UserCreate
from src.users.models import User
from src.database import SessionLocal


def seed_users(session):
    users = [
        UserCreate(
            name="Alice",
            email="alice@example.com",
            phone=None,
            subscribed_categories=[1, 2],
            subscribed_channels=[1]
        ),
        UserCreate(
            name="Bob",
            email=None,
            phone="1234567890",
            subscribed_categories=[3],
            subscribed_channels=[2, 3]
        ),
        UserCreate(
            name="Charlie",
            email="charlie@example.com",
            phone=None,
            subscribed_categories=[],
            subscribed_channels=[]
        ),
        UserCreate(
            name="Clare",
            email="clare@example.com",
            phone="123456896",
            subscribed_categories=[3],
            subscribed_channels=[1]
        )
    ]

    for user_data in users:
        user = User(
            name=user_data.name,
            email=user_data.email,
            phone=user_data.phone
        )
        session.add(user)
    
    session.commit()

# Execute the seeder
if __name__ == "__main__":
    session = SessionLocal()

    seed_users(session)
    print("Users seeded successfully.")
