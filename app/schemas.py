from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from app.models import GenderEnum, SwipeDirectionEnum, AgentStatusEnum, MatchmakerStatusEnum


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    gender: GenderEnum
    age: int

    @field_validator("age")
    @classmethod
    def age_must_be_reasonable(cls, v: int) -> int:
        if not (18 <= v <= 100):
            raise ValueError("Age must be between 18 and 100")
        return v

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    name: str
    gender: GenderEnum
    age: int
    created_at: datetime


# ---------------------------------------------------------------------------
# Candidate
# ---------------------------------------------------------------------------

class CandidateSearchRequest(BaseModel):
    gender: Optional[GenderEnum] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    tags: Optional[list[str]] = None

    @field_validator("min_age", "max_age")
    @classmethod
    def age_bounds(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and not (18 <= v <= 100):
            raise ValueError("Age filter must be between 18 and 100")
        return v


class CandidateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    gender: GenderEnum
    age: int
    location: Optional[str]
    bio: Optional[str]
    tags: Optional[str]
    photo_url: Optional[str]


# ---------------------------------------------------------------------------
# Swipe
# ---------------------------------------------------------------------------

class SwipeRequest(BaseModel):
    direction: SwipeDirectionEnum


class SwipeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    candidate_id: int
    direction: SwipeDirectionEnum
    swiped_at: datetime
    candidate: CandidateResponse


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------

class AgentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: str
    status: AgentStatusEnum
    notes: Optional[str]
    created_at: datetime


# ---------------------------------------------------------------------------
# Matchmaker
# ---------------------------------------------------------------------------

class MatchmakerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    agent_id: int
    candidate_id: int
    status: MatchmakerStatusEnum
    contact_notes: Optional[str]
    created_at: datetime
    candidate: CandidateResponse
