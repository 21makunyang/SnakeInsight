class HouseInfo(object):
    def __init__(self, id_, title, bedroom, living_room, space, floor, community, city, region, area, tags, advertisement, price, unit, raw):
        self.id = id_
        self.title = title
        # info
        self.bedroom = bedroom
        self.living_room = living_room
        self.space = space
        self.floor = floor
        # location
        self.community = community
        self.city = city
        self.region = region
        self.area = area
        # price
        self.price = price
        self.unit = unit
        # extra
        self.tags = str(tags)
        self.advertisement = str(advertisement)
        # raw html
        self.raw = str(raw)

    def __repr__(self):
        # return (f'{{{self.bedroom}室{self.living_room}厅 | {self.area}平方米\n'
        #         f'标签: {self.tags}\n'
        #         f'价格: {self.price}{self.unit}}}')
        return f'{{{self.title}...}}'


