from redis.asyncio import Redis


class RedisStorage:
    def __init__(self):
        self.storage = Redis(decode_responses=True)
