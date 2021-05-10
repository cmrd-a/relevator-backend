from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.db.common import SessionLocal, engine
from app.db.models import *
from app.main import app

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope='session')
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope='module')
def client() -> Generator:
    with TestClient(app) as c:
        yield c
