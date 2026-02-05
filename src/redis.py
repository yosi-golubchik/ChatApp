from redis import Redis
from src.config import redis_conf

redis_client_instance = Redis(**redis_conf, decode_responses=True)

def get_redis_client() -> Redis:
    return redis_client_instance
