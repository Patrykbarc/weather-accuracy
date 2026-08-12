from sqlmodel import create_engine

from api.config import settings
from api.schemas import schemas  # noqa: F401

engine = create_engine(settings.database_url, echo=settings.db_echo)
