import redis

from snake_insight_threading.classes import HouseInfo


class RedisCommand(object):
    def __init__(self, *, host='localhost', port=6379, db=0):
        self.__pool = redis.ConnectionPool(host=host, port=port, db=db, protocol=3)

    @property
    def redis(self):
        return redis.Redis(connection_pool=self.__pool)

    def hset(self, info: HouseInfo):
        self.redis.hset(name=info.id, mapping=info.__dict__)

    def hget(self, id_):
        return self.redis.hgetall(id_)

    def hscan(self, name: bytes | str | memoryview, cursor: int = 0, patten: bytes | str | memoryview | None = None,
              count: int | None = None):
        return self.redis.hscan(name, cursor, patten, count)

    def scan(self,
             cursor: int = 0,
             match: bytes | str | memoryview | None = None,
             count: int | None = None,
             _type: str | None = None):
        """
        参数：
        match - 匹配的模式。用于筛选过滤 key。(对元素的模式匹配工作是在命令从数据集中取出元素之后， 向客户端返回元素之前的这段时间内进行的， 所以如果被迭代的数据集中只有少量元素和模式相匹配， 那么迭代命令或许会在多次执行中都不返回任何元素。)
        count - 指定查询元素数量，默认值为 10。（count 不是限定返回结果的数量，而是限定服务器单次遍历的字典槽位数量，所以返回数量可能因为 pattern 过滤而返回少于 count）
        _type - 按特定的Redis类型过滤返回的值。 Redis实例允许的类型：HASH，LIST，SET，STREAM，STRING，ZSET。

        """
        return self.redis.scan_iter(match, count, _type)
