import math
import re

from random_forest.utils.place_code import region_code, area_code


class PreProcessor(object):
    def __init__(self, target_name='price'):
        self.level_dic = {'低': 1 / 6, '中': 1 / 2, '高': 5 / 6}
        self.target_name = target_name

    def process(self, data):
        house_info_utf8 = {k.decode('utf8'): v.decode('utf8') for k, v in data.items()}
        # 将tags的值转为列表
        house_info_utf8['tags'] = str(house_info_utf8.get('tags')[1:-1]).split(',')
        # house_info_utf8['has_elevator'] = 0
        has_elevator = 0

        # 对tags进行遍历，去掉多余的单引号，判断是否有电梯
        for i, tag in enumerate(house_info_utf8['tags']):
            sub_tag = re.search(r"('(.*)?')", tag).group(2)

            if sub_tag == '有电梯':
                # house_info_utf8['has_elevator'] = 1
                has_elevator = 1

            house_info_utf8['tags'][i] = sub_tag

        floor, ok = self.get_floor(house_info_utf8.get('floor'))
        if not ok:
            return None, None

        area = self.encode_area(house_info_utf8.get('area'))
        region = self.encode_region(house_info_utf8.get('region'))
        living_room = float(house_info_utf8.get('living_room'))
        bedroom = float(house_info_utf8.get('bedroom'))
        price = float(house_info_utf8.get('price'))
        space = float(house_info_utf8.get('space'))
        if self.target_name == 'price':
            return [area, region, floor, has_elevator, living_room, bedroom, space], price
        else:
            return [area, region, floor, has_elevator, living_room, bedroom, price], space

    def get_floor(self, floor_info):
        if floor_info == '':
            return 0, False

        level = self.level_dic.get(floor_info[0], 0.0)

        total = re.search(r'共([0-9]+)层', floor_info)
        if total is None:
            return 0, False
        else:
            total = float(total.group(1))
        floor = math.ceil(total * level)
        return floor, True

    def encode_region(self, region):
        return region_code.get(region, -1)

    def encode_area(self, area):
        return area_code.get(area, -1)
