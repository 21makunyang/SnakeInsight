import time

from snake_insight_threading.util import RedisCommand


class Divider(object):
    redis = RedisCommand(db=1)
    city_infos = []
    last_area = ''

    def divide_by_area(self):

        house_info_keys = self.redis.scan(match=None, count=10000, _type='HASH')
        index = 0
        for key in house_info_keys:
            # print(self.redis.hget(key))
            index += 1
            print(index)
            house_info = self.redis.hget(key)
            self.redis.sadd(house_info.get(b'area').decode('utf8'), key)

    def divide_by_region(self):

        house_info_keys = self.redis.scan(match=None, count=10000, _type='HASH')
        index = 0
        for key in house_info_keys:
            # print(self.redis.hget(key))
            index += 1
            print(index)
            house_info = self.redis.hgetall(key)
            self.redis.sadd(house_info.get(b'region').decode('utf8'), key)



if __name__ == "__main__":
    area = Divider()
    start = time.time()
    print(area.divide_by_region())
    # time.sleep(1)
    end = time.time()
    print('finished\ncost: {}'.format(str(end-start)))
