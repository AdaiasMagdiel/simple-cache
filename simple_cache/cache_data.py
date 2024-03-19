from typing import Any


class CacheData:
    """
    A class representing cached data.

    Attributes:
        value (Any): The cached value.
        valid (bool): Indicates whether the cached value is valid.
    """
    def __init__(self, value: Any, valid: bool) -> None:
        """
        Initialize a CacheData instance with a value and a validity flag.

        Args:
            value (Any): The cached value.
            valid (bool): Indicates whether the cached value is valid.
        """
        self.value = value
        self.valid = valid

    def __repr__(self) -> str:
        """
        Return a string representation of the CacheData instance.

        Returns:
            str: A string representation of the CacheData instance.
        """
        return f'<CacheData value="..." valid="{self.valid}">'
