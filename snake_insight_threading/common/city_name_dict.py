CITY_ABBR_TO_NAME = {}

# 可以不用写
CITY_NAME_TO_ABBR = {}


def init():
    for abbr, name in CITY_ABBR_TO_NAME.items():
        CITY_NAME_TO_ABBR[name] = abbr


init()
