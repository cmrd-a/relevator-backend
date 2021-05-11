FROM python:3.9.5

EXPOSE 8000
WORKDIR /app

RUN pip install poetry==1.1
COPY pyproject.toml ./
RUN poetry config virtualenvs.in-project true && \
    poetry install

COPY . .

CMD poetry run uvicorn --host=0.0.0.0 app.main:app