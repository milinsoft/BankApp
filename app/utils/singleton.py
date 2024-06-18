from threading import Lock
from typing import Any


class Singleton(type):
    _instance = None
    _lock = Lock()

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        if not cls._instance:
            with cls._lock:
                # Another thread could have created the instance
                # before the lock was acquired. So check that the
                # instance is still nonexistent.
                if not cls._instance:
                    cls._instance = super().__new__(cls, *args)
        return cls._instance
