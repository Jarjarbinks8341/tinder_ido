import os
import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_db, get_current_user

router = APIRouter(prefix="/users", tags=["users"])

UPLOAD_DIR = "uploads"


@router.patch("/me", response_model=schemas.UserResponse)
def update_me(
    payload: schemas.UserUpdateRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if payload.location is not None:
        current_user.location = payload.location
    if payload.bio is not None:
        current_user.bio = payload.bio
    if payload.tags is not None:
        current_user.tags = payload.tags
    db.commit()
    db.refresh(current_user)
    return current_user


@router.post("/me/photos", response_model=schemas.UserResponse, status_code=201)
async def upload_photos(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    existing_count = len(current_user.photos)
    if existing_count + len(files) > 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot exceed 6 photos total (you already have {existing_count})",
        )

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    for i, file in enumerate(files):
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File '{file.filename}' is not an image",
            )
        ext = (file.filename or "jpg").rsplit(".", 1)[-1].lower()
        filename = f"user_{current_user.id}_{uuid.uuid4().hex[:8]}.{ext}"
        path = os.path.join(UPLOAD_DIR, filename)
        content = await file.read()
        with open(path, "wb") as f:
            f.write(content)

        photo = models.UserPhoto(
            user_id=current_user.id,
            filename=filename,
            display_order=existing_count + i,
        )
        db.add(photo)

    db.commit()
    db.refresh(current_user)
    return current_user


@router.delete("/me/photos/{photo_id}", response_model=schemas.UserResponse)
def delete_photo(
    photo_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    photo = db.get(models.UserPhoto, photo_id)
    if not photo or photo.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")

    path = os.path.join(UPLOAD_DIR, photo.filename)
    if os.path.exists(path):
        os.remove(path)

    db.delete(photo)
    db.commit()
    db.refresh(current_user)
    return current_user
