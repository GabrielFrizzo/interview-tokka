from sqlmodel import SQLModel, create_engine

sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url, echo=True)  # noqa: F821


def create_db_and_tables():
    print("Creating tables:")
    import models  # noqa

    SQLModel.metadata.create_all(engine)


create_db_and_tables()
