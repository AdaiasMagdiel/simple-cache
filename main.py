from simple_cache import SimpleCache
from simple_cache.providers import DetaProvider
from config import deta_key

provider = DetaProvider(deta_key=deta_key)
cache = SimpleCache(provider=provider)

cache.set(key="/", value="Value")
