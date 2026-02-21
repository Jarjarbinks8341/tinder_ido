from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_, select

from app import models, schemas
from app.dependencies import get_db, get_current_user

router = APIRouter(prefix="/candidates", tags=["candidates"])


@router.post("/search", response_model=list[schemas.ProfileResponse])
def search_candidates(
    filters: schemas.CandidateSearchRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # Exclude current user and users already swiped on
    already_swiped = select(models.Swipe.target_user_id).where(
        models.Swipe.user_id == current_user.id
    )

    stmt = select(models.User).where(
        models.User.id != current_user.id,
        models.User.id.not_in(already_swiped),
    )

    if filters.gender is not None:
        stmt = stmt.where(models.User.gender == filters.gender)
    if filters.min_age is not None:
        stmt = stmt.where(models.User.age >= filters.min_age)
    if filters.max_age is not None:
        stmt = stmt.where(models.User.age <= filters.max_age)

    if filters.tags:
        tag_conditions = []
        for tag in filters.tags:
            t = tag.lower().strip()
            tag_conditions.append(models.User.tags.ilike(f"%{t}%"))
        stmt = stmt.where(or_(*tag_conditions))

    if filters.location:
        stmt = stmt.where(models.User.location.ilike(f"%{filters.location}%"))
    if filters.education is not None:
        stmt = stmt.where(models.User.education == filters.education)
    if filters.industry is not None:
        stmt = stmt.where(models.User.industry == filters.industry)
    if filters.income_range is not None:
        stmt = stmt.where(models.User.income_range == filters.income_range)

    return db.scalars(stmt).all()
