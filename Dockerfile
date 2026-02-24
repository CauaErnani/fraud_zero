FROM python:3.13-slim

ENV POETRY_VIRTUALENVS_CREATE=false \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config installer.max-workers 10 && \
    poetry install --no-interaction --no-ansi --without dev

COPY . .

RUN chmod +x ./entrypoint.sh

EXPOSE 8000

CMD ["uvicorn", "--host", "0.0.0.0", "app.main:app"]