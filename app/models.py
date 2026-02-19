import enum
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from app.database import Base


class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"


class SwipeDirectionEnum(str, enum.Enum):
    left = "left"
    right = "right"


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
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    swipes = relationship("Swipe", back_populates="user", cascade="all, delete-orphan")
    agent = relationship("Agent", back_populates="user", uselist=False, cascade="all, delete-orphan")
    photos = relationship("UserPhoto", back_populates="user", cascade="all, delete-orphan", order_by="UserPhoto.display_order")


class UserPhoto(Base):
    __tablename__ = "user_photos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String(255), nullable=False)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="photos")

    @property
    def url(self) -> str:
        return f"/uploads/{self.filename}"


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    age = Column(Integer, nullable=False)
    location = Column(String(200), nullable=True)
    bio = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)  # comma-separated, e.g. "music,hiking,coffee"
    photo_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    swipes = relationship("Swipe", back_populates="candidate")
    matchmakers = relationship("Matchmaker", back_populates="candidate")


class Swipe(Base):
    __tablename__ = "swipes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    candidate_id = Column(Integer, ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False)
    direction = Column(Enum(SwipeDirectionEnum), nullable=False)
    swiped_at = Column(DateTime, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="swipes")
    candidate = relationship("Candidate", back_populates="swipes")


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
    agent_id = Column(Integer, ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)
    candidate_id = Column(Integer, ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(MatchmakerStatusEnum), nullable=False, default=MatchmakerStatusEnum.pending)
    contact_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    agent = relationship("Agent", back_populates="matchmakers")
    candidate = relationship("Candidate", back_populates="matchmakers")
