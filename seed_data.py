"""
Seed the database with sample Candidate records.
Run: python seed_data.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, engine, Base
from app.models import Candidate, GenderEnum

Base.metadata.create_all(bind=engine)

CANDIDATES = [
    {
        "name": "Alice Chen",
        "gender": GenderEnum.female,
        "age": 26,
        "location": "San Francisco, CA",
        "bio": "Coffee enthusiast and weekend hiker. Love exploring new restaurants.",
        "tags": "hiking,coffee,food,travel",
        "photo_url": "https://randomuser.me/api/portraits/women/1.jpg",
    },
    {
        "name": "Bella Nguyen",
        "gender": GenderEnum.female,
        "age": 24,
        "location": "New York, NY",
        "bio": "Photographer by passion, marketer by profession.",
        "tags": "photography,music,art,coffee",
        "photo_url": "https://randomuser.me/api/portraits/women/2.jpg",
    },
    {
        "name": "Clara Smith",
        "gender": GenderEnum.female,
        "age": 29,
        "location": "Austin, TX",
        "bio": "Software engineer who loves climbing and board games.",
        "tags": "climbing,gaming,tech,music",
        "photo_url": "https://randomuser.me/api/portraits/women/3.jpg",
    },
    {
        "name": "Diana Park",
        "gender": GenderEnum.female,
        "age": 31,
        "location": "Seattle, WA",
        "bio": "Yoga instructor and plant-based chef. ENFP.",
        "tags": "yoga,cooking,wellness,travel",
        "photo_url": "https://randomuser.me/api/portraits/women/4.jpg",
    },
    {
        "name": "Emma Johnson",
        "gender": GenderEnum.female,
        "age": 23,
        "location": "Los Angeles, CA",
        "bio": "Aspiring screenwriter. Dog mom. Loves beaches.",
        "tags": "film,dogs,beach,art",
        "photo_url": "https://randomuser.me/api/portraits/women/5.jpg",
    },
    {
        "name": "Finn O'Brien",
        "gender": GenderEnum.male,
        "age": 28,
        "location": "Chicago, IL",
        "bio": "Architect by day, jazz musician by night.",
        "tags": "music,architecture,jazz,coffee",
        "photo_url": "https://randomuser.me/api/portraits/men/1.jpg",
    },
    {
        "name": "George Kim",
        "gender": GenderEnum.male,
        "age": 25,
        "location": "San Jose, CA",
        "bio": "Marathon runner and startup founder. Obsessed with productivity.",
        "tags": "running,tech,startups,travel",
        "photo_url": "https://randomuser.me/api/portraits/men/2.jpg",
    },
    {
        "name": "Harry Patel",
        "gender": GenderEnum.male,
        "age": 30,
        "location": "Boston, MA",
        "bio": "Medical resident. Gym rat. Big reader.",
        "tags": "fitness,reading,cooking,hiking",
        "photo_url": "https://randomuser.me/api/portraits/men/3.jpg",
    },
    {
        "name": "Ivan Rossi",
        "gender": GenderEnum.male,
        "age": 27,
        "location": "Miami, FL",
        "bio": "Italian expat. Surfer. Amateur chef.",
        "tags": "surfing,cooking,beach,travel",
        "photo_url": "https://randomuser.me/api/portraits/men/4.jpg",
    },
    {
        "name": "Jake Turner",
        "gender": GenderEnum.male,
        "age": 33,
        "location": "Denver, CO",
        "bio": "Mountain guide and wildlife photographer.",
        "tags": "hiking,photography,nature,climbing",
        "photo_url": "https://randomuser.me/api/portraits/men/5.jpg",
    },
]


def seed():
    db = SessionLocal()
    try:
        if db.query(Candidate).count() > 0:
            print("Database already seeded. Skipping.")
            return

        for data in CANDIDATES:
            candidate = Candidate(**data)
            db.add(candidate)

        db.commit()
        print(f"Seeded {len(CANDIDATES)} candidates successfully.")
    except Exception as e:
        db.rollback()
        print(f"Seeding failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
