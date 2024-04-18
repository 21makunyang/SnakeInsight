import time

from snake_insight_threading.util import RedisCommand


class Divider(object):
    redis = RedisCommand(host='10.242.91.125')
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


if __name__ == "__main__":
    area = Divider()
    start = time.time()
    print(area.divide_by_area())
    # time.sleep(1)
    end = time.time()
    print('finished\ncost: {}', str(end-start))
