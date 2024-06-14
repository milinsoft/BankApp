from typing import TYPE_CHECKING

from sqlalchemy import select

from app.repository import SqlAlchemyRepository

from .models import Account

if TYPE_CHECKING:
    from decimal import Decimal


class AccountRepository(SqlAlchemyRepository):
    model = Account

    def update_balance(self, account_id: int, amount_to_add: "Decimal") -> None:
        stmt = select(self.model).where(self.model.id == account_id).with_for_update()
        account = self.session.execute(stmt).scalars().one_or_none()
        account.balance += amount_to_add
        if account.balance < account.credit_limit:
            raise ValueError(
                f"Impossible to import data, as your account balance would go less than {account.credit_limit}"
            )
