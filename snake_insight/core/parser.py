from bs4 import BeautifulSoup
from requests import Response

from snake_insight.classes import HouseInfo
from snake_insight.util import getLogger
from snake_insight.util.decorator import entry_debug

logger = getLogger('SI.core.parser')


@entry_debug(logger)
def _do_parse(response: Response) -> list[HouseInfo]:
    house_info_list = []
    bs = BeautifulSoup(response.text, 'html.parser')

    rent_info = bs.find_all(class_='zu-itemmod clearfix')
    for info in rent_info:
        title_info = info.h3.a
        detail_info = info.find_all(class_=['details-item'])
        house_info = detail_info[0]
        house_data = house_info.find_all(class_=['strongbox'])
        address_info = detail_info[1]
        tag_info = detail_info[2]
        price_info = info.find(class_=['zu-side'])

        house_info_list.append(HouseInfo(
            title=title_info.text.strip(),
            bedroom=int(house_data[0].text),
            living_room=int(house_data[1].text),
            area=float(house_data[2].text),
            floor=house_info.contents[-1].strip(),
            community=address_info.a['href'],
            tags=list([tag.text for tag in tag_info.find_all(class_=['cls-common'])]),
            price=int(price_info.find(class_=['price']).text),
            unit=price_info.find(class_=['unit']).text,
            raw=info.text
        ))

    return house_info_list


@entry_debug(logger)
def parse_info(response_list: list[Response]) -> list[HouseInfo]:
    house_info_list = []
    for response in response_list:
        l = len(house_info_list)
        house_info_list += _do_parse(response)
        logger.info(f'Parse data of {response.url}. Length {len(house_info_list) - l}')
    logger.info(f'Parse data end. Length {len(house_info_list)}')
    return house_info_list
