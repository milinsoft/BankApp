from typing import TYPE_CHECKING

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import settings
from app.models import Base
from app.utils import Singleton

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine


class Database(metaclass=Singleton):
    """DB connection abstraction.

    DB url format: ``dialect[+driver]://user:password@host/dbname[?key=value..]``,  # pragma: allowlist secret

    Examples:
        'postgresql+psycopg2://scott:tiger@localhost/dbname'  # pragma: allowlist secret
        'sqlite:///db_name.extension'

    """

    def __init__(self, db_url: str = settings.DB_URL) -> None:
        self.db_url: str = db_url
        self.engine: "Engine" = create_engine(self.db_url)
        # Create tables if they don't exist
        Base.metadata.create_all(self.engine)

    def create_session(self) -> Session:
        return sessionmaker(bind=self.engine)()
