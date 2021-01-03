import config as c
from libs import logger, redis, slack


# disable the app
def disable(e):
    if is_admin(e['user']):
        # only for admin
        redis.disable()
        logger.error(f"Check bot disabled by {e['user']} - redis.is_enabled(): {redis.is_enabled()}")
        message_text = f"{slack.mention(c.SLACK_CHECK_BOT_ID)} brought down " \
                       f"by {slack.mention(e['user'])} :disappointed:"
    else:
        # restrict others
        logger.error(f"Check bot disable request by {e['user']} rejected")
        message_text = f"{slack.mention(e['user'])} is not allowed to disable the app :no_entry_sign:"

    # send message
    slack.send_message({
        "channel": e['channel'],
        "text": message_text
    })
    return e


# enable the app
def enable(e):
    if is_admin(e['user']):
        # only for admin
        redis.enable()
        logger.error(f"Check bot enabled by {e['user']} - redis.is_enabled(): {redis.is_enabled()}")
        message_text = f"{slack.mention(c.SLACK_CHECK_BOT_ID)} back alive " \
                       f"by {slack.mention(e['user'])} :tada:"
    else:
        # restrict others
        logger.error(f"Check bot enable request by {e['user']} rejected")
        message_text = f"{slack.mention(e['user'])} is not allowed to enable the app :no_entry_sign:"

    # send message
    slack.send_message({
        "channel": e['channel'],
        "text": message_text
    })
    return e


def is_admin(user):
    logger.info(f"Current admins: {c.ADMIN_SLACK_IDS}")
    return user in c.ADMIN_SLACK_IDS
