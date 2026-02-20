from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_, select

from app import models, schemas
from app.dependencies import get_db, get_current_user

router = APIRouter(prefix="/candidates", tags=["candidates"])


@router.post("/search", response_model=list[schemas.CandidateResponse])
def search_candidates(
    filters: schemas.CandidateSearchRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # Subquery: candidate IDs the user has already swiped on
    already_swiped = select(models.Swipe.candidate_id).where(
        models.Swipe.user_id == current_user.id
    )

    stmt = select(models.Candidate).where(
        models.Candidate.id.not_in(already_swiped)
    )

    if filters.gender is not None:
        stmt = stmt.where(models.Candidate.gender == filters.gender)
    if filters.min_age is not None:
        stmt = stmt.where(models.Candidate.age >= filters.min_age)
    if filters.max_age is not None:
        stmt = stmt.where(models.Candidate.age <= filters.max_age)

    if filters.tags:
        tag_conditions = []
        for tag in filters.tags:
            t = tag.lower().strip()
            # Match tag anywhere in comma-separated list
            tag_conditions.append(models.Candidate.tags.ilike(f"%{t}%"))
        stmt = stmt.where(or_(*tag_conditions))

    return db.scalars(stmt).all()
