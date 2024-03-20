import re
import pickle
from uuid import uuid4
from datetime import datetime, timedelta
from typing import Any, Callable, Optional, Union
from pathlib import Path
from simple_cache.cache_data import CacheData
from simple_cache.providers.provider import Provider

PathLike = Union[Path, str]


class FileProvider(Provider):
    cache_dir: Path

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
        error_message = "The cache_dir argument should be a Path instance or a valid path string."

        if (cache_dir is None) or (cache_dir == ""):
            raise ValueError(error_message)

        if not isinstance(cache_dir, (str, Path)):
            raise ValueError(error_message)

        if isinstance(cache_dir, str
                     ) and self.__is_valid_directory_name(cache_dir) is False:
            raise ValueError(error_message)

        if isinstance(cache_dir, str):
            cache_dir = Path(cache_dir)

        if cache_dir.is_file():
            raise FileExistsError(
                "The provided cache_dir path already exists as a file."
            )

        if not cache_dir.exists():
            cache_dir.mkdir()

        self.cache_dir = cache_dir
        self.metadata = self.cache_dir.joinpath('.metadata.pickle')

    def __generate_filepath(self) -> Path:
        return self.cache_dir.joinpath(f'{uuid4()}.pickle')

    def __read_pickle(self, file: Path):
        if not file.exists():
            return None

        with file.open('rb') as fp:
            return pickle.load(fp)

    def __write_pickle(self, file: Path, data: Any):
        with file.open('wb') as fp:
            pickle.dump(data, fp, pickle.HIGHEST_PROTOCOL)

    def get(
        self,
        key: str,
        action: Callable[[], str],
        expire_in: Optional[timedelta] = None
    ) -> CacheData:
        metadata = self.__read_pickle(file=self.metadata) or {}
        file: Path = metadata.get(key, None)

        def regenerate_value():
            value = action()

            self.set(key=key, value=value, expire_in=expire_in)
            return CacheData(value=value, valid=True)

        if file is None:
            return regenerate_value()

        if not file.exists() or not file.is_file():
            return regenerate_value()

        data: dict = self.__read_pickle(file=file)  # type:ignore
        value = data.get('value', False)
        valid = data.get('valid', False)
        expires = data.get('expires', None)

        if valid is False or value is None:
            return regenerate_value()

        actual_timestamp = datetime.now().timestamp()
        if expires is not None and expires <= actual_timestamp:
            return regenerate_value()

        return CacheData(value=value, valid=valid)

    def set(
        self,
        key: str,
        value: Any,
        expire_in: Optional[timedelta] = None
    ) -> CacheData:
        metadata = self.__read_pickle(file=self.metadata) or {}

        file = metadata.get(key, self.__generate_filepath())
        data = {
            'value':
                value,
            'valid':
                True,
            'expires':
                (datetime.now() + expire_in).timestamp() if expire_in else None
        }
        metadata[key] = data

        self.__write_pickle(file, data)
        self.__write_pickle(self.metadata, metadata)

        return CacheData(value=value, valid=True)

    def set_validate(self, key: str, valid: bool, silent: bool = True) -> None:
        metadata = self.__read_pickle(file=self.metadata) or {}

        file = metadata.get(key, None)
        if file is None and silent is False:
            raise ValueError("There's no cache with the provided key.")
