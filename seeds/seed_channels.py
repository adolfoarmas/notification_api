# src/seeds/seed_channels.py

from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.channels.models import Channel

def seed_channels(session: Session):
    channels = [
        {"type": "SMS"},
        {"type": "Email"},
        {"type": "Push Notification"}
    ]

    for channel_data in channels:
        channel = Channel(**channel_data)
        session.add(channel)
    
    session.commit()

if __name__ == "__main__":
    session = SessionLocal()
    try:
        seed_channels(session)
        print("Channels seeded successfully.")
    finally:
        session.close()
