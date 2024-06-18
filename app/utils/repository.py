from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from sqlalchemy import insert, select

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class AbstractRepository(ABC):
    @abstractmethod
    def create_one(self, data):
        raise NotImplementedError

    @abstractmethod
    def create_multi(self, data_list):
        raise NotImplementedError

    @abstractmethod
    def get_one(self, filters=None, order_by=None):
        raise NotImplementedError

    @abstractmethod
    def get_all(
        self,
        filters=None,
        order_by=None,
    ):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, rec_id: int):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    model: Any = None

    def __init__(self, session: "Session") -> None:
        self.session = session

    def create_one(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        return self.session.execute(stmt).scalar_one()

    def create_multi(self, data_list: list[dict]) -> list[int]:
        stmt = insert(self.model).values(data_list).returning(self.model.id)
        return self.session.execute(stmt).scalars().all()

    def get_one(self, filters=None, order_by=None):
        stmt = select(self.model).filter(*filters).order_by(order_by).limit(1)
        return self.session.execute(stmt).scalars().one_or_none()

    def get_all(self, filters=None, order_by=None):
        stmt = select(self.model).filter(*filters).order_by(order_by)
        return self.session.execute(stmt).scalars().fetchall()

    def get_aggregated(self, aggregate_func: Callable, column_name: str, filters=None, order_by=None):
        selectee = aggregate_func(getattr(self.model, column_name))
        stmt = select(selectee).filter(*filters).order_by(order_by)
        return self.session.execute(stmt).scalars().all()

    def get_by_id(self, rec_id: int, for_update: bool = False):
        stmt = select(self.model, for_update=for_update).where(self.model.id == rec_id)
        return self.session.execute(stmt).scalars().one_or_none()
