import math
import re
import time

from snake_insight_threading.common import PredictByType
from snake_insight_threading.util import RedisCommand


class Filter(object):
    # redis = RedisCommand(host='10.242.91.125')
    redis = RedisCommand(db=1)
    city_infos = []
    last_region = ''
    predict_base = {}
    def __init__(self, region=None):
        self.get_city_info_by_area(region)
        # self.app = Flask(__name__)
    def __init_before_process(self, region=None):
        if region is None:
            region = self.last_region

        self.get_city_info_by_area(region)

    def get_city_info_by_area(self, region):
        if region is None or region == self.last_region:
            return self.city_infos

        self.city_infos = []
        house_info_keys = self.redis.smembers(region)

        # 使用pineline将指令一起发送可以从70秒降低到3秒
        with self.redis.pipeline(transaction=False) as p:
            for key in house_info_keys:
                p.hgetall(key)

            result = p.execute()
            for house_info in result:
                # 转为utf-8编码
                house_info_utf8 = {k.decode('utf8'): v.decode('utf8') for k, v in house_info.items()}
                # 将tags的值转为列表
                house_info_utf8['tags'] = str(house_info_utf8.get('tags')[1:-1]).split(',')
                house_info_utf8['has_elevator'] = False

                # 对tags进行遍历，去掉多余的单引号，判断是否有电梯
                for i, tag in enumerate(house_info_utf8['tags']):
                    sub_tag = re.search(r"('(.*)?')", tag).group(2)

                    if sub_tag == '有电梯':
                        house_info_utf8['has_elevator'] = True

                    house_info_utf8['tags'][i] = sub_tag

                self.city_infos.append(house_info_utf8)

        self.last_region = region
        return self.city_infos

    def get_room_price(self, region=None):
        """
        厅室数量-价格
        """
        self.__init_before_process(region)

        # key为living_room和bedroom构成的元组，value为列表，分别为平均价 最高价 最低价 统计数量
        # 例如： {
        #        ('1', '3'): [4342.133555926544, 14800.0, 990.0, 599],
        #        ('2', '2'): [5055.043143297381, 16500.0, 1900.0, 1298],
        #        ...
        #       }
        statisticians_result = {}

        for house_info in self.city_infos:
            living_room = house_info.get('living_room')
            bedroom = house_info.get('bedroom')
            price = float(house_info.get('price'))

            statisticians = statisticians_result.get((living_room, bedroom), [0, price, price, 0])
            statisticians[0] += price
            statisticians[1] = max(statisticians[1], price)
            statisticians[2] = min(statisticians[2], price)
            statisticians[3] += 1
            statisticians_result[(living_room, bedroom)] = statisticians

        # 计算平均价格
        for k in statisticians_result:
            statisticians_result[k][0] = statisticians_result[k][0] / statisticians_result[k][3]

        return statisticians_result

    def get_floor_price(self, require_elevator=False,region=None):
        """
        （有无电梯）楼层——每平方米价格（柱状图）
        """
        self.__init_before_process(region)

        statisticians_result = {}

        for house_info in self.city_infos:
            floor = house_info.get('floor')
            if floor is None or floor == '':
                continue
            has_elevator = house_info.get('has_elevator')
            if (require_elevator and not has_elevator) or (not require_elevator and has_elevator):
                continue
            price = float(house_info.get('price'))
            space = float(house_info.get('space'))
            price_per_square = price / space

            level_dic = {'低': 1 / 6, '中': 1 / 2, '高': 5 / 6}
            level = level_dic.get(floor[0], 0.0)

            total = re.search(r'共([0-9]+)层', floor)
            if total is None:
                continue
            else:
                total = float(total.group(1))
            floor = math.ceil(total * level)
            # key为floor(int)构成的元组，value为列表，分别为平均每平方米价格 最高每平方米价格 最低每平方米价格 统计数量
            # 例如：{
            #       (7,): [69.90145372704634, 275.0, 21.59709618874773, 244],
            #       (38,): [78.95237587138996, 107.98122065727699, 60.60606060606061, 4],
            #       ...
            #      }
            tuple_k = (floor,)
            statisticians = statisticians_result.get(tuple_k, [0, price_per_square, price_per_square, 0])
            statisticians[0] += price_per_square
            statisticians[1] = max(price_per_square, statisticians[1])
            statisticians[2] = min(price_per_square, statisticians[2])
            statisticians[3] += 1

            statisticians_result[tuple_k] = statisticians

        # 计算平均价格
        for k in statisticians_result:
            statisticians_result[k][0] = statisticians_result[k][0] / statisticians_result[k][3]

        return statisticians_result

    def get_space_price_per_square(self, region=None):
        """
        面积-每平方米价格
        """
        self.__init_before_process(region)

        statisticians_result = {}

        for house_info in self.city_infos:
            space = float(house_info.get('space'))
            price = float(house_info.get('price'))
            price_per_square = price / space

            tuple_k = ('{:.2f}'.format(space),)
            # key为space(2位小数)构成的元组，value为列表，分别为平均每平方米价格 最高每平方米价格 最低每平方米价格 统计数量
            # 例如：{
            #       ('28.00',): [53.022921108742004, 100.0, 24.571428571428573, 134],
            #       ('60.00',): [57.494411177644714, 108.33333333333333, 16.666666666666668, 167],
            #       ...
            #      }
            statisticians = statisticians_result.get(tuple_k, [0, price_per_square, price_per_square, 0])
            statisticians[0] += price_per_square
            statisticians[1] = max(price_per_square, statisticians[1])
            statisticians[2] = min(price_per_square, statisticians[2])
            statisticians[3] += 1

            statisticians_result[tuple_k] = statisticians

        # 计算平均价格
        for k in statisticians_result:
            statisticians_result[k][0] = statisticians_result[k][0] / statisticians_result[k][3]

        return statisticians_result

    def get_area_price(self, region=None):
        """
        区域各地段平均价格
        """
        self.__init_before_process(region)
        statisticians_result = {}

        for house_info in self.city_infos:
            area = house_info.get('area')
            price = float(house_info.get('price'))
            tuple_k = (area,)
            statisticians = statisticians_result.get(tuple_k, [0, price, price, 0])
            statisticians[0] += price
            statisticians[1] = max(price, statisticians[1])
            statisticians[2] = min(price, statisticians[2])
            statisticians[3] += 1

            statisticians_result[tuple_k] = statisticians

        # 计算平均价格
        for k in statisticians_result:
            statisticians_result[k][0] = statisticians_result[k][0] / statisticians_result[k][3]

        return statisticians_result

    def get_distribution_by_area(self, region):
        self.__init_before_process(region)
        statisticians_result = {}

        for house_info in self.city_infos:
            area = house_info.get('area')

            tuple_k = (area,)
            statisticians_result[tuple_k] = statisticians_result.get(tuple_k, [0])[0] + 1

        return statisticians_result

    def get_neighborhood_price(self, region):
        self.__init_before_process(region)
        statisticians_result = {}

        for house_info in self.city_infos:
            raw = house_info.get('raw')
            space = float(house_info.get('space'))
            price = float(house_info.get('price'))
            price_per_square = price / space
            print('*************************')
            print(raw)

        return

    def get_predict_base(self, region):
        if self.predict_base and (region is None or region == self.last_region):
            return self.predict_base
        self.__init_before_process(region)
        self.predict_base = {}

        for house_info in self.city_infos:
            floor = house_info.get('floor')
            if floor is None or floor == '':
                continue
            area_ = region
            area_ += house_info.get('area', '')
            has_elevator = house_info.get('has_elevator')
            living_room = house_info.get('living_room')
            bedroom = house_info.get('bedroom')
            space_ = float(house_info.get('space'))

            price_ = float(house_info.get('price'))
            price_per_square = price_ / space_

            level_dic = {'低': 1 / 6, '中': 1 / 2, '高': 5 / 6}
            level = level_dic.get(floor[0], 0.0)

            total = re.search(r'共([0-9]+)层', floor)
            if total is None:
                continue
            else:
                total = float(total.group(1))
            floor = math.ceil(total * level)

            tuple_k = (area_, floor, has_elevator, living_room, bedroom)
            statisticians = self.predict_base.get(tuple_k, [0, price_per_square, price_per_square, 0])
            statisticians[0] += price_per_square
            statisticians[1] = max(price_per_square, statisticians[1])
            statisticians[2] = min(price_per_square, statisticians[2])
            statisticians[3] += 1

            self.predict_base[tuple_k] = statisticians

        # 计算平均价格
        for k in self.predict_base:
            self.predict_base[k][0] = self.predict_base[k][0] / self.predict_base[k][3]

        return self.predict_base

    def predict_price(self, area, floor, has_elevator, living_room, bedroom, space):
        return self.predict_base.get((area, floor, has_elevator, living_room, bedroom), -1) * space

    def predict_space(self, area, floor, has_elevator, living_room, bedroom, price):
        return price / self.predict_base.get((area, floor, has_elevator, living_room, bedroom), -1)

    def predict(self, region, area, floor, has_elevator, living_room, bedroom, predict_by_type: PredictByType, value):
        self.get_predict_base(region)
        result = -1
        if predict_by_type == PredictByType.PRICE.value:
            result = self.predict_space(area, floor, has_elevator, living_room, bedroom, value)
        else:
            result = self.predict_price(area, floor, has_elevator, living_room, bedroom, value)

        return result

    def get_region_price(self, region):
        self.__init_before_process(region)

        price_list = [float(info.get('price')) for info in self.city_infos if info.get('price') is not None]
        return sum(price_list) / len(price_list)



if __name__ == "__main__":
    region_list = ['海珠', '从化', '南沙', '增城', '天河', '广州周边', '番禺', '白云', '花都', '荔湾',
                   '越秀', '黄埔']
    filter = Filter()
    start = time.time()
    for region in region_list:
        res = filter.get_region_price(region)
        print(region, res)
    # res = filter.get_region_price('海珠')
    # res = filter.get_floor_price('海珠')
    # print(filter.get_predict_base('海珠'))
    # res = filter.predict('海珠', '宝岗', 3, True, 1, 2, PredictByType.SPACE, 80)
    end = time.time()
    # print(res)
    print('finished\ncost: {}'.format(str(end - start)))
