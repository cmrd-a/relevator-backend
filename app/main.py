import time

from fastapi import FastAPI, Request
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db.common import SessionLocal
from app.routers import items, users, auth
from app.settings import settings

app = FastAPI(debug=settings.debug)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(items.router)


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = f'{int(process_time * 1000)} ms'
    return response


@app.on_event('startup')
def startup_event():
    db: Session = SessionLocal()
    user = crud.get_user_by_email(db, settings.super_user_email)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.super_user_email, password=settings.super_user_password
        )
        crud.create_user(db, user_in)
    db.close()
