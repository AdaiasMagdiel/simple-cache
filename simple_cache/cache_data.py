from typing import Any


class CacheData:
    def __init__(self, value: Any, valid: bool) -> None:
        self.value = value
        self.valid = valid

    def __repr__(self) -> str:
        return f'<CacheData value="..." valid="{self.valid}">'
