from simple_cache import SimpleCache
from config import deta_key

cache = SimpleCache(deta_key=deta_key)
"""
OR

cache = SimpleCache()
cache.init(deta_key=deta_key)
"""

# -*-*-*


def generate_content() -> str:
    return "content"


# -*-*-*

res = cache.get(key="/", action=generate_content)
print(res)  # <CacheData value="content" valid=True>

# -*-*-*

res = cache.get(key="/", action=generate_content)
print(res.valid)  # True

# -*-*-*

res = cache.get(key="/", action=generate_content)
print(res.value)  # content

# -*-*-*

res = cache.set(key="/", value="<h1>Olá, Mundo!</h1>")

print(res.value)  # <h1>Olá, Mundo!</h1>
print(res.valid)  # True

# -*-*-*

cache.set_validate(key="/", valid=False)
res = cache.get(key="/", action=generate_content)

print(res.value)  # content
print(res.valid)  # True
