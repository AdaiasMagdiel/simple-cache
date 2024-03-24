# Changelog

All notable changes to this project will be documented in this file.

## [v1.2.0] - 2024-03-23

### Added

- Added `pytest-cov` to dev dependencies in `pyproject.toml`.
- Introduced a new `FileProvider` in the `simple_cache.providers` module.

### Changed

- Updated the `__init__.py` file to set the version to `1.2.0`.
- Modified the `SimpleCache` class in `__init__.py` to accept only a valid `Provider`.
- Changed the `init` method of the `FileProvider` class to have a return type of `None`.
- Updated the `Provider` abstract class in `provider.py` to include a return type of `None` for the `init` method.

### Removed

- Removed redundant code related to the initialization of the `FileProvider`.
- Deleted unnecessary comments and unused imports in the codebase.
- Eliminated redundant code in test files.

[v1.2.0]: https://github.com/AdaiasMagdiel/simple-cache/compare/v1.1.2...v1.2.0

## [v1.1.2] - 2024-03-21

### Changed

- Updated the package version from 1.1.1 to 1.1.2 in the `__init__.py` file.
- Modified the `__init__` method in the `SimpleCache` class to accept an optional `provider` parameter.

[v1.1.2]: https://github.com/AdaiasMagdiel/simple-cache/compare/v1.1.1...v1.1.2

## [v1.1.1] - 2024-03-19

### Added

- Development dependencies installation instructions to contribute to the project.
- `config.py.example` file to showcase how to set up Deta key.
- Instructions on how to run tests using the `pytest` command.
- A coverage section detailing how to include coverage in tests.

### Changed

- Updated the project version from `1.1.0` to `1.1.1`.
- Modified the `simple_cache/__init__.py` file to return the actual value from the cache instead of the whole cache object when calling `function()`.

### Removed

- The need to manually install `pytest`.
- `config.py` file content from the repository. It is now provided as an example only.

[v1.1.1]: https://github.com/AdaiasMagdiel/simple-cache/compare/v1.1.0...v1.1.1

## [v1.1.0] - 2024-03-19

### Added

- Added `attach` decorator feature that stores the result of a function in the cache, reducing repetitive executions.
- Included `DetaProvider` class for caching using Deta databases.
- Added `requirements.dev.txt` and `test.bat` for development requirements and testing script.
- Updated `description` in `pyproject.toml` to mention the support for providers.
- Created `cache_data.py` to represent cached data as a class.
- Implemented mocks and tests for the `attach` decorator, `DetaProvider`, and basic cache operations.

### Changed

- Removed `main.py` as it is no longer needed for the library.
- Modified `README.md` to include the detailed usage of the Simple Cache library.

### Removed

- Deleted unused files such as `.gitignore` entries and the `tests/test_simple_cache.py` script.

[v1.1.0]: https://github.com/AdaiasMagdiel/simple-cache/compare/v0.0.1...v1.1.0
