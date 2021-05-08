from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.settings import settings

engine = create_engine(settings.sqlalchemy_url, connect_args={'check_same_thread': False}, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

Base = declarative_base()
import app.db.models  # noqa for alembic revision --autogenerate
