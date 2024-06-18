from app.utils.repository import SqlAlchemyRepository

from .models import Transaction


class TransactionRepository(SqlAlchemyRepository):
    model = Transaction
