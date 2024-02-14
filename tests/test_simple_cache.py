import pytest
from simple_cache import SimpleCache
from config import deta_key


def test_initialize_class_and_post_initialize():
    cache = SimpleCache(deta_key=deta_key)
    assert cache.deta is not None

    cache = SimpleCache()
    assert not hasattr(cache, "deta")

    cache.init(deta_key=deta_key)
    assert cache.deta is not None


def test_insert_and_get_cache():
    cache = SimpleCache(deta_key=deta_key)

    cache.set(key="/", value="value")
    res = cache.get(key="/")

    assert res.value == "value"
    assert res.valid is True


def test_update_cache():
    cache = SimpleCache(deta_key=deta_key)

    cache.set(key="/", value="value")
    cache.set(key="/", value="value2")
    res = cache.get(key="/")

    assert res.value == "value2"
    assert res.valid is True


def test_invalidate_cache():
    cache = SimpleCache(deta_key=deta_key)

    cache.set(key="/", value="value")
    res = cache.get(key="/")

    assert res.valid is True

    cache.set_validate(key="/", valid=False)
    res = cache.get(key="/")

    assert res.valid is False


def test_invalid_key_returns_none():
    cache = SimpleCache(deta_key=deta_key)

    res = cache.get(key="not-exists")
    assert res.value is None
    assert res.valid is False


def test_mixed_values():
    cache = SimpleCache(deta_key=deta_key)

    cache.set(key="/", value=None)
    res = cache.get(key="/")

    assert res.value is None
    assert res.valid is True

    cache.set(key="/", value={"panic": 42})
    res = cache.get(key="/")

    assert res.value == {"panic": 42}
    assert res.valid is True

    cache.set(key="/", value=42)
    res = cache.get(key="/")

    assert res.value == 42
    assert res.valid is True

    cache.set(key="/", value=False)
    res = cache.get(key="/")

    assert res.value is False
    assert res.valid is True


def test_large_value():
    cache = SimpleCache(deta_key=deta_key)

    large_value = "a" * 10000
    cache.set(key="/large", value=large_value)
    res = cache.get(key="/large")

    assert res.value == large_value
    assert res.valid is True


def test_invalid_key():
    cache = SimpleCache(deta_key=deta_key)

    with pytest.raises(ValueError):
        cache.set(key="", value="value")

    with pytest.raises(ValueError):
        cache.set(key=None, value="value")

    with pytest.raises(ValueError):
        cache.get(key="")

    with pytest.raises(ValueError):
        cache.get(key=None)

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
