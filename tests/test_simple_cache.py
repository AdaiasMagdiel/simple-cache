import pytest
from simple_cache import SimpleCache
from config import deta_key
from uuid import uuid4


def generate_content() -> str:
    return "content"


def test_initialize_class_and_post_initialize():
    cache = SimpleCache(deta_key=deta_key)
    assert cache.deta is not None

    cache = SimpleCache()
    assert not hasattr(cache, "deta")

    cache.init(deta_key=deta_key)
    assert cache.deta is not None


def test_initialize_class_and_post_initialize_with_valid_table_name():
    table_name = "table"

    cache = SimpleCache(deta_key=deta_key, table_name=table_name)
    assert cache.deta is not None
    assert cache.cache_table == table_name

    cache = SimpleCache()
    assert not hasattr(cache, "deta")
    assert cache.cache_table == "sc_cache"

    cache.init(deta_key=deta_key, table_name=table_name)
    assert cache.deta is not None
    assert cache.cache_table == table_name


def test_raise_exception_with_invalid_table_name():
    table_name = ""

    with pytest.raises(ValueError):
        SimpleCache(deta_key=deta_key, table_name=table_name)

    with pytest.raises(ValueError):
        cache = SimpleCache()
        cache.init(deta_key=deta_key, table_name=table_name)


def test_cache_with_action_value():
    cache = SimpleCache(deta_key=deta_key)
    key = str(uuid4())

    res = cache.get(key=key, action=generate_content)

    assert res.value == "content"
    assert res.valid is True


def test_insert_and_get_cache():
    cache = SimpleCache(deta_key=deta_key)
    key = str(uuid4())

    cache.set(key=key, value="value")
    res = cache.get(key=key, action=generate_content)

    assert res.value == "value"  # it's not "content" because cache already have value
    assert res.valid is True


def test_update_cache():
    cache = SimpleCache(deta_key=deta_key)
    key = str(uuid4())

    cache.set(key=key, value="value")
    cache.set(key=key, value="value2")
    res = cache.get(key=key, action=generate_content)

    assert res.value == "value2"
    assert res.valid is True


def test_invalidate_cache():
    cache = SimpleCache(deta_key=deta_key)
    key = str(uuid4())

    cache.set(key=key, value="value")
    res = cache.get(key=key, action=generate_content)

    assert res.value == "value"

    cache.set_validate(key=key, valid=False)
    res = cache.get(key=key, action=generate_content)

    assert res.value == "content"


def test_mixed_values():
    cache = SimpleCache(deta_key=deta_key)
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
    cache = SimpleCache(deta_key=deta_key)
    key = str(uuid4())

    large_value = "a" * 10000
    cache.set(key=key, value=large_value)
    res = cache.get(key=key, action=generate_content)

    assert res.value == large_value
    assert res.valid is True


def test_invalid_key():
    cache = SimpleCache(deta_key=deta_key)

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
    cache = SimpleCache(deta_key=deta_key)

    with pytest.raises(ValueError):
        cache.set_validate(key="this-key-not-exists", valid=False, silent=False)

    res = cache.set_validate(
        key="this-key-not-exists", valid=False, silent=True
    )
    assert res is None
