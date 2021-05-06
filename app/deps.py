from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status

from app import crud, models, schemas, security
from app.database import SessionLocal
from app.settings import settings

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl='/login/access-token')


async def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        # noinspection PyUnboundLocalVariable
        db.close()


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[security.ALGORITHM])
        token_data = schemas.TokenPayload(**payload)
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Could not validate credentials')
    user = crud.get_user(db, user_id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


async def get_current_superuser(current_user: models.User = Depends(get_current_user)):
    if not current_user.email == settings.super_user_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not the superuser')
    return current_user
