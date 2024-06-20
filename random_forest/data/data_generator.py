import numpy as np

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

        # # 下四分位数
        # X_lower_25 = np.percentile(X, 25, axis=0)
        # Y_lower_25 = np.percentile(y, 25)
        # # 上四分位数
        # X_upper_75 = np.percentile(X, 75, axis=0)
        # Y_upper_75 = np.percentile(y, 75)
        # print(X_lower_25, Y_lower_25, X_upper_75, Y_upper_75)

        # new_X = []
        # new_y = []
        # for i in range(len(X)):
        #     accept = True
        #     if X[i][5] < X_lower_25[5]:
        #         accept = False
        #         X[i][5] = X_lower_25[5]
        #     elif X[i][5] > X_upper_75[5]:
        #         accept = False
        #         X[i][5] = X_upper_75[5]
        #     # for j in range(len(X[i])):
        #     #     if X[i][j] < X_lower_25[j]:
        #     #         X[i][j] = X_lower_25[j]
        #     #         accept = False
        #     #     elif X[i][j] > X_upper_75[j]:
        #     #         accept = False
        #     #         X[i][j] = X_upper_75[j]
        #     if y[i] < Y_lower_25:
        #         accept = False
        #         y[i] = Y_lower_25
        #     elif y[i] > Y_upper_75:
        #         accept = False
        #         y[i] = Y_upper_75
        #     # if accept:
        #     #     new_X.append(X[i])
        #     #     new_y.append(y[i])

        return X, y