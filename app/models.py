import enum
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, Text, UniqueConstraint, func
from sqlalchemy.orm import relationship
from app.database import Base


class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"


class SwipeDirectionEnum(str, enum.Enum):
    left = "left"
    right = "right"


class IncomeRangeEnum(str, enum.Enum):
    prefer_not_to_say = "prefer_not_to_say"
    under_50k = "0-50K"
    k50_100 = "50K-100K"
    k100_150 = "100K-150K"
    k150_200 = "150K-200K"
    over_200k = "200K+"


class EducationEnum(str, enum.Enum):
    high_school = "high_school"
    associate = "associate"
    bachelor = "bachelor"
    master = "master"
    phd = "phd"
    other = "other"


class IndustryEnum(str, enum.Enum):
    engineering = "engineering"
    education = "education"
    financial_services = "financial_services"
    healthcare = "healthcare"
    legal = "legal"
    marketing = "marketing"
    real_estate = "real_estate"
    technology = "technology"
    hospitality = "hospitality"
    government = "government"
    arts_entertainment = "arts_entertainment"
    other = "other"


class AgentStatusEnum(str, enum.Enum):
    active = "active"
    inactive = "inactive"
    pending = "pending"


class MatchmakerStatusEnum(str, enum.Enum):
    pending = "pending"
    contacted = "contacted"
    matched = "matched"
    rejected = "rejected"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    age = Column(Integer, nullable=False)
    location = Column(String(200), nullable=True)
    bio = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)  # comma-separated
    income_range = Column(Enum(IncomeRangeEnum), nullable=True)
    education = Column(Enum(EducationEnum), nullable=True)
    industry = Column(Enum(IndustryEnum), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    swipes_made = relationship(
        "Swipe", foreign_keys="[Swipe.user_id]",
        back_populates="user", cascade="all, delete-orphan",
    )
    agent = relationship("Agent", back_populates="user", uselist=False, cascade="all, delete-orphan")
    photos = relationship(
        "UserPhoto", back_populates="user",
        cascade="all, delete-orphan", order_by="UserPhoto.display_order",
    )


class UserPhoto(Base):
    __tablename__ = "user_photos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="photos")

    @property
    def url(self) -> str:
        return f"/uploads/{self.filename}"


class Swipe(Base):
    __tablename__ = "swipes"
    __table_args__ = (
        UniqueConstraint("user_id", "target_user_id", name="uq_swipe_user_target"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    target_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    direction = Column(Enum(SwipeDirectionEnum), nullable=False)
    swiped_at = Column(DateTime, server_default=func.now(), nullable=False)

    user = relationship("User", foreign_keys=[user_id], back_populates="swipes_made")
    target_user = relationship("User", foreign_keys=[target_user_id])


class Match(Base):
    __tablename__ = "matches"
    __table_args__ = (
        UniqueConstraint("user1_id", "user2_id", name="uq_match_users"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    user2_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    matched_at = Column(DateTime, server_default=func.now(), nullable=False)

    user1 = relationship("User", foreign_keys=[user1_id])
    user2 = relationship("User", foreign_keys=[user2_id])


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    name = Column(String(100), nullable=False, default="My Agent")
    status = Column(Enum(AgentStatusEnum), nullable=False, default=AgentStatusEnum.pending)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="agent")
    matchmakers = relationship("Matchmaker", back_populates="agent", cascade="all, delete-orphan")


class Matchmaker(Base):
    __tablename__ = "matchmakers"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id", ondelete="CASCADE"), nullable=False, index=True)
    target_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(Enum(MatchmakerStatusEnum), nullable=False, default=MatchmakerStatusEnum.pending)
    contact_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    agent = relationship("Agent", back_populates="matchmakers")
    target_user = relationship("User", foreign_keys=[target_user_id])
