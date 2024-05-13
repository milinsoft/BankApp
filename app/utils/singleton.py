from threading import Lock


class Singleton(type):
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs) -> type["Singleton"]:
        if not cls._instance:
            with cls._lock:
                # Another thread could have created the instance
                # before the lock was acquired. So check that the
                # instance is still nonexistent.
                if not cls._instance:
                    cls._instance = super().__new__(cls, *args)
        return cls._instance
