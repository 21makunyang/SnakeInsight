from snake_insight.classes import HouseInfo, PagedUrl, UrlFormatter
from snake_insight.core import spider, parser
from snake_insight.util import getLogger
from snake_insight.util.decorator import entry_debug

logger = getLogger('SI.core.processor')


@entry_debug(logger)
def _do_process(paged_url: PagedUrl) -> list[HouseInfo]:
    response_list = spider.get_info(paged_url=paged_url)
    return parser.parse_info(response_list=response_list)


@entry_debug(logger)
def get_rent_info(city_name_list: list[str], page_limit: int | None = None) -> dict[str, list[HouseInfo]]:
    uf = UrlFormatter(city_name_list, page_limit=page_limit)
    city_house_info = {}
    for city, paged_url in uf:
        city_house_info[city] = _do_process(paged_url=paged_url)
        logger.info(f'Get {city}-info end. Length {len(city_house_info[city])}.')
    return city_house_info
