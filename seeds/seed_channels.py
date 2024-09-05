from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.channels.models import Channel

session = SessionLocal()

def seed_channels():
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
    seed_channels()
    print("Channels seeded successfully.")

