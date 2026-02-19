from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app import models, schemas, auth
from app.dependencies import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=schemas.UserResponse, status_code=201)
def register(payload: schemas.UserRegisterRequest, db: Session = Depends(get_db)):
    existing = db.scalar(select(models.User).where(models.User.email == payload.email))
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user = models.User(
        email=payload.email,
        password_hash=auth.hash_password(payload.password),
        name=payload.name,
        gender=payload.gender,
        age=payload.age,
    )
    db.add(user)
    db.flush()  # get user.id before creating Agent

    agent = models.Agent(
        user_id=user.id,
        name=f"{payload.name}'s Agent",
        status=models.AgentStatusEnum.pending,
    )
    db.add(agent)
    db.commit()
    db.refresh(user)

    return user


@router.post("/login", response_model=schemas.TokenResponse)
def login(payload: schemas.UserLoginRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(models.User).where(models.User.email == payload.email))

    if not user or not auth.verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = auth.create_access_token(user.id)
    return schemas.TokenResponse(access_token=token)
