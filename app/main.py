from fastapi import FastAPI
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import items, users, auth
from app.database import SessionLocal, engine
from app.settings import settings

app = FastAPI()

app.include_router(auth.router, tags=["auth"])
app.include_router(users.router, tags=["users"])
app.include_router(items.router, tags=["items"])


@app.on_event("startup")
def startup_event():
    models.Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    user = crud.get_user_by_email(db, settings.super_user_email)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.super_user_email, password=settings.super_user_password
        )
        crud.create_user(db, user_in)
    db.close()
