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
