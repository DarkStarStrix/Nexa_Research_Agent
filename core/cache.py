import json

async def get_cached_report(redis, key: str):
    data = await redis.get(key)
    if data:
        return json.loads(data)
    return None

async def set_cached_report(redis, key: str, report, ttl: int):
    await redis.set(key, json.dumps(report), ex=ttl)
