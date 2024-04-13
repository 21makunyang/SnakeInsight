from snake_insight.classes.PagedUrl import PagedUrl


def form_base_url(city_name_list: list[str], page_limit: int = None) -> dict[str, PagedUrl]:
    city_url_dict = {}

    for city_name in city_name_list:
        formatted_city_url = f'https://{city_name}.zu.anjuke.com/fangyuan/'
        city_url_dict[city_name] = PagedUrl(url=formatted_city_url, page_limit=page_limit)

    return city_url_dict


class UrlFormatter(object):
    """
    url格式化，传入城市名缩写，可生成对应城市的url
    """

    def __init__(self, city_name_list: list[str], page_limit: int = None):
        self.formatted_url = form_base_url(city_name_list, page_limit=page_limit)

    def __iter__(self):
        return self.formatted_url.items().__iter__()
