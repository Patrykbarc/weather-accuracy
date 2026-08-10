from sqlmodel import SQLModel, create_engine

from schemas import schemas  # noqa: F401

sqlite_connection = "sqlite:///weather.db"
engine = create_engine(sqlite_connection, echo=True)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    init_db()
