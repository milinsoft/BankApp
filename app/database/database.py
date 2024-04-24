from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

import settings
from app.models import Base


class Database:
    """DB connection abstraction.

    DB url format: ``dialect[+driver]://user:password@host/dbname[?key=value..]``,  # pragma: allowlist secret

    Examples:
        'postgresql+psycopg2://scott:tiger@localhost/dbname'  # pragma: allowlist secret
        'sqlite:///db_name.extension'

    """

    def __init__(self, db_url: str = settings.DB_URL) -> None:
        self.db_url: str = db_url
        self.engine: Engine = create_engine(self.db_url)
        self.session: Session = self.create_session()

    def create_session(self) -> Session:
        # Create tables if they don't exist
        Base.metadata.create_all(self.engine)
        return sessionmaker(bind=self.engine)()
