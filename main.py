from simple_cache import SimpleCache
from config import deta_key

cache = SimpleCache(deta_key=deta_key)
"""
OR

cache = SimpleCache()
cache.init(deta_key=deta_key)
"""

# -*-*-*

res = cache.get(key="/")
print(res)  # <CacheData value="..." valid=False>

# -*-*-*

res = cache.get(key="/")
print(res.valid)  # False

# -*-*-*

res = cache.get(key="/")
print(res.value)  # None

# -*-*-*

res = cache.set(key="/", value="<h1>Olá, Mundo!</h1>")

print(res.value)  # <h1>Olá, Mundo!</h1>
print(res.valid)  # True

# -*-*-*

cache.set_validate(key="/", valid=False)
res = cache.get(key="/")

print(res.value)  # <h1>Olá, Mundo!</h1>
print(res.valid)  # False
