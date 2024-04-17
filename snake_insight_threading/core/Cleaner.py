from snake_insight_threading.util import RedisCommand


class Cleaner(object):
    """
    用于数据清洗

    主要是将广告从数据库去除
    """
    redis = RedisCommand(host='10.242.91.125')

    def __init__(self):
        pass

    def cleanAds(self):
        """
        清理广告

        由于存值时是一份数据一个哈希表，而hscan()针对单个哈希表，
        因此采用遍历所有哈希表，逐条清理的方案
        """
        house_info_keys = self.redis.scan(match=None, count=10000, _type='HASH')
        print(house_info_keys)
        for key in house_info_keys:
            # print(self.redis.hget(key))
            value = self.redis.hget(key)
            # print(value)
            if value.get(b'advertisement') == b'True':
                print('{}-{}'.format(key.decode('utf-8'),
                                     {k.decode('utf-8'): v.decode('utf-8') for k, v in value.items()}))

    def clean(self):
        self.cleanAds()


if __name__ == "__main__":
    cleaner = Cleaner()
    cleaner.clean()
