from sqlalchemy.orm import Session

from app import crud, schemas
from app.db.models import Base  # noqa
from app.settings import settings


def init_db(db: Session) -> None:
    user = crud.get_user_by_email(db, settings.super_user_email)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.super_user_email, password=settings.super_user_password
        )
        crud.create_user(db, user_in)
    db.close()
