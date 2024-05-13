import sys
from logging import getLogger

from app.cli import BankAppCli
from app.database import Database

_logger = getLogger(__name__)
MAJOR = 3
MINOR = 11


def check_python_version(min_version=(MAJOR, MINOR)):
    if sys.version_info[:2] < min_version:
        _logger.error(f"Python {min_version[0]}.{min_version[1]} or above is required.")
        sys.exit(1)


if __name__ == "__main__":
    check_python_version()
    db = Database()
    app = BankAppCli(db)
    try:
        app.main_menu()
    except KeyboardInterrupt:
        print("\nGoodbye!")
