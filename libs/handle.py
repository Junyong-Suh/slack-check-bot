import config as c
from datetime import datetime
from libs import logger, redis, slack


KEYWORDS_MARK = ["done", "Done", "DONE", "인증"]
KEYWORDS_STATUS = ["status", "Status", "STATUS", "현황"]
KEYWORDS_CANCEL = ["cancel", "Cancel", "CANCEL", "취소"]
KEYWORDS_HELP = ["help", "Help", "HELP"]
KEYWORDS_DISABLE = ["disable"]
KEYWORDS_ENABLE = ["enable"]


def event(e):
    event_text = get_app_mention_text(e)

    # do nothing if app mention text is not available
    if event_text is None:
        return None

    # disable the app - emergency stop
    if any(tag in event_text for tag in KEYWORDS_DISABLE):
        return disable(e)

    # enable the app
    if any(tag in event_text for tag in KEYWORDS_ENABLE):
        return enable(e)

    # reject if the app is disabled hereafter
    if not c.CHECK_BOT_APP_ENABLED:
        return reject(e)

    # help
    if any(tag in event_text for tag in KEYWORDS_HELP):
        return usage(e)

    # mark
    if any(tag in event_text for tag in KEYWORDS_MARK):
        return mark(e)

    # status
    if any(tag in event_text for tag in KEYWORDS_STATUS):
        return status(e)

    # cancel
    if any(tag in event_text for tag in KEYWORDS_CANCEL):
        return cancel(e)

    return e


# handles different types of event
# returns None if not available
def get_app_mention_text(e):
    # app_mention: https://gist.github.com/Junyong-Suh/94fc948c8c1f7819a258101a23f169aa
    if is_event_type_app_mention(e) and 'text' in e:
        return e['text']

    if is_event_type_message(e):
        # message_changed: https://gist.github.com/Junyong-Suh/20e0291bc3ba230b2496ea2620cc66dd
        if is_message_subtype_message_changed(e):
            logger.info(f"Message changed: {e}")
            return None

        # message_deleted: https://gist.github.com/Junyong-Suh/385d2d68dd3ffbf88dad50f2032716c8
        if is_message_subtype_message_deleted(e):
            logger.info(f"Message deleted: {e}")
            return None

    logger.error(f"Unexpected event: {e}")
    return None


# disable the app
def disable(e):
    if is_user_admin(e['user']):
        # only for admin
        c.CHECK_BOT_APP_ENABLED = False
        logger.error(f"Check bot disabled by {e['user']}")
        message_text = f"{slack.mention(e['user'])} disabled :disappointed:"
    else:
        # restrict others
        logger.error(f"Check bot disable request by {e['user']} rejected")
        message_text = f"{slack.mention(e['user'])} is not allowed to disable the app :no_entry_sign:"

    # send message
    slack.send_message({
        "channel": e['channel'],
        "text": message_text
    })


# enable the app
def enable(e):
    if is_user_admin(e['user']):
        # only for admin
        c.CHECK_BOT_APP_ENABLED = True
        logger.error(f"Check bot enabled by {e['user']}")
        message_text = f"{slack.mention(e['user'])} enabled :tada:"
    else:
        # restrict others
        logger.error(f"Check bot enable request by {e['user']} rejected")
        message_text = f"{slack.mention(e['user'])} is not allowed to enable the app :no_entry_sign:"

    # send message
    slack.send_message({
        "channel": e['channel'],
        "text": message_text
    })


# reject if the app is disabled
def reject(e):
    message = {
        "channel": e['channel'],
        "text": "The app is disabled by admin :pray: - please contact admins"
    }
    slack.send_message(message)
    return e


# help commands
def usage(e):
    message = {
        "channel": e['channel'],
        "text": f"Mention me with any keyword in ['done', 'cancel', 'status', 'help'] :wave:"
    }
    slack.send_message(message)
    return e


# increase the count
def mark(e):
    count = redis.mark(e['channel'], e['user'])
    message = {
        "channel": e['channel'],
        "text": f"{slack.mention(e['user'])} marked {progress_percent(count)} this month :white_check_mark:"
    }
    slack.send_message(message)
    return e


# get the count
def status(e):
    count = redis.status(e['channel'], e['user'])

    # no status
    if int(count) < 1:
        return reset(e)

    message = {
        "channel": e['channel'],
        "text": f"{slack.mention(e['user'])} marked {progress_percent(count)} this month so far :thumbsup:"
    }
    slack.send_message(message)
    return e


# decrease the count
def cancel(e):
    count = redis.cancel(e['channel'], e['user'])

    # can't go negative, reset
    if int(count) < 0:
        return reset(e)

    message = {
        "channel": e['channel'],
        "text": f"{slack.mention(e['user'])} last mark canceled - {progress_percent(count)} marked this month :wink:"
    }
    slack.send_message(message)
    return e


# reset the status
def reset(e):
    redis.reset(e['channel'], e['user'])
    message = {
        "channel": e['channel'],
        "text": f"{slack.mention(e['user'])} wait, you never done any yet :smirk:"
    }
    slack.send_message(message)
    return e


def is_user_admin(user):
    logger.info(f"Current admins: {c.ADMIN_SLACK_IDS}")
    return user in c.ADMIN_SLACK_IDS


def is_event_type_app_mention(e):
    return 'type' in e and e['type'] == 'app_mention'


def is_event_type_message(e):
    return 'type' in e and e['type'] == 'message'


def is_message_subtype_message_changed(e):
    return 'subtype' in e and e['subtype'] == 'message_changed'


def is_message_subtype_message_deleted(e):
    return 'subtype' in e and e['subtype'] == 'message_deleted'


# progress percent
def progress_percent(count):
    now = datetime.now()
    percent = round(int(count) / int(now.day) * 100, 2)
    if int(count) == 1:
        return f"{count} time ({percent}%)"
    else:
        return f"{count} times ({percent}%)"
