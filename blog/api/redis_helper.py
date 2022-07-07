import redis
from datetime import date

client = redis.StrictRedis(host='localhost', port=6379, password=None, db=0)


def redis_helper():
    return client
