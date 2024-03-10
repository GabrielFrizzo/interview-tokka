FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /app/

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* /app/

RUN poetry install --no-root

ENV MODULE_NAME=src.api.main
ENV PYTHONPATH=/app

# COPY ./alembic.ini /app/

# COPY ./prestart.sh /app/

# COPY ./tests-start.sh /app/

COPY ./src /app/src
