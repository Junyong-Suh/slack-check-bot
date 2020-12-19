from datetime import datetime
import os
import redis as redis_heroku

r = redis_heroku.from_url(os.environ.get("REDIS_URL"), charset="utf-8", decode_responses=True)


def mark(channel_id, user_id):
    return r.incr(generate_key(channel_id, user_id))


def status(channel_id, user_id):
    return r.get(generate_key(channel_id, user_id))


def cancel(channel_id, user_id):
    return r.decr(generate_key(channel_id, user_id))


def reset(channel_id, user_id):
    r.set(generate_key(channel_id, user_id), 0)


def generate_key(channel_id, user_id):
    now = datetime.now()
    return f"{channel_id}:{now.year}:{now.month:02d}:{user_id}"
