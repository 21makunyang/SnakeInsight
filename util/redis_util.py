import redis


class RedisUtil:
    def __init__(self, host='localhost', port=6379, max_connections=10):
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.conn_pool = self.get_redis_connect()

    def get_redis_connect(self):
        return redis.ConnectionPool(host=self.host, port=self.port, max_connections=self.max_connections)

    def get(self, key):
        conn = redis.Redis(connection_pool=self.conn_pool, decode_responses=True)
        return conn.get(key)

    def set(self, key, value):
        conn = redis.Redis(connection_pool=self.conn_pool, decode_responses=True)
        conn.set(key, value)


r = RedisUtil()
