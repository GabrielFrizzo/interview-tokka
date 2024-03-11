FROM python:3.11

WORKDIR /app/

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* /app/

RUN poetry install --no-root

ENV PYTHONPATH=/app/src


COPY ./src /app/src

COPY ./backend-start.sh /app/
RUN chmod +x /app/backend-start.sh
CMD [ "/app/backend-start.sh" ]
