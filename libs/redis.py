from datetime import datetime
from libs import logger
import config as c
import os
import redis as redis_heroku

r = redis_heroku.from_url(os.environ.get("REDIS_URL"), charset="utf-8", decode_responses=True)


# increase by one
def mark(channel_id, user_id):
    return r.incr(generate_key(channel_id, user_id))


# return the status
def status(channel_id, user_id):
    return r.get(generate_key(channel_id, user_id))


# decrease by one
def cancel(channel_id, user_id):
    return r.decr(generate_key(channel_id, user_id))


# set to 0
def reset(channel_id, user_id):
    r.set(generate_key(channel_id, user_id), 0)


def generate_key(channel_id, user_id):
    now = datetime.now()
    return f"{channel_id}:{now.year}:{now.month:02d}:{user_id}"


# return if the app is enabled
def is_enabled():
    enabled = r.get(config_key_enabled())
    logger.info(f"is_enabled: {enabled}")
    if enabled != "False":
        return True  # includes the value never set
    else:
        return False


# enable the app
def enable():
    r.set(config_key_enabled(), "True")


# disable the app
def disable():
    r.set(config_key_enabled(), "False")


def config_key_enabled():
    return f"{c.SLACK_CHECK_BOT_ID}:config:enabled"
