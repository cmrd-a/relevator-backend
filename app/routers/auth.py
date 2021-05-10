from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, deps, schemas, security

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post('/access-token', response_model=schemas.Token)
async def login_access_token(
        db: Session = Depends(deps.get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
):
    """OAuth2 compatible token login, get an access token for future requests."""
    user = crud.authenticate_user(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect email or password')
    return {
        'access_token': security.create_access_token(subject=user.id),
        'token_type': 'bearer',
    }
