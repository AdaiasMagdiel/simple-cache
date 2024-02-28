from datetime import datetime, UTC
from deta import Deta, _Base
from typing import Any, Callable, Optional

__version__ = "0.0.3"


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

    def get(self, key: str, action: Callable[[], str]) -> CacheData:
        if key is None or key == "":
            raise ValueError("Key can not be None or empty")

        res: dict = self.cache_db.get(key=key) or {}  # type:ignore
        value = res.get("value", None)
        valid = res.get("valid", False)

        if value is None or valid is False:
            value = action()

            self.set(key=key, value=value)
            return CacheData(value=value, valid=True)

        return CacheData(value=value, valid=valid)

    def set(self, key: str, value: Any) -> CacheData:
        if key is None or key == "":
            raise ValueError("Key can not be None or empty")

        self.cache_db.put(
            data={
                "value": value,
                "valid": True,
                "created_at": datetime.now(UTC).isoformat(),
            },
            key=key,
        )  # type:ignore

        return CacheData(value=value, valid=True)

    def set_validate(self, key: str, valid: bool, silent: bool = True) -> None:
        if key is None or key == "":
            raise ValueError("Key can not be None or empty")

        try:
            self.cache_db.update(key=key, updates={"valid": valid})
        except Exception as e:
            if not silent:
                raise ValueError(e)
            else:
                return None
