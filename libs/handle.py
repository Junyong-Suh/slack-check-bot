import config as c
from libs import logger, admin, redis, slack, utils as u


KEYWORDS_MARK = ["done", "Done", "DONE", "인증", "ㅇㅈ"]
KEYWORDS_STATUS = ["status", "Status", "STATUS", "현황"]
KEYWORDS_CANCEL = ["cancel", "Cancel", "CANCEL", "취소", "ㅊㅅ"]
KEYWORDS_HELP = ["help", "Help", "HELP"]
KEYWORDS_DISABLE = ["긴급상황"]
KEYWORDS_ENABLE = ["돌아와줘"]
KEYWORDS_IS_ENABLED = ["살아있니"]


def event(e):
    event_text, ok = u.get_app_mention_text(e)

    # do nothing if app mention text is not available
    if not ok:
        return e

    # Admin Commands (check regardless of app enabled or not)

    # disable the app - emergency stop
    if any(tag in event_text for tag in KEYWORDS_DISABLE):
        return admin.disable(e)

    # enable the app
    if any(tag in event_text for tag in KEYWORDS_ENABLE):
        return admin.enable(e)

    # enable the app
    if any(tag in event_text for tag in KEYWORDS_IS_ENABLED):
        return is_enabled(e)

    # General Commands (reject if the app is not enabled)

    # reject if the app is disabled hereafter
    if not redis.is_enabled():
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


# reject if the app is disabled
def reject(e):
    message = {
        "channel": e['channel'],
        "text": "The app is disabled by admin :pray: - please contact admins"
    }
    slack.send_message(message)
    return e


# is enabled
def is_enabled(e):
    if redis.is_enabled():
        status_by_emoji = ":man-gesturing-ok:"
    else:
        status_by_emoji = ":man-gesturing-no:"

    message = {
        "channel": e['channel'],
        "text": f"Is {slack.mention(c.SLACK_CHECK_BOT_ID)} alive? :arrow_right: {status_by_emoji}"
    }
    slack.send_message(message)
    return e


# help commands
def usage(e):
    message = {
        "channel": e['channel'],
        "text": f"Mention me with any keyword in "
                f"['done', 'cancel', 'status', 'help', '인증', 'ㅇㅈ', '취소', 'ㅊㅅ', '현황'] "
                f":wave:"
    }
    slack.send_message(message)
    return e


# increase the count
def mark(e):
    count = redis.mark(e['channel'], e['user'])
    message = {
        "channel": e['channel'],
        "text": f"{slack.mention(e['user'])} marked "
                f"{u.progress_percent(count)} this month :white_check_mark:"
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
        "text": f"{slack.mention(e['user'])} marked "
                f"{u.progress_percent(count)} this month so far :thumbsup:"
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
        "text": f"{slack.mention(e['user'])} last mark canceled - "
                f"{u.progress_percent(count)} marked this month :wink:"
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
