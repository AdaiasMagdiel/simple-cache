from datetime import datetime, timedelta
from typing import Any, Callable, Optional
from deta import Deta, _Base
from simple_cache.cache_data import CacheData
from simple_cache.providers.provider import Provider

database = {}


class MockProvider(Provider):
    """
    A class that provides caching functionality using Deta as the backend.

    Attributes:
        cache_table (str): The name of the cache table in Deta.
        deta (Deta): The Deta client instance.
        cache_db (_Base): The Deta Base instance for the cache table.
    """

    cache_table = "sc_cache"
    deta: Deta
    cache_db: _Base

    def __init__(self,) -> None:
        pass

    def init(self, **kwargs) -> None:
        pass

    def get(
        self,
        key: str,
        action: Callable[[], str],
        expire_in: Optional[timedelta] = None
    ) -> CacheData:
        res = database.get(key, {})

        value = res.get("value", None)
        valid = res.get("valid", False)
        expires = res.get("expires", None)

        actual_timestamp = datetime.now().timestamp()
        if (value is None or
            valid is False) or (expires and expires <= actual_timestamp):
            value = action()

            self.set(key=key, value=value, expire_in=expire_in)

            return CacheData(value=value, valid=True)

        return CacheData(value=value, valid=valid)

    def set(
        self,
        key: str,
        value: Any,
        expire_in: Optional[timedelta] = None
    ) -> CacheData:
        data = {
            "value": value,
            "valid": True,
        }

        if expire_in:
            data["expires"] = (datetime.now() + expire_in).timestamp()

        database[key] = data

        return CacheData(value=value, valid=True)

    def set_validate(self, key: str, valid: bool, silent: bool = True) -> None:
        if key in database:
            database[key]['valid'] = valid
