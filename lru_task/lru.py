from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int=10) -> None:
        self._capacity = capacity
        self._cache = OrderedDict()

    def _update_on_use(self, key):
        if key not in self._cache:
            return

        value = self._cache[key]

        self._cache.pop(key)

        self._cache[key] = value

    def get(self, key: str) -> str:
        if key not in self._cache:
            return ''

        self._update_on_use(key)

        return self._cache[key]

    def set(self, key: str, value: str) -> None:
        self._update_on_use(key)

        self._cache[key] = value

        if len(self._cache) > self._capacity:
            self._cache.popitem(last=False)

    def rem(self, key: str) -> None:
        self._cache.pop(key)