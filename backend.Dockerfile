FROM python:3.11

WORKDIR /app/

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* /app/

RUN poetry install --no-root

ENV PYTHONPATH=/app/src

# COPY ./alembic.ini /app/

# COPY ./prestart.sh /app/

# COPY ./tests-start.sh /app/

COPY ./src /app/src

CMD ["poetry", "run", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
