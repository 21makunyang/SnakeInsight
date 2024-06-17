from random_forest.data.pre_processor import PreProcessor
from snake_insight_threading.util import RedisCommand


class DataGenerator(object):
    redis = RedisCommand(db=1)

    def __init__(self):
        self.__pattern = "广州:*"
        self.pre_processor = PreProcessor()

    def generate_data(self):
        cursor = "0"
        X = []
        y = []
        while cursor != 0:
            cursor, data = self.redis.scan(cursor=cursor, match=self.__pattern, count=10_000, _type="HASH")
            for key, value in data.items():
                pre_processed_data, target = self.pre_processor.process(value)
                if not pre_processed_data:
                    continue
                X.append(pre_processed_data)
                y.append(target)

        return X, y