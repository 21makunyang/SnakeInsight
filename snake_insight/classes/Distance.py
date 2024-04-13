
class Distance(object):
    """
    到达某地的距离（目前配合CommunityInfo使用，表示该小区到某地的距离）
    """
    def __init__(self, loc: str, dis: int, info: str = None):
        self.loc = loc
        self.dis = dis
        self.info = info

    def __eq__(self, other):
        return self.loc == other.loc and self.dis == other.dis

    def __lt__(self, other):
        return self.dis < other.dis or self.loc < other.loc
