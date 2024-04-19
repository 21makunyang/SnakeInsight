import time
import numpy as np
from snake_insight_threading.util import RedisCommand


class Filter(object):
    redis = RedisCommand(host='10.242.91.125')
    city_infos = []
    last_area = ''

    def __init__(self, area=None):
        self.get_city_info_by_area(area)

    def get_city_info_by_area(self, area):
        if area is None or area == self.last_area:
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

        self.last_area = area
        return self.city_infos

    def get_room_price(self, area):
        self.get_city_info_by_area(area)

        # key为living_room和bedroom构成的元组，value为列表，分别为平均价 最高价 最低价 统计数量
        statisticians_result = {}

        for house_info in self.city_infos:
            living_room = house_info.get('living_room')
            bedroom = house_info.get('bedroom')
            price = float(house_info.get('price'))

            statisticians = statisticians_result.get((living_room, bedroom),[0, price, price, 0])
            statisticians[0] += price
            statisticians[1] = max(statisticians[1], price)
            statisticians[2] = min(statisticians[2], price)
            statisticians[3] += 1
            statisticians_result[(living_room, bedroom)] = statisticians

        for k in statisticians_result:
            statisticians_result[k][0] = statisticians_result[k][0]/statisticians_result[k][3]

        return statisticians_result


if __name__ == "__main__":
    filter = Filter()
    start = time.time()
    res = filter.get_room_price('海珠')
    end = time.time()
    print(res)
    print('finished\ncost: {}'.format(str(end - start)))
