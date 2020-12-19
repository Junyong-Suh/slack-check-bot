from datetime import datetime
import os
import redis as redis_heroku

r = redis_heroku.from_url(os.environ.get("REDIS_URL"), charset="utf-8", decode_responses=True)


def mark(channel_id, user_id):
    return r.incr(generate_key(channel_id, user_id), 1)


def status(channel_id, user_id):
    return r.get(generate_key(channel_id, user_id))


def generate_key(channel_id, user_id):
    now = datetime.now()
    return f"{channel_id}:{now.year}:{now.month:02d}:{user_id}"

