from sqlmodel import SQLModel, create_engine

from config import settings
from schemas import schemas  # noqa: F401

engine = create_engine(settings.database_url, echo=settings.db_echo)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    init_db()
