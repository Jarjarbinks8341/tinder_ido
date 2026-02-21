from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app import models, schemas
from app.dependencies import get_db, get_current_user

router = APIRouter(prefix="/swipes", tags=["swipes"])


@router.get("/matches", response_model=list[schemas.MatchResponse])
def get_matches(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return db.scalars(
        select(models.Match)
        .options(
            joinedload(models.Match.user1).joinedload(models.User.photos),
            joinedload(models.Match.user2).joinedload(models.User.photos),
        )
        .where(
            (models.Match.user1_id == current_user.id) |
            (models.Match.user2_id == current_user.id)
        )
        .order_by(models.Match.matched_at.desc())
    ).unique().all()


@router.post("/{target_user_id}", response_model=schemas.SwipeResponse, status_code=201)
def swipe_user(
    direction_body: schemas.SwipeRequest,
    target_user_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if target_user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot swipe on yourself")

    target_user = db.get(models.User, target_user_id)
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    swipe = models.Swipe(
        user_id=current_user.id,
        target_user_id=target_user_id,
        direction=direction_body.direction,
    )
    db.add(swipe)

    if direction_body.direction == models.SwipeDirectionEnum.right:
        # Check for mutual right swipe → create match
        mutual = db.scalar(
            select(models.Swipe).where(
                models.Swipe.user_id == target_user_id,
                models.Swipe.target_user_id == current_user.id,
                models.Swipe.direction == models.SwipeDirectionEnum.right,
            )
        )
        if mutual:
            u1, u2 = sorted([current_user.id, target_user_id])
            db.add(models.Match(user1_id=u1, user2_id=u2))

        # Queue in matchmaker if user has an agent
        agent = db.scalar(
            select(models.Agent).where(models.Agent.user_id == current_user.id)
        )
        if agent:
            db.add(models.Matchmaker(
                agent_id=agent.id,
                target_user_id=target_user_id,
                status=models.MatchmakerStatusEnum.pending,
            ))

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already swiped on this user",
        )
    db.refresh(swipe)

    return db.scalar(
        select(models.Swipe)
        .options(joinedload(models.Swipe.target_user).joinedload(models.User.photos))
        .where(models.Swipe.id == swipe.id)
    )


@router.get("", response_model=list[schemas.SwipeResponse])
def get_swipe_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return db.scalars(
        select(models.Swipe)
        .options(joinedload(models.Swipe.target_user).joinedload(models.User.photos))
        .where(models.Swipe.user_id == current_user.id)
        .order_by(models.Swipe.swiped_at.desc())
    ).unique().all()
