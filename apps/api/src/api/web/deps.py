from typing import TYPE_CHECKING

from sqlmodel import Session

from api.db import engine

if TYPE_CHECKING:
    from collections.abc import Iterator


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
