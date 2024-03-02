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

To use the Simple Cache library, follow these steps:

1. **Choose a Provider**: Simple Cache provides different providers for storing cache data. See all available providers [here](#providers). Alternatively, you can implement your own provider by subclassing the `Provider` abstract class.

2. **Initialize the Provider**: Initialize the chosen provider with the necessary parameters. For example, if you are using the `DetaProvider`, you need to provide the Deta project key and optionally the table name:

```python
from simple_cache.providers import DetaProvider

provider = DetaProvider(deta_key="your_deta_project_key", table_name="cache_table")
```

Check the [providers section](#providers) to see the signature of all parameters that are available for each provider.

3. **Create a SimpleCache Instance**: Create an instance of `SimpleCache` by passing the initialized provider:

```python
from simple_cache import SimpleCache

cache = SimpleCache(provider)
```

5. **Usage**:

    - **Get Data**: To retrieve data from the cache, use the `get` method. If the data is not found in the cache or has expired, you can provide a callback function to generate the data and set it in the cache:

    ```python
    data = cache.get(key="some_key", action=some_function, expire_in=timedelta(minutes=5))
    ```

    - **Set Data**: To set data in the cache, use the `set` method. You can specify an optional expiration time for the data:

    ```python
    cache.set(key="some_key", value=some_value, expire_in=timedelta(hours=1))
    ```

    - **Set Data Validation**: You can mark data as valid or invalid in the cache using the `set_validate` method:

    ```python
    cache.set_validate(key="some_key", valid=True)
    ```

## Documentation

### SimpleCache

The `SimpleCache` class provides a simplified interface for interacting with cache providers. It acts as a wrapper around a specific cache provider instance. It includes methods to initialize the cache provider, retrieve data from the cache, set data in the cache, and mark data as valid or invalid.

-   `__init__(self, provider: Provider) -> None`: Initialize the SimpleCache instance with the specified cache provider.
-   `init(self, **kwargs)`: Initialize the cache provider with the given parameters.
-   `get(self, key: str, action: Callable[[], str], expire_in: Optional[timedelta] = None) -> CacheData`: Retrieve data from the cache with the specified key. If the data is not found or has expired, the provided action function is executed to generate the data.
-   `set(self, key: str, value: Any, expire_in: Optional[timedelta] = None) -> CacheData`: Set data in the cache with the specified key and value. Optionally, you can specify an expiration time for the data.
-   `set_validate(self, key: str, valid: bool, silent: bool = True) -> None`: Mark data in the cache as valid or invalid.

### Providers

#### Provider (ABC)

The `Provider` class is an abstract base class defining the interface for cache providers. It includes the following abstract methods:

-   `init(self, **kwargs)`: Initialize the provider with the given parameters. This method should be implemented by subclasses.
-   `get(self, key: str, action: Callable[[], str], expire_in: Optional[timedelta] = None) -> CacheData`: Retrieve data from the cache with the specified key. If the data is not found or has expired, the provided action function is executed to generate the data.
-   `set(self, key: str, value: Any, expire_in: Optional[timedelta] = None) -> CacheData`: Set data in the cache with the specified key and value. Optionally, you can specify an expiration time for the data.
-   `set_validate(self, key: str, valid: bool, silent: bool = True) -> None`: Mark data in the cache as valid or invalid.

#### DetaProvider

The `DetaProvider` class is a concrete implementation of the `Provider` interface that stores cache data in Deta databases. It includes methods to initialize the provider, retrieve data from the cache, set data in the cache, and mark data as valid or invalid.

-   `__init__(self, deta_key: Optional[str] = None, table_name: Optional[str] = None)`: Initialize the Deta provider with the specified Deta project key and table name.
-   `init(self, **kwargs) -> None`: Initialize the Deta provider with the given parameters. If no table name is provided, a default table name is used.
-   `get(self, key: str, action: Callable[[], str], expire_in: Optional[timedelta] = None) -> CacheData`: Retrieve data from the Deta cache with the specified key. If the data is not found or has expired, the provided action function is executed to generate the data.
-   `set(self, key: str, value: Any, expire_in: Optional[timedelta] = None) -> CacheData`: Set data in the Deta cache with the specified key and value. Optionally, you can specify an expiration time for the data.
-   `set_validate(self, key: str, valid: bool, silent: bool = True) -> None`: Mark data in the Deta cache as valid or invalid.

## Testing

If you wish to contribute to this project and run the tests, you will need to install `pytest` and run.

```bash
pip install pytest
```

```bash
pytest -vvsx # Increased verbosity, shows the stdout, breaks at the first failure
```

### Coverage

If you would like to include coverage, make sure to also install `pytest-cov`.

```bash
pip install pytest-cov
```

And run `pytest` command with the coverage options:

```bash
pytest --cov=simple_cache --cov-report=html -vvsx
```

## License

This project is licensed under the terms of the MIT license. See the [LICENSE](./LICENSE) file for details.

## Contribution

Contributions are welcome! Feel free to open issues or submit pull requests to enhance this project. Your feedback and contributions help make Simple Cache even better.
