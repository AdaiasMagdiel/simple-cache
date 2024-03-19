from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any, Callable, Optional
from simple_cache.cache_data import CacheData


class Provider(ABC):
    """
    An abstract base class for cache providers.

    This class defines the interface for cache providers.
    """
    @abstractmethod
    def init(self, **kwargs):
        """
        Initialize the provider with the given keyword arguments.

        Args:
            **kwargs: Keyword arguments to initialize the provider.
        """
        pass

    @abstractmethod
    def get(
        self,
        key: str,
        action: Callable[[], str],
        expire_in: Optional[timedelta] = None
    ) -> CacheData:
        """
        Retrieve a value from the cache.

        Args:
            key (str): The key to retrieve the value from the cache.
            action (Callable[[], str]): A callable that returns the value to be cached.
            expire_in (Optional[timedelta]): The time after which the cached value expires.

        Returns:
            CacheData: The cached data.
        """
        pass

    @abstractmethod
    def set(
        self,
        key: str,
        value: Any,
        expire_in: Optional[timedelta] = None
    ) -> CacheData:
        """
        Store a value in the cache.

        Args:
            key (str): The key to store the value in the cache.
            value (Any): The value to be cached.
            expire_in (Optional[timedelta]): The time after which the cached value expires.

        Returns:
            CacheData: The cached data.
        """
        pass

    @abstractmethod
    def set_validate(self, key: str, valid: bool, silent: bool = True) -> None:
        """
        Set the validation status of a cached value.

        Args:
            key (str): The key of the cached value.
            valid (bool): Whether the cached value is valid.
            silent (bool): Whether to suppress errors.
        """
        pass
