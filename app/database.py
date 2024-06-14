from typing import TYPE_CHECKING

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from app.config import settings

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class Database:
    """DB connection abstraction.

    DB url format: ``dialect[+driver]://user:password@host/dbname[?key=value..]``,  # pragma: allowlist secret

    Examples:
        'postgresql+psycopg2://scott:tiger@localhost/dbname'  # pragma: allowlist secret
        'sqlite:///db_name.extension'

    """

    def __init__(self, db_url: str = settings.DB_URL) -> None:
        self.db_url: str = db_url
        self.engine: "Engine" = create_engine(self.db_url)
        self._create_tables()

    def create_session(self) -> Session:
        return sessionmaker(bind=self.engine)()

    def _create_tables(self):
        # Create tables if they don't exist
        Base.metadata.create_all(self.engine)

    def _drop_tables(self):
        if self.db_url == settings.TEST_DB_URL:
            Base.metadata.drop_all(self.engine)
