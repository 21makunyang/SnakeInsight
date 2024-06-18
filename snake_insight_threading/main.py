from snake_insight_threading.classes import Task
from snake_insight_threading.core import Controller

if __name__ == '__main__':
    controller = Controller(idle_detection_time=10, parser_page_limit=10)
    # paged_url = PagedUrl(base_url='https://gz.zu.anjuke.com/fangyuan/', page_limit=2)
    # ['Parser.RegionUrlTask', 'Parser.AreaUrlTask', 'Parser.HouseInfo']
    task = Task(group='广州',
                parser_sequence=['Parser.RegionUrlTask', 'Parser.AreaUrlTask', 'Parser.HouseInfo'],
                url='https://gz.zu.anjuke.com/fangyuan/',
                target='https://gz.zu.anjuke.com/fangyuan/')

    controller.add_task(task)
    controller.start()
