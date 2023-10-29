from typing import Any, TypedDict
from .queue import CircularQueue


class Cache:
    def __init__(self, capacity=50) -> None:
        self._cache: dict[str, Any] = {}
        self._count = 0
        self._capacity = capacity

    def __raise_not_implemented_error(self, method_name: str) -> None:
        raise NotImplementedError(
            f"Classes inheriting `Cache` class should implement `{method_name}` method"
        )

    def get(self, key: str) -> Any:
        self.__raise_not_implemented_error("get")

    def set(self, key: str, val: Any) -> None:
        self.__raise_not_implemented_error("set")

    def delete(self, key: str) -> None:
        self.__raise_not_implemented_error("delete")

    def is_full(self) -> bool:
        return self._count == self._capacity

    def is_empty(self) -> bool:
        return self._count == 0

    def get_capacity(self) -> int:
        return self._capacity


# Right now the meta only contains the frequency but can later have more keys like `last_accessed_at`
# which can help manage cache expiration / invalidations...
class CacheMeta(TypedDict):
    frequency: int


class FrequencyCache(Cache):
    def __init__(self, capacity=50) -> None:
        self.__frequency_buckets: list[CircularQueue] = []
        self.__cache_meta: dict[str, CacheMeta] = {}
        super().__init__(capacity)

    def __upsert_cache_meta_and_frequency_buckets(self, key: str) -> None:
        meta = self.__cache_meta.get(key, None)

        if meta is None:
            # New key is inserted
            if len(self.__frequency_buckets) == 0:
                self.__frequency_buckets.append(CircularQueue(self._capacity))

            self.__frequency_buckets[0].enqueue(key)
            self.__cache_meta[key] = {"frequency": 0}
            return

        self.__frequency_buckets[meta["frequency"]].delete(key)
        meta["frequency"] += 1

        if len(self.__frequency_buckets) <= meta["frequency"]:
            self.__frequency_buckets.append(CircularQueue(self._capacity))

        self.__frequency_buckets[meta["frequency"]].enqueue(key)

    def get(self, key: str) -> Any:
        value = self._cache.get(key, None)
        if value is not None:
            self.__upsert_cache_meta_and_frequency_buckets(key)
        return value

    def set(self, key: str, val: Any) -> Any:
        old_val = self._cache.get(key, None)

        if old_val is None and self.is_full():
            self.__delete_least_frequent()

        self._cache[key] = val
        self._count += 1

        if old_val is None:
            self.__upsert_cache_meta_and_frequency_buckets(key)

    def delete(self, key: str) -> None:
        meta = self.__cache_meta.get(key, None)
        if meta is None:
            return

        self.__frequency_buckets[meta["frequency"]].delete(key)
        self.__cache_meta.pop(key, None)
        self._cache.pop(key, None)
        self._count -= 1

    def __delete_least_frequent(self) -> None:
        index = 0

        while self.__frequency_buckets[index].is_empty():
            index += 1

        key = self.__frequency_buckets[index].peek()
        self.delete(key)
