import re
from datetime import timedelta
from typing import Any, Callable, Optional, Union
from pathlib import Path
from simple_cache.cache_data import CacheData
from simple_cache.providers.provider import Provider

PathLike = Union[Path, str]


class FileProvider(Provider):
    def __init__(self, cache_dir: Optional[PathLike] = None):
        if cache_dir is not None:
            self.__validate_cache_dir(cache_dir)

    def init(self, **kwargs) -> None:
        cache_dir = kwargs.get("cache_dir", None)
        self.__validate_cache_dir(cache_dir)

    def __is_valid_directory_name(self, name: str):
        invalid_chars = r'[\\/*?:"<>|]'

        if re.search(invalid_chars, name):
            return False
        else:
            return True

    def __validate_cache_dir(self, cache_dir: PathLike) -> None:
        if (
            (cache_dir is None) or (cache_dir == "") or (
                isinstance(cache_dir, str) and
                self.__is_valid_directory_name(cache_dir) is False
            )
        ):
            raise ValueError(
                "The cache_dir argument should be a Path instance or a valid path string."
            )

        if isinstance(cache_dir, str):
            cache_dir = Path(cache_dir)

        if cache_dir.is_file():
            raise FileExistsError(
                "The provided cache_dir path already exists as a file."
            )

        self.cache_dir = cache_dir

    def get(
        self,
        key: str,
        action: Callable[[], str],
        expire_in: Optional[timedelta] = None
    ) -> CacheData:
        pass

    def set(
        self,
        key: str,
        value: Any,
        expire_in: Optional[timedelta] = None
    ) -> CacheData:
        pass

    def set_validate(self, key: str, valid: bool, silent: bool = True) -> None:
        pass
