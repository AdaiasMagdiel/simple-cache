from datetime import timedelta
from functools import wraps
from typing import Any, Callable, Optional

from simple_cache.cache_data import CacheData
from .providers.provider import Provider

__version__ = "1.0.0"


class SimpleCache(Provider):
    """
    A class that provides caching functionality for a given provider.

    Attributes:
        provider (Provider): The provider that handles the actual caching logic.
    """
    def __init__(self, provider: Provider) -> None:
        """
        Initialize the SimpleCache with a given provider.

        Args:
            provider (Provider): The provider that handles the actual caching logic.
        """

        self.provider = provider

    def init(self, **kwargs):
        """
        Initialize the provider with the given keyword arguments.

        Args:
            provider (Provider): The provider that handles the actual caching logic.
        """

        self.provider.init(**kwargs)

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

        return self.provider.get(key=key, action=action, expire_in=expire_in)

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

        return self.provider.set(key=key, value=value, expire_in=expire_in)

    def set_validate(self, key: str, valid: bool, silent: bool = True) -> None:
        """
        Set the validation status of a cached value.

        Args:
            key (str): The key of the cached value.
            valid (bool): Whether the cached value is valid.
            silent (bool): Whether to suppress errors.
        """

        self.provider.set_validate(key=key, valid=valid, silent=silent)

    def attach(self, key: str, expire_in: Optional[timedelta] = None):
        """
        Decorator to cache the result of a function.

        Args:
            key (str): The unique key for the cache.
            expire_in (Optional[timedelta]): The expiration time for the cache.

        Returns:
            Callable: The decorated function.
        """
        def decorator(function: Callable) -> Callable:
            @wraps(function)
            def inner(*args, **kwargs) -> Any:
                """
                Inner function that calls the original function and stores the result in the cache.

                Returns:
                    Any: The result of the original function.
                """
                def action():
                    return function(*args, **kwargs)

                return self.provider.get(
                    key=key, action=function, expire_in=expire_in
                )

            return inner

        return decorator

    def __getattr__(self, attr):
        """
        Get the attribute from the provider if it exists, otherwise raise an AttributeError.

        Args:
            attr (str): The attribute name.

        Returns:
            Any: The attribute value.

        Raises:
            AttributeError: If the attribute does not exist on the provider.
        """
        if hasattr(self.provider, attr):
            return getattr(self.provider, attr)
        else:
            raise AttributeError(
                f"The current provider '{type(self.provider).__name__}' object has no attribute '{attr}'"
            )
