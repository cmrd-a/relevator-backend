# relevator-backend
Run in debug-mode:
* ```pip install poetry```
* ```poetry install```
* ```poetry shell```
* ```cp .env.example .env```
* ```alembic upgrade head```
* ```uvicorn app.main:app --reload```

Run tests:
* ```export ITS_TEST=True``` This is necessary in order to switch to the test database.
* ```pytest```

## Features:
* [ ] Tests
* [ ] Logging
* [ ] Postgres DB
* [ ] Async db queries
