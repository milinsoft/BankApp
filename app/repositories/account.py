from typing import TYPE_CHECKING

from app.models import Account
from app.utils import SqlAlchemyRepository

if TYPE_CHECKING:
    from decimal import Decimal


class AccountRepository(SqlAlchemyRepository):
    model = Account

    def update_balance(self, account_id: int, amount_to_add: "Decimal") -> "Decimal":
        account = self.get_by_id(account_id)
        new_balance = account.balance + amount_to_add  # type: ignore[attr-defined]
        credit_limit = account.credit_limit  # type: ignore[attr-defined]
        if new_balance < credit_limit:
            raise ValueError(f"\nImpossible to import data, as your account balance would go less than {credit_limit}")
        self.update({"balance": new_balance}, where=[self.model.id == account_id])
        return new_balance
