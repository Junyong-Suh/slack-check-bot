import config as c
from datetime import datetime
from libs import logger, redis, slack


KEYWORDS_MARK = ["done", "Done"]
KEYWORDS_STATUS = ["status", "Status"]
KEYWORDS_CANCEL = ["cancel", "Cancel"]
KEYWORDS_HELP = ["help", "Help"]


def event(request):
    # unexpected requests
    if 'event' not in request:
        logger.error(f"unexpected request missing 'event': {request}")
        return None

    e = request['event']
    logger.info(e)

    # unexpected events
    if 'text' not in e:
        logger.error(f"unexpected event missing 'text': {e}")
        return None

    # help
    if any(tag in e['text'] for tag in KEYWORDS_HELP):
        return usage(e)

    # mark
    if any(tag in e['text'] for tag in KEYWORDS_MARK):
        return mark(e)

    # status
    if any(tag in e['text'] for tag in KEYWORDS_STATUS):
        return status(e)

    # cancel
    if any(tag in e['text'] for tag in KEYWORDS_CANCEL):
        return cancel(e)

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


# progress percent
def progress_percent(count):
    now = datetime.now()
    percent = round(int(count) / int(now.day) * 100, 2)
    if int(count) == 1:
        return f"{count} time ({percent}%)"
    else:
        return f"{count} times ({percent}%)"


def challenge(request):
    return request['challenge']
