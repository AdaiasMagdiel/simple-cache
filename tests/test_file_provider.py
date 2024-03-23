import pytest
import tempfile
import shutil
from pathlib import Path
from simple_cache import SimpleCache
from datetime import timedelta
from time import sleep
from uuid import uuid4

from simple_cache.providers import FileProvider

temp_dir = tempfile.TemporaryDirectory()
provider = FileProvider(cache_dir=Path(temp_dir.name))
cache = SimpleCache(provider=provider)


@pytest.fixture(scope='session', autouse=True)
def teardown():
    yield
    temp_dir.cleanup()


def generate_content() -> str:
    return "content"


def test_initialize_class_and_post_initialize():
    with tempfile.TemporaryDirectory() as tmpdirname:
        provider = FileProvider(cache_dir=Path(tmpdirname))
        cache = SimpleCache(provider=provider)
        assert cache.provider is not None

        provider = FileProvider()
        cache = SimpleCache(provider=provider)

        cache.init(cache_dir=Path(tmpdirname))
        assert provider.cache_dir is not None


def test_try_to_create_cache_dir():
    provider = FileProvider(cache_dir=".temp-cache-dir")
    cache = SimpleCache(provider=provider)
    assert cache.provider is not None
    shutil.rmtree(".temp-cache-dir")

    with pytest.raises(ValueError):
        provider = FileProvider(cache_dir=object())  # type:ignore
        cache = SimpleCache(provider=provider)

    with pytest.raises(ValueError):
        provider = FileProvider(cache_dir=False)  # type:ignore
        cache = SimpleCache(provider=provider)

    with pytest.raises(ValueError):
        provider = FileProvider(cache_dir=7)  # type:ignore
        cache = SimpleCache(provider=provider)

    with pytest.raises(ValueError):
        provider = FileProvider(cache_dir=[1, 2, 3])  # type:ignore
        cache = SimpleCache(provider=provider)

    with pytest.raises(NotADirectoryError):
        provider = FileProvider(cache_dir='README.md')  # type:ignore
        cache = SimpleCache(provider=provider)


def test_raise_exception_with_invalid_cache_dir():
    with pytest.raises(ValueError):
        provider = FileProvider(cache_dir="")
        cache = SimpleCache(provider=provider)

    with pytest.raises(ValueError):
        provider = FileProvider(cache_dir="/this/is/valid/only/with/pathlib")
        cache = SimpleCache(provider=provider)

    with pytest.raises(ValueError):
        provider = FileProvider(cache_dir="*invalid-path>")
        cache = SimpleCache(provider=provider)

    with pytest.raises(ValueError):
        provider = FileProvider()
        cache = SimpleCache(provider=provider)
        cache.init(cache_dir="")

    with pytest.raises(ValueError):
        provider = FileProvider()
        cache = SimpleCache(provider=provider)
        cache.init(cache_dir="/this/is/valid/only/with/pathlib")

    with pytest.raises(ValueError):
        provider = FileProvider()
        cache = SimpleCache(provider=provider)
        cache.init(cache_dir="*invalid-path>")


def test_cache_with_action_value():
    key = str(uuid4())

    res = cache.get(key=key, action=generate_content)

    assert res.value == "content"
    assert res.valid is True


def test_insert_and_get_cache():
    key = str(uuid4())

    cache.set(key=key, value="value")
    res = cache.get(key=key, action=generate_content)

    assert res.value == "value"  # it's not "content" because cache already have value
    assert res.valid is True


def test_update_cache():
    key = str(uuid4())

    cache.set(key=key, value="value")
    cache.set(key=key, value="value2")
    res = cache.get(key=key, action=generate_content)

    assert res.value == "value2"
    assert res.valid is True


def test_invalidate_cache():
    key = str(uuid4())

    cache.set(key=key, value="value")
    res = cache.get(key=key, action=generate_content)

    assert res.value == "value"

    cache.set_validate(key=key, valid=False)
    res = cache.get(key=key, action=generate_content)

    assert res.value == "content"


def test_mixed_values():
    key = str(uuid4())

    cache.set(key=key, value={"panic": 42})
    res = cache.get(key=key, action=generate_content)

    assert res.value == {"panic": 42}
    assert res.valid is True

    cache.set(key=key, value=42)
    res = cache.get(key=key, action=generate_content)

    assert res.value == 42
    assert res.valid is True

    cache.set(key=key, value=False)
    res = cache.get(key=key, action=generate_content)

    assert res.value is False
    assert res.valid is True


def test_large_value():
    key = str(uuid4())

    large_value = "a" * 10000
    cache.set(key=key, value=large_value)
    res = cache.get(key=key, action=generate_content)

    assert res.value == large_value
    assert res.valid is True


def test_invalid_key():
    with pytest.raises(ValueError):
        cache.set(key="", value="value")

    with pytest.raises(ValueError):
        cache.set(key=None, value="value")

    with pytest.raises(ValueError):
        cache.get(key="", action=generate_content)

    with pytest.raises(ValueError):
        cache.get(key=None, action=generate_content)

    with pytest.raises(ValueError):
        cache.set_validate(key="", valid=False)

    with pytest.raises(ValueError):
        cache.set_validate(key=None, valid=False)


def test_set_validate_to_non_existing_key():
    with pytest.raises(ValueError):
        cache.set_validate(key="this-key-not-exists", valid=False, silent=False)

    res = cache.set_validate(
        key="this-key-not-exists", valid=False, silent=True
    )
    assert res is None


def test_set_cache_with_expiry():
    key = str(uuid4())

    def action():
        return str(uuid4())

    res = cache.get(key=key, action=action, expire_in=timedelta(seconds=2))
    value = res.value

    # Wait for the cache to expire
    sleep(3)

    # Ensure that the cache has expired
    res_expired = cache.get(
        key=key, action=action, expire_in=timedelta(seconds=2)
    )
    assert res_expired.value != value


def test_set_cache_with_expiry_and_regenerate_without_expiry():
    key = str(uuid4())

    def action():
        return str(uuid4())

    res = cache.get(key=key, action=action, expire_in=timedelta(seconds=2))
    value = res.value

    sleep(3)

    res_expired = cache.get(key=key, action=action)
    assert res_expired.value != value
    value = res_expired.value

    sleep(1)

    res_expired = cache.get(key=key, action=action)
    assert res_expired.value == value


def test_invalid_expire_in_type_in_set():
    key = str(uuid4())

    with pytest.raises(TypeError):
        cache.set(
            key=key,
            value="value",
            expire_in="invalid_type"  # type:ignore
        )

    with pytest.raises(TypeError):
        cache.set(key=key, value="value", expire_in=[1, 2, 3])  # type:ignore

    with pytest.raises(TypeError):
        cache.set(
            key=key,
            value="value",
            expire_in={"key": "value"}  # type:ignore
        )

    with pytest.raises(TypeError):
        cache.set(key=key, value="value", expire_in=(1,))  # type:ignore

    with pytest.raises(TypeError):
        cache.set(key=key, value="value", expire_in=True)  # type:ignore

    with pytest.raises(TypeError):
        cache.set(key=key, value="value", expire_in=1 + 2j)  # type:ignore

    with pytest.raises(TypeError):
        cache.set(key=key, value="value", expire_in=object())  # type:ignore


def test_invalid_expire_in_type_in_get():
    key = str(uuid4())

    def action():
        return ''

    with pytest.raises(TypeError):
        cache.get(
            key=key,
            action=action,
            expire_in="invalid_type"  # type:ignore
        )

    with pytest.raises(TypeError):
        cache.get(key=key, action=action, expire_in=[1, 2, 3])  # type:ignore

    with pytest.raises(TypeError):
        cache.get(
            key=key,
            action=action,
            expire_in={"key": "value"}  # type:ignore
        )

    with pytest.raises(TypeError):
        cache.get(key=key, action=action, expire_in=(1,))  # type:ignore

    with pytest.raises(TypeError):
        cache.get(key=key, action=action, expire_in=True)  # type:ignore

    with pytest.raises(TypeError):
        cache.get(key=key, action=action, expire_in=1 + 2j)  # type:ignore

    with pytest.raises(TypeError):
        cache.get(key=key, action=action, expire_in=object())  # type:ignore
