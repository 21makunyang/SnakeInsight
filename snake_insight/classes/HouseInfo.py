class HouseInfo(object):
    def __init__(self, title, bedroom, living_room, area, floor, community, tags, price, unit, raw):
        self.title = title
        # info
        self.bedroom = bedroom  # 几室
        self.living_room = living_room  # 几厅
        self.area = area  # 面积
        self.floor = floor  # 楼层
        # location
        self.community = community  # 计划存储小区id
        # price
        self.price = price  # 价格
        self.unit = unit  # price的单位
        # extra
        self.tags = tags  # 额外标签
        # raw html
        self.raw = raw  # 获取该对象时对应的原文本

    def __repr__(self):
        # return (f'{{{self.bedroom}室{self.living_room}厅 | {self.area}平方米\n'
        #         f'标签: {self.tags}\n'
        #         f'价格: {self.price}{self.unit}}}')
        return f'{{{self.title}...}}'


