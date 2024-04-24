import sys
from logging import getLogger

from app.database import Database
from app.interface import BankAppCli
from settings import DB_URL

_logger = getLogger(__name__)
MAJOR = 3
MINOR = 11


def check_python_version(min_version=(MAJOR, MINOR)):
    if sys.version_info[:2] < min_version:
        _logger.error(f"Python {min_version[0]}.{min_version[1]} or above is required.")
        sys.exit(1)


if __name__ == "__main__":
    check_python_version()
    db_session = Database(DB_URL).session
    app = BankAppCli(db_session)
    try:
        app.main_menu()
    except KeyboardInterrupt:
        db_session.close()
        print("\nGoodbye!")
