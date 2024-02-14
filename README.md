# Simple Cache

[![PyPI version](https://badge.fury.io/py/mgdl-simple-cache.svg)](https://badge.fury.io/py/mgdl-simple-cache)
![License](https://img.shields.io/badge/license-MIT-blue)


Simple Cache is a lightweight cache manager designed to simplify caching operations using Deta Base. It offers a convenient way to store and retrieve cached data efficiently in Python applications.

## Installation

Install Simple Cache via pip:

```bash
pip install mgdl-simple-cache
```

## Purpose

In today's data-driven applications, caching plays a crucial role in enhancing performance by reducing the need to repeatedly fetch data from external sources. Simple Cache aims to streamline this process by providing a user-friendly interface for managing cached data, backed by Deta Base, a fast and scalable database service.

## Usage

To use `simple-cache`, you need to initialize an instance of the `SimpleCache` class. You can optionally provide a Deta Base key during initialization. If not provided during initialization, you can call the `init()` method later to set the Deta Base key.

```python
from simple_cache import SimpleCache

# Initialize SimpleCache
cache = SimpleCache("YOUR_DETA_PROJECT_KEY")
```

Or

```python
from simple_cache import SimpleCache

# Initialize SimpleCache
cache = SimpleCache()
cache.init("YOUR_DETA_PROJECT_KEY")
```

### Methods

#### `get(key: str) -> CacheData`

Retrieve cached data associated with the specified key.

- `key`: The key corresponding to the cached data.
- Returns a `CacheData` object containing the cached value and its validity status.

#### `set(key: str, value: Any) -> CacheData`

Store data in the cache under the given key.

- `key`: The key to associate with the cached data.
- `value`: The data to be cached.
- Returns a `CacheData` object representing the stored value and its validity status.

#### `set_validate(key: str, valid: bool, silent: bool = True) -> None`

Update the validity status of cached data.

- `key`: The key associated with the cached data.
- `valid`: A boolean value indicating whether the cached data is valid.
- `silent`: If True, suppress errors during the update process.
- Does not return any value.

## Documentation

### `CacheData`

A simple class representing cached data.

#### Attributes

- `value`: The cached value.
- `valid`: A boolean indicating whether the cached value is valid.

### `SimpleCache`

A class for managing cached data using Deta Base.

#### Attributes

- `cache_table`: The name of the table where cached data is stored, default `sc_cache`.
- `deta`: An instance of the Deta class.
- `cache_db`: An instance of the Deta Base class.

#### Methods

- `__init__(deta_key: Optional[str] = None)`: Initialize the SimpleCache instance.
- `init(deta_key: str)`: Initialize the SimpleCache instance with the Deta Base key.
- `get(key: str) -> CacheData`: Retrieve cached data.
- `set(key: str, value: Any) -> CacheData`: Store data in the cache.
- `set_validate(key: str, valid: bool, silent: bool = True) -> None`: Update the validity status of cached data.

## License

This project is licensed under the terms of the MIT license. See the [LICENSE](./LICENSE) file for details.

## Contribution

Contributions are welcome! Feel free to open issues or submit pull requests to enhance this project. Your feedback and contributions help make Simple Cache even better.
