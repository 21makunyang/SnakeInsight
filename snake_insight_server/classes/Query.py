from typing import Iterator

from snake_insight_threading.util import RedisCommand


class Query(object):
    __redis_pool = None

    def __init__(self, *args, **kwargs):
        if Query.__redis_pool is None:
            Query.__redis_pool = RedisCommand(**kwargs)
        self.__path = list(args)
        self.__pattern = ":".join(self.__path) + "*"

    @classmethod
    def init_redis(cls, **kwargs):
        cls.__redis_pool = RedisCommand(**kwargs)

    @property
    def redis(self):
        return self.__redis_pool.redis

    def fetch(self, *, exclude_field: list[str] = None, auto_convert: bool = True) -> Iterator:
        for keys in self.batch:
            with self.__redis_pool.pipeline(False) as pipeline:
                for key in keys:
                    pipeline.hgetall(name=key)
                result = pipeline.execute()

            for value in result:
                hash_object = {}
                for hash_field, hash_value in value.items():
                    if hash_field.decode() not in exclude_field:
                        if auto_convert:
                            try:
                                hash_object[hash_field.decode()] = float(hash_value.decode())
                            except Exception:
                                hash_object[hash_field.decode()] = hash_value.decode()
                        else:
                            hash_object[hash_field.decode()] = hash_value.decode()
                yield hash_object

    @property
    def batch(self):
        cursor = "0"
        while cursor != 0:
            cursor, data = self.redis.scan(cursor=cursor, match=self.__pattern, count=10_000, _type="HASH")
            yield data

    def __iter__(self):
        return self.redis.scan_iter(self.__pattern, 10_000, "HASH")
