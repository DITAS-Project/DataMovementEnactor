import redis

from config import conf


class RedisClient:

    def __init__(self, host=None, port=None):
        self.host = host if host else conf.redis_host
        self.port = port if port else conf.redis_port
        self.redis = redis.StrictRedis(host=self.host, port=self.port,
                                       charset="utf-8", decode_responses=True)

    def set(self, key, value):
        return self.redis.set(key, value)

    def get(self, key):
        return self.redis.get(key)
