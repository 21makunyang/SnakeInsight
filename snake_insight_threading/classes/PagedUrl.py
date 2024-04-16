class PagedUrl(object):
    """
    带页码的url
    """

    def __init__(self,
                 base_url: str,
                 current_page: int = 1,
                 page_limit: int = None):
        if base_url[-1] != '/':
            base_url += '/'
        self.base_url = base_url
        self.current_page = current_page
        self.page_limit = 50 if page_limit is None else page_limit

    @property
    def url(self):
        return self.base_url + f'p{self.current_page}/'

    @property
    def next_page(self):
        if self.page_limit is None or self.current_page < self.page_limit:
            self.current_page += 1
            paged_url = self.url
            return paged_url
        else:
            return None
