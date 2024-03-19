from datetime import timedelta
import time
from simple_cache import SimpleCache
from tests.mocks import MockProvider

provider = MockProvider()
cache = SimpleCache(provider=provider)


def test_decoraton_can_set_cache():
    inc = 1

    @cache.attach(key="key")
    def function():
        return f"Value: {inc}"

    res1 = function()
    inc += 1
    res2 = function()

    assert res1 == "Value: 1"
    assert res2 == "Value: 1"


def test_decoraton_can_set_cache_with_expiration():
    inc = 2

    @cache.attach(key="key_2", expire_in=timedelta(seconds=1))
    def function():
        return f"Value: {inc}"

    res1 = function()

    inc += 1
    time.sleep(5)

    res2 = function()
    res3 = function()

    assert res1 == "Value: 2"
    assert res2 == "Value: 3"
    assert res3 == "Value: 3"
