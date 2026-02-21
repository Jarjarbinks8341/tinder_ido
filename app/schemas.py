from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator, computed_field, ConfigDict
from app.models import (
    GenderEnum, SwipeDirectionEnum, AgentStatusEnum, MatchmakerStatusEnum,
    IncomeRangeEnum, EducationEnum, IndustryEnum,
)


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    gender: GenderEnum
    age: int
    location: Optional[str] = None
    bio: Optional[str] = None
    tags: Optional[str] = None
    income_range: Optional[IncomeRangeEnum] = None
    education: Optional[EducationEnum] = None
    industry: Optional[IndustryEnum] = None

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


class UserPhotoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    display_order: int


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    name: str
    gender: GenderEnum
    age: int
    location: Optional[str] = None
    bio: Optional[str] = None
    tags: Optional[str] = None
    income_range: Optional[IncomeRangeEnum] = None
    education: Optional[EducationEnum] = None
    industry: Optional[IndustryEnum] = None
    photos: list[UserPhotoResponse] = []
    created_at: datetime


class UserUpdateRequest(BaseModel):
    location: Optional[str] = None
    bio: Optional[str] = None
    tags: Optional[str] = None
    income_range: Optional[IncomeRangeEnum] = None
    education: Optional[EducationEnum] = None
    industry: Optional[IndustryEnum] = None


# ---------------------------------------------------------------------------
# Profile (public view — no email or password exposed)
# ---------------------------------------------------------------------------

class ProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    gender: GenderEnum
    age: int
    location: Optional[str] = None
    bio: Optional[str] = None
    tags: Optional[str] = None
    income_range: Optional[IncomeRangeEnum] = None
    education: Optional[EducationEnum] = None
    industry: Optional[IndustryEnum] = None
    photos: list[UserPhotoResponse] = []

    @computed_field
    @property
    def photo_url(self) -> Optional[str]:
        return self.photos[0].url if self.photos else None


# ---------------------------------------------------------------------------
# Candidate search (browse other users)
# ---------------------------------------------------------------------------

class CandidateSearchRequest(BaseModel):
    gender: Optional[GenderEnum] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    tags: Optional[list[str]] = None
    location: Optional[str] = None
    education: Optional[EducationEnum] = None
    industry: Optional[IndustryEnum] = None
    income_range: Optional[IncomeRangeEnum] = None

    @field_validator("min_age", "max_age")
    @classmethod
    def age_bounds(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and not (18 <= v <= 100):
            raise ValueError("Age filter must be between 18 and 100")
        return v


# ---------------------------------------------------------------------------
# Swipe
# ---------------------------------------------------------------------------

class SwipeRequest(BaseModel):
    direction: SwipeDirectionEnum


class SwipeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    target_user_id: int
    direction: SwipeDirectionEnum
    swiped_at: datetime
    target_user: ProfileResponse


# ---------------------------------------------------------------------------
# Match
# ---------------------------------------------------------------------------

class MatchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user1_id: int
    user2_id: int
    matched_at: datetime
    user1: ProfileResponse
    user2: ProfileResponse


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
    target_user_id: int
    status: MatchmakerStatusEnum
    contact_notes: Optional[str]
    created_at: datetime
    target_user: ProfileResponse
