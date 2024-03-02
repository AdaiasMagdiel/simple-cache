from datetime import timedelta
from typing import Any, Callable, Optional

from simple_cache.cache_data import CacheData
from .providers.provider import Provider

__version__ = "1.0.0"


class SimpleCache(Provider):
    def __init__(self, provider: Provider) -> None:
        self.provider = provider

    def init(self, **kwargs):
        self.provider.init(**kwargs)

    def get(
        self,
        key: str,
        action: Callable[[], str],
        expire_in: Optional[timedelta] = None
    ) -> CacheData:
        return self.provider.get(key=key, action=action, expire_in=expire_in)

    def set(
        self,
        key: str,
        value: Any,
        expire_in: Optional[timedelta] = None
    ) -> CacheData:
        return self.provider.set(key=key, value=value, expire_in=expire_in)

    def set_validate(self, key: str, valid: bool, silent: bool = True) -> None:
        self.provider.set_validate(key=key, valid=valid, silent=silent)

    def __getattr__(self, attr):
        if hasattr(self.provider, attr):
            return getattr(self.provider, attr)
        else:
            raise AttributeError(
                f"The current provider '{type(self.provider).__name__}' object has no attribute '{attr}'"
            )
