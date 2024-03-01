from datetime import datetime, UTC, timedelta
from deta import Deta, _Base
from typing import Any, Callable, Optional

__version__ = "0.0.4"


class CacheData:
    def __init__(self, value: Any, valid: bool) -> None:
        self.value = value
        self.valid = valid

    def __repr__(self) -> str:
        return f'<CacheData value="..." valid="{self.valid}">'


class SimpleCache:
    cache_table = "sc_cache"
    deta: Deta
    cache_db: _Base

    def __init__(
        self,
        deta_key: Optional[str] = None,
        table_name: Optional[str] = None
    ) -> None:
        if table_name == "":
            raise ValueError(
                "The table name should be a valid name, not a empty string"
            )

        if table_name:
            self.cache_table = table_name

        if deta_key is not None:
            self.deta_key = deta_key
            self.__configure_db()

    def init(self, deta_key: str, table_name: Optional[str] = None) -> None:
        if table_name == "":
            raise ValueError(
                "The table name should be a valid name, not a empty string"
            )

        if table_name:
            self.cache_table = table_name

        self.deta_key = deta_key

        self.__configure_db()

    def __configure_db(self):
        self.deta = Deta(self.deta_key)
        self.cache_db = self.deta.Base(self.cache_table)

    def get(
        self,
        key: str,
        action: Callable[[], str],
        expire_in: Optional[timedelta] = None
    ) -> CacheData:
        if not key:
            raise ValueError("Key can not be None or empty")

        if expire_in and not isinstance(expire_in, timedelta):
            raise TypeError(
                "'expire_in' must be a 'timedelta' with the expire time"
            )

        res: dict = self.cache_db.get(key=key) or {}  # type:ignore
        value = res.get("value")
        valid = res.get("valid", False)
        expires = res.get("expires")

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
        if not key:
            raise ValueError("Key can not be None or empty")

        data = {
            "value": value,
            "valid": True,
            "created_at": datetime.now(UTC).isoformat(),
        }

        if expire_in:
            if not isinstance(expire_in, timedelta):
                raise TypeError(
                    "'expire_in' must be a 'timedelta' with the expire time"
                )

            data["expires"] = (datetime.now() + expire_in).timestamp()

        self.cache_db.put(data=data, key=key)

        return CacheData(value=value, valid=True)

    def set_validate(self, key: str, valid: bool, silent: bool = True) -> None:
        if not key:
            raise ValueError("Key can not be None or empty")

        try:
            self.cache_db.update(key=key, updates={"valid": valid})
        except Exception as e:
            if not silent:
                raise ValueError(e)
            else:
                return None
