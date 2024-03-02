from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any, Callable, Optional
from simple_cache.cache_data import CacheData


class Provider(ABC):
    @abstractmethod
    def init(self, **kwargs):
        pass

    @abstractmethod
    def get(
        self,
        key: str,
        action: Callable[[], str],
        expire_in: Optional[timedelta] = None
    ) -> CacheData:
        pass

    @abstractmethod
    def set(
        self,
        key: str,
        value: Any,
        expire_in: Optional[timedelta] = None
    ) -> CacheData:
        pass

    @abstractmethod
    def set_validate(self, key: str, valid: bool, silent: bool = True) -> None:
        pass
