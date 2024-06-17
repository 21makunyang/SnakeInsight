from random_forest.data.pre_processor import PreProcessor
from snake_insight_threading.util import RedisCommand


class DataGenerator(object):
    __redis_pool = None

    def __init__(self, target_name, *args, **kwargs):
        if DataGenerator.__redis_pool is None:
            DataGenerator.__redis_pool = RedisCommand(**kwargs)
        self.__pattern = "广州:*"
        self.target_name = target_name
        self.pre_processor = PreProcessor(target_name=self.target_name)


    @classmethod
    def init_redis(cls, **kwargs):
        cls.__redis_pool = RedisCommand(**kwargs)

    @property
    def redis(self):
        return self.__redis_pool.redis

    def generate_data(self):
        cursor = "0"
        X = []
        y = []
        while cursor != 0:
            cursor, keys = self.redis.scan(cursor=cursor, match=self.__pattern, count=10_000, _type="HASH")
            with self.__redis_pool.pipeline(False) as pipeline:
                for key in keys:
                    pipeline.hgetall(name=key)
                data = pipeline.execute()
            for value in data:
                pre_processed_data, target = self.pre_processor.process(value)
                if not pre_processed_data:
                    continue
                X.append(pre_processed_data)
                y.append(target)

        return X, y