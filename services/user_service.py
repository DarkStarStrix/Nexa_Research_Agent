import datetime
from fastapi import HTTPException

# Tier limits as per doc.md monetization & rate-limit section
tier_limits = {
    "free": {"queries": 10},
    "pro": {"queries": 200},
    "custom": {"queries": 10000}
}

async def check_rate_limit(redis, user_id: str, tier: str) -> bool:
    """
    Increment and check daily query count for user.
    """
    today = datetime.date.today().isoformat()
    key = f"queries:{user_id}:{today}"
    count = await redis.incr(key)
    # On first increment, set TTL til midnight
    if count == 1:
        now = datetime.datetime.utcnow()
        seconds_left = 86400 - (now.hour * 3600 + now.minute * 60 + now.second)
        await redis.expire(key, seconds_left)
    return count <= tier_limits.get(tier, {}).get("queries", 0)

async def enforce_quota(redis, user_id: str, tier: str):
    """
    Raise 429 if user has hit their daily limit.
    """
    allowed = await check_rate_limit(redis, user_id, tier)
    if not allowed:
        raise HTTPException(status_code=429, detail="Daily query limit reached")
    return True

async def get_user_tier(db_conn, user_id: str) -> str:
    """
    Retrieve user tier from PostgreSQL. Default to 'free'.
    """
    with db_conn.cursor() as cur:
        cur.execute("SELECT tier FROM users WHERE id = %s", (user_id,))
        row = cur.fetchone()
    return row[0] if row else "free"

