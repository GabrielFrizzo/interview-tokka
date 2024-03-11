import os

from sqlmodel import SQLModel, create_engine


def get_url():
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "")
    server = os.getenv("POSTGRES_SERVER", "db")
    db = os.getenv("POSTGRES_DB", "app")
    return f"postgresql+psycopg://{user}:{password}@{server}/{db}"


engine = create_engine(get_url(), echo=True)


def create_db_and_tables():
    print("Creating tables:")
    import models  # noqa

    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
