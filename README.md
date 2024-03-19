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

### Decorator `attach`

The `attach` decorator is a powerful feature of Simple Cache that allows you to store the result of a function in the cache, reducing the need to repeatedly execute the function. This is especially useful for operations that are time or resource-intensive, such as API calls or database queries.

#### How to Use

To use the `attach` decorator, you need to apply it to a function that you want to cache. Here's an example of how to do this:

```python
from datetime import timedelta
from simple_cache import SimpleCache
from simple_cache.providers import DetaProvider

# Initialize the cache provider
provider = DetaProvider(deta_key="your_deta_project_key", table_name="cache_table")
cache = SimpleCache(provider)

# Define a function that you want to cache
@cache.attach(key="my_function_result", expire_in=timedelta(minutes=5))
def my_function():
    # Simulate an operation that is time or resource-intensive
    result = "Result of the function"
    return result

# The first call to the function will store the result in the cache
print(my_function())

# Subsequent calls within the expiration time will use the cached result
print(my_function())
```

In this example, the function `my_function` is decorated with `@cache.attach`, which means that its result will be stored in the cache with the key `"my_function_result"` and will expire after 5 minutes. On the first call to the function, the result is calculated and stored in the cache. On subsequent calls within the expiration time, the cached result is returned, avoiding the need to recalculate the result.

#### Documentation

-   `attach(self, key: str, expire_in: Optional[timedelta] = None)`: Decorator to store the result of a function in the cache.
    -   `key (str)`: The unique key for the cache.
    -   `expire_in (Optional[timedelta])`: The expiration time for the cache.

This decorator is an efficient way to improve the performance of your Python applications, reducing the need for repetitive and resource-intensive operations.

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

If you wish to contribute to this project, simply install the development dependencies:

```bash
pip install -r requirements.dev.txt
```

And you need to rename the `config.py.example` to `config.py` and fill the `deta_key` var with a valid Deta Key:

> The `config.py` file is already in `.gitignore` so don't worry about exposing your key.

```python
# config.py
deta_key = "a0abcyxz_aSecretValue" # Change to a valid Deta Key
```

> I know I can use a `.env` for this, but I'm trying to make it as simple as possible to run the tests without an external dependency.

Finally, you can run this command to execute the tests:

```bash
pytest -vvsx # Increased verbosity, shows the stdout, breaks at the first failure
```

### Coverage

If you would like to include coverage, just run `pytest` command with the coverage options:

```bash
pytest --cov=simple_cache --cov-report=html -vvsx
```

## License

This project is licensed under the terms of the MIT license. See the [LICENSE](./LICENSE) file for details.

## Contribution

Contributions are welcome! Feel free to open issues or submit pull requests to enhance this project. Your feedback and contributions help make Simple Cache even better.
