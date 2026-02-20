from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app import models, schemas
from app.dependencies import get_db, get_current_user

router = APIRouter(prefix="/swipes", tags=["swipes"])


@router.post("/{candidate_id}", response_model=schemas.SwipeResponse, status_code=201)
def swipe_candidate(
    direction_body: schemas.SwipeRequest,
    candidate_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    candidate = db.get(models.Candidate, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    swipe = models.Swipe(
        user_id=current_user.id,
        candidate_id=candidate_id,
        direction=direction_body.direction,
    )
    db.add(swipe)

    if direction_body.direction == models.SwipeDirectionEnum.right:
        agent = db.scalar(
            select(models.Agent).where(models.Agent.user_id == current_user.id)
        )
        if agent:
            matchmaker = models.Matchmaker(
                agent_id=agent.id,
                candidate_id=candidate_id,
                status=models.MatchmakerStatusEnum.pending,
            )
            db.add(matchmaker)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already swiped on this candidate",
        )
    db.refresh(swipe)

    return db.scalar(
        select(models.Swipe)
        .options(joinedload(models.Swipe.candidate))
        .where(models.Swipe.id == swipe.id)
    )


@router.get("", response_model=list[schemas.SwipeResponse])
def get_swipe_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    swipes = db.scalars(
        select(models.Swipe)
        .options(joinedload(models.Swipe.candidate))
        .where(models.Swipe.user_id == current_user.id)
        .order_by(models.Swipe.swiped_at.desc())
    ).all()
    return swipes
