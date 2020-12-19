from libs import logger, redis, slack


KEYWORDS_MARK = ["인증", "ㅇㅈ", "done", "Done", "check", "Check"]
KEYWORDS_STATUS = ["현황", "내역", "status", "Status"]
KEYWORDS_CANCEL = ["취소", "cancel", "Cancel"]


def event(request):
    e = request['event']
    logger.info(e)

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


# increase the count
def mark(e):
    st = redis.mark(e['channel'], e['user'])
    message = {
        "channel": e['channel'],
        "text": f"<@{e['user']}> marked {st} times this month :white_check_mark:"
    }
    slack.send_message(message)
    return e


# get the count
def status(e):
    st = redis.status(e['channel'], e['user'])
    message = {
        "channel": e['channel'],
        "text": f"<@{e['user']}> marked {st} times this month so far :thumbsup:"
    }
    slack.send_message(message)
    return e


# decrease the count
def cancel(e):
    st = redis.cancel(e['channel'], e['user'])

    # can't go negative
    if st < 0:
        redis.reset(e['channel'], e['user'])
        message = {
            "channel": e['channel'],
            "text": f"<@{e['user']}> wait, you never done any yet :smirk:"
        }
    else:
        message = {
            "channel": e['channel'],
            "text": f"<@{e['user']}> last mark canceled - {st} times marked this month :wink:"
        }
    slack.send_message(message)
    return e


def challenge(request):
    return request['challenge']
