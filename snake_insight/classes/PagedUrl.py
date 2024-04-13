class PagedUrl(object):
    """
    带页码的url
    """

    def __init__(self,
                 url: str,
                 page_limit: int = None):
        if url[-1] != '/':
            url += '/'
        self.url = url
        self.current_page = 0
        self.page_limit = 50 if page_limit is None else page_limit

    def __iter__(self):
        return self

    def __next__(self):
        if self.page_limit is None or self.current_page < self.page_limit:
            self.current_page += 1
            paged_url = self.url + f'p{self.current_page}/'
            return paged_url
        else:
            raise StopIteration()
