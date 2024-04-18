import time

from snake_insight_threading.util import RedisCommand


class Filter(object):
    redis = RedisCommand(host='10.242.91.125')
    city_infos = []
    last_area = ''

    def __init__(self, area=None):
        self.get_city_info_by_area(area)

    def get_city_info_by_area(self, area):
        if area is None:
            return self.city_infos
        if area == self.last_area:
            return self.city_infos
        self.city_infos = []
        house_info_keys = self.redis.smembers(area)

        # 使用pineline将指令一起发送可以从70秒降低到3秒
        with self.redis.pipeline(transaction=False) as p:
            for key in house_info_keys:
                p.hgetall(key)

            result = p.execute()
            for house_info in result:
                house_info_utf8 = {k.decode('utf8'): v.decode('utf8') for k, v in house_info.items()}
                house_info_utf8['tags'] = str(house_info_utf8.get('tags')[1:-1]).split(',')
                self.city_infos.append(house_info_utf8)
        return self.city_infos


if __name__ == "__main__":
    filter = Filter()
    start = time.time()
    res = filter.get_city_info_by_area('海珠')
    end = time.time()
    print(res)
    print('finished\ncost: {}'.format(str(end-start)))
