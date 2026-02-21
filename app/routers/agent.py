from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app import models, schemas
from app.dependencies import get_db, get_current_user

router = APIRouter(tags=["agent"])


@router.get("/agent/me", response_model=schemas.AgentResponse)
def get_my_agent(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    agent = db.scalar(
        select(models.Agent).where(models.Agent.user_id == current_user.id)
    )
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found for this user")
    return agent


@router.get("/matchmaker", response_model=list[schemas.MatchmakerResponse])
def get_matchmakers(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    agent = db.scalar(
        select(models.Agent).where(models.Agent.user_id == current_user.id)
    )
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found for this user")

    return db.scalars(
        select(models.Matchmaker)
        .options(joinedload(models.Matchmaker.target_user).joinedload(models.User.photos))
        .where(models.Matchmaker.agent_id == agent.id)
        .order_by(models.Matchmaker.created_at.desc())
    ).unique().all()
