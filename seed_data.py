"""
Seed the database with sample User records (unified profile table).
Run: python seed_data.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, engine, Base
from app.models import User, Agent, GenderEnum, IncomeRangeEnum, EducationEnum, IndustryEnum, AgentStatusEnum
from app.auth import hash_password

Base.metadata.create_all(bind=engine)

SEED_PASSWORD = "password123"

USERS = [
    # --- Females ---
    {
        "email": "alice.chen@example.com",
        "name": "Alice Chen",
        "gender": GenderEnum.female,
        "age": 26,
        "location": "Sydney, NSW",
        "bio": "Coffee enthusiast and weekend hiker. Love exploring Surry Hills cafes.",
        "tags": "hiking,coffee,food,travel",
        "income_range": IncomeRangeEnum.k100_150,
        "education": EducationEnum.master,
        "industry": IndustryEnum.technology,
    },
    {
        "email": "bella.nguyen@example.com",
        "name": "Bella Nguyen",
        "gender": GenderEnum.female,
        "age": 24,
        "location": "Melbourne, VIC",
        "bio": "Photographer by passion, marketer by profession. Laneway art lover.",
        "tags": "photography,music,art,coffee",
        "income_range": IncomeRangeEnum.k50_100,
        "education": EducationEnum.bachelor,
        "industry": IndustryEnum.marketing,
    },
    {
        "email": "clara.smith@example.com",
        "name": "Clara Smith",
        "gender": GenderEnum.female,
        "age": 29,
        "location": "Brisbane, QLD",
        "bio": "Software engineer who loves climbing at Kangaroo Point.",
        "tags": "climbing,gaming,tech,music",
        "income_range": IncomeRangeEnum.k150_200,
        "education": EducationEnum.bachelor,
        "industry": IndustryEnum.engineering,
    },
    {
        "email": "diana.park@example.com",
        "name": "Diana Park",
        "gender": GenderEnum.female,
        "age": 31,
        "location": "Perth, WA",
        "bio": "Yoga instructor and plant-based chef. Beach sunsets daily.",
        "tags": "yoga,cooking,wellness,travel",
        "income_range": IncomeRangeEnum.k50_100,
        "education": EducationEnum.bachelor,
        "industry": IndustryEnum.healthcare,
    },
    {
        "email": "emma.johnson@example.com",
        "name": "Emma Johnson",
        "gender": GenderEnum.female,
        "age": 23,
        "location": "Gold Coast, QLD",
        "bio": "Aspiring screenwriter. Dog mum. Lives for the beach.",
        "tags": "film,dogs,beach,art",
        "income_range": IncomeRangeEnum.under_50k,
        "education": EducationEnum.bachelor,
        "industry": IndustryEnum.arts_entertainment,
    },
    {
        "email": "fiona.li@example.com",
        "name": "Fiona Li",
        "gender": GenderEnum.female,
        "age": 27,
        "location": "Sydney, NSW",
        "bio": "Investment banker by day, salsa dancer by night. Harbour views.",
        "tags": "dancing,finance,travel,wine",
        "income_range": IncomeRangeEnum.over_200k,
        "education": EducationEnum.master,
        "industry": IndustryEnum.financial_services,
    },
    {
        "email": "grace.wang@example.com",
        "name": "Grace Wang",
        "gender": GenderEnum.female,
        "age": 32,
        "location": "Canberra, ACT",
        "bio": "Neuroscience researcher at ANU. Cat lover. Parkrun regular.",
        "tags": "science,running,cats,reading",
        "income_range": IncomeRangeEnum.k100_150,
        "education": EducationEnum.phd,
        "industry": IndustryEnum.healthcare,
    },
    {
        "email": "hannah.kim@example.com",
        "name": "Hannah Kim",
        "gender": GenderEnum.female,
        "age": 25,
        "location": "Melbourne, VIC",
        "bio": "UX designer at a startup. Obsessed with matcha and vinyl.",
        "tags": "design,music,coffee,art",
        "income_range": IncomeRangeEnum.k100_150,
        "education": EducationEnum.bachelor,
        "industry": IndustryEnum.technology,
    },
    {
        "email": "isla.martinez@example.com",
        "name": "Isla Martinez",
        "gender": GenderEnum.female,
        "age": 30,
        "location": "Adelaide, SA",
        "bio": "High school teacher and weekend pottery enthusiast.",
        "tags": "pottery,teaching,hiking,dogs",
        "income_range": IncomeRangeEnum.k50_100,
        "education": EducationEnum.master,
        "industry": IndustryEnum.education,
    },
    {
        "email": "julia.torres@example.com",
        "name": "Julia Torres",
        "gender": GenderEnum.female,
        "age": 28,
        "location": "Gold Coast, QLD",
        "bio": "Real estate agent. Beach volleyball. Foodie.",
        "tags": "real_estate,volleyball,food,beach",
        "income_range": IncomeRangeEnum.k150_200,
        "education": EducationEnum.bachelor,
        "industry": IndustryEnum.real_estate,
    },
    # --- Males ---
    {
        "email": "finn.obrien@example.com",
        "name": "Finn O'Brien",
        "gender": GenderEnum.male,
        "age": 28,
        "location": "Melbourne, VIC",
        "bio": "Architect by day, jazz musician by night. Fitzroy regular.",
        "tags": "music,architecture,jazz,coffee",
        "income_range": IncomeRangeEnum.k100_150,
        "education": EducationEnum.master,
        "industry": IndustryEnum.engineering,
    },
    {
        "email": "george.kim@example.com",
        "name": "George Kim",
        "gender": GenderEnum.male,
        "age": 25,
        "location": "Sydney, NSW",
        "bio": "Marathon runner and startup founder. Obsessed with productivity.",
        "tags": "running,tech,startups,travel",
        "income_range": IncomeRangeEnum.k150_200,
        "education": EducationEnum.bachelor,
        "industry": IndustryEnum.technology,
    },
    {
        "email": "harry.patel@example.com",
        "name": "Harry Patel",
        "gender": GenderEnum.male,
        "age": 30,
        "location": "Brisbane, QLD",
        "bio": "Medical resident at Royal Brisbane. Gym rat. Big reader.",
        "tags": "fitness,reading,cooking,hiking",
        "income_range": IncomeRangeEnum.k100_150,
        "education": EducationEnum.phd,
        "industry": IndustryEnum.healthcare,
    },
    {
        "email": "ivan.rossi@example.com",
        "name": "Ivan Rossi",
        "gender": GenderEnum.male,
        "age": 27,
        "location": "Perth, WA",
        "bio": "Italian expat. Surfer at Cottesloe. Amateur chef.",
        "tags": "surfing,cooking,beach,travel",
        "income_range": IncomeRangeEnum.k50_100,
        "education": EducationEnum.bachelor,
        "industry": IndustryEnum.hospitality,
    },
    {
        "email": "jake.turner@example.com",
        "name": "Jake Turner",
        "gender": GenderEnum.male,
        "age": 33,
        "location": "Hobart, TAS",
        "bio": "Mountain guide and wildlife photographer. MONA obsessed.",
        "tags": "hiking,photography,nature,climbing",
        "income_range": IncomeRangeEnum.k50_100,
        "education": EducationEnum.associate,
        "industry": IndustryEnum.arts_entertainment,
    },
    {
        "email": "kevin.zhao@example.com",
        "name": "Kevin Zhao",
        "gender": GenderEnum.male,
        "age": 29,
        "location": "Sydney, NSW",
        "bio": "ML engineer at Atlassian. Board game addict.",
        "tags": "tech,gaming,AI,climbing",
        "income_range": IncomeRangeEnum.over_200k,
        "education": EducationEnum.master,
        "industry": IndustryEnum.technology,
    },
    {
        "email": "leo.fernandez@example.com",
        "name": "Leo Fernandez",
        "gender": GenderEnum.male,
        "age": 35,
        "location": "Melbourne, VIC",
        "bio": "Corporate lawyer. Aspiring sommelier. Dog dad in St Kilda.",
        "tags": "wine,law,dogs,cooking",
        "income_range": IncomeRangeEnum.over_200k,
        "education": EducationEnum.phd,
        "industry": IndustryEnum.legal,
    },
    {
        "email": "marcus.brown@example.com",
        "name": "Marcus Brown",
        "gender": GenderEnum.male,
        "age": 26,
        "location": "Adelaide, SA",
        "bio": "Footy coach and BBQ legend. Big into live music at the Gov.",
        "tags": "AFL,music,BBQ,coaching",
        "income_range": IncomeRangeEnum.k50_100,
        "education": EducationEnum.bachelor,
        "industry": IndustryEnum.education,
    },
    {
        "email": "nathan.wright@example.com",
        "name": "Nathan Wright",
        "gender": GenderEnum.male,
        "age": 31,
        "location": "Darwin, NT",
        "bio": "ER nurse and amateur triathlete. Always up for adventure.",
        "tags": "triathlon,healthcare,travel,hiking",
        "income_range": IncomeRangeEnum.k100_150,
        "education": EducationEnum.bachelor,
        "industry": IndustryEnum.healthcare,
    },
    {
        "email": "oscar.reyes@example.com",
        "name": "Oscar Reyes",
        "gender": GenderEnum.male,
        "age": 24,
        "location": "Canberra, ACT",
        "bio": "Film editor and weekend DJ. Loves lakeside sunsets.",
        "tags": "film,music,DJ,food",
        "income_range": IncomeRangeEnum.under_50k,
        "education": EducationEnum.bachelor,
        "industry": IndustryEnum.arts_entertainment,
    },
]


def seed():
    db = SessionLocal()
    try:
        if db.query(User).count() > 0:
            print("Database already seeded. Skipping.")
            return

        hashed_pw = hash_password(SEED_PASSWORD)
        for data in USERS:
            user = User(password_hash=hashed_pw, **data)
            db.add(user)
            db.flush()  # get user.id
            db.add(Agent(
                user_id=user.id,
                name=f"{data['name']}'s Agent",
                status=AgentStatusEnum.pending,
            ))

        db.commit()
        print(f"Seeded {len(USERS)} users with agents. Password for all: '{SEED_PASSWORD}'")
    except Exception as e:
        db.rollback()
        print(f"Seeding failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
