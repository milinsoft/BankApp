from app.repository import SqlAlchemyRepository

from .models import Transaction


class TransactionRepository(SqlAlchemyRepository):
    model = Transaction
