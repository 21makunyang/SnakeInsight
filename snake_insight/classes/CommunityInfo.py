# TODO: 完善信息
class CommunityInfo(object):
    """
    小区信息
    """

    def __init__(self, city):
        self.city = city
        # supporting facilities
        self.bus = []
