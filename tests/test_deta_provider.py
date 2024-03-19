import pytest
from simple_cache import SimpleCache
from config import deta_key
from uuid import uuid4
from datetime import timedelta
from time import sleep

from simple_cache.providers.deta import DetaProvider

provider = DetaProvider(deta_key=deta_key)
cache = SimpleCache(provider=provider)


def generate_content() -> str:
    return "content"


def test_initialize_class_and_post_initialize():
    provider = DetaProvider(deta_key=deta_key)
    cache = SimpleCache(provider=provider)
    assert cache.deta is not None

    provider = DetaProvider()
    cache = SimpleCache(provider=provider)
    assert not hasattr(cache, "deta")

    cache.init(deta_key=deta_key)
    assert cache.deta is not None


def test_initialize_class_and_post_initialize_with_valid_table_name():
    table_name = "table"

    provider = DetaProvider(deta_key=deta_key, table_name=table_name)
    cache = SimpleCache(provider=provider)
    assert cache.deta is not None
    assert cache.cache_table == table_name

    provider = DetaProvider()
    cache = SimpleCache(provider=provider)
    assert not hasattr(cache, "deta")
    assert cache.cache_table == "sc_cache"

    cache.init(deta_key=deta_key, table_name=table_name)
    assert cache.deta is not None
    assert cache.cache_table == table_name


def test_raise_exception_with_invalid_table_name():
    table_name = ""

    with pytest.raises(ValueError):
        provider = DetaProvider(deta_key=deta_key, table_name=table_name)
        cache = SimpleCache(provider=provider)

    with pytest.raises(ValueError):
        provider = DetaProvider()
        cache = SimpleCache(provider=provider)
        cache.init(deta_key=deta_key, table_name=table_name)


def test_raise_exception_with_invalid_deta_key():
    with pytest.raises(ValueError):
        provider = DetaProvider(deta_key="")
        cache = SimpleCache(provider=provider)

    with pytest.raises(ValueError):
        provider = DetaProvider()
        cache = SimpleCache(provider=provider)
        cache.init(deta_key=None)

    with pytest.raises(ValueError):
        provider = DetaProvider()
        cache = SimpleCache(provider=provider)
        cache.init(deta_key="")


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
