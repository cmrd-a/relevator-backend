from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, deps, models, schemas

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.get('/', response_model=List[schemas.User])
async def read_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(deps.get_db)
):
    """Read users.

    Doesn't require authentication.
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get('/me', response_model=schemas.User)
async def read_user_me(
        current_user: models.User = Depends(deps.get_current_user),
):
    """Read the user data for the currently authenticated user."""
    return current_user


@router.get('/{user_id}', response_model=schemas.User)
async def read_user(
        user_id: int,
        db: Session = Depends(deps.get_db)
):
    """Read the data for a specific user.

    Doesn't require authentication.
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return db_user


@router.post(
    '/',
    response_model=schemas.User,
    dependencies=[Depends(deps.get_current_superuser)],
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    """Create a new user. Ony accessible by the superuser."""

    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered')
    return crud.create_user(db=db, user=user)
