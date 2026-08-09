from schemas import schemas  # noqa: F401
from sqlmodel import SQLModel, create_engine

sqlite_connection = "sqlite:///weather.db"
engine = create_engine(sqlite_connection, echo=True)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    init_db()
