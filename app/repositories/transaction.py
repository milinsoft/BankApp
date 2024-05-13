from app.models import Transaction
from app.utils import SqlAlchemyRepository


class TransactionRepository(SqlAlchemyRepository):
    model = Transaction
