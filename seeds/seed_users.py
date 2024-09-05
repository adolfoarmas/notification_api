from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.users.schemas import UserCreate
from src.users.models import User, UserCategory, UserChannel
from src.database import SessionLocal

session = SessionLocal()

def seed_users():
    try:
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
                subscribed_categories=[3],
                subscribed_channels=[2]
            ),
            UserCreate(
                name="Clare",
                email="clare@example.com",
                phone="123456896",
                subscribed_categories=[3],
                subscribed_channels=[1]
            ),
            # New users
            UserCreate(
                name="David",
                email="david@example.com",
                phone="9876543210",
                subscribed_categories=[1],
                subscribed_channels=[2, 3]
            ),
            UserCreate(
                name="Eve",
                email="eve@example.com",
                phone=None,
                subscribed_categories=[2],
                subscribed_channels=[1]
            ),
            UserCreate(
                name="Frank",
                email=None,
                phone="6543210987",
                subscribed_categories=[1, 3],
                subscribed_channels=[1, 2]
            ),
            UserCreate(
                name="Grace",
                email="grace@example.com",
                phone="3216549870",
                subscribed_categories=[2, 3],
                subscribed_channels=[2]
            ),
            UserCreate(
                name="Hank",
                email="hank@example.com",
                phone=None,
                subscribed_categories=[1],
                subscribed_channels=[3]
            ),
            UserCreate(
                name="Ivy",
                email=None,
                phone="0123456789",
                subscribed_categories=[2],
                subscribed_channels=[1, 3]
            ),
            UserCreate(
                name="Jack",
                email="jack@example.com",
                phone="9870123456",
                subscribed_categories=[3],
                subscribed_channels=[1, 2]
            ),
            UserCreate(
                name="Kara",
                email="kara@example.com",
                phone=None,
                subscribed_categories=[1, 2],
                subscribed_channels=[3]
            ),
            UserCreate(
                name="Leo",
                email="leo@example.com",
                phone="3456789012",
                subscribed_categories=[2, 3],
                subscribed_channels=[2]
            ),
            UserCreate(
                name="Mia",
                email="mia@example.com",
                phone=None,
                subscribed_categories=[1, 3],
                subscribed_channels=[1]
            ),
            UserCreate(
                name="Nina",
                email="nina@example.com",
                phone="2109876543",
                subscribed_categories=[2],
                subscribed_channels=[2, 3]
            )
        ]

        for user_data in users:
            user = User(
                name=user_data.name,
                email=user_data.email,
                phone=user_data.phone,
            )
            session.add(user)
            session.commit()
            session.refresh(user)

            if user_data.subscribed_categories:
                for category_id in user_data.subscribed_categories:
                    session.add(UserCategory(user_id=user.id, category_id=category_id))

            if user_data.subscribed_channels:
                for channel_id in user_data.subscribed_channels:
                    session.add(UserChannel(user_id=user.id, channel_id=channel_id))
            
            session.commit()
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")

    finally:
        session.close()

if __name__ == "__main__":
    seed_users()
    print("Users seeded successfully.")
