from libs import logger, redis, slack


KEYWORDS_MARK = ["인증", "ㅇㅈ", "done", "Done", "DONE"]
KEYWORDS_STATUS = ["현황", "내역", "status", "Status", "STATUS"]
KEYWORDS_CANCEL = ["취소", "cancel"]


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
        "text": f"<@{e['user']}> marked {st} times this month :raised_hands:"
    }
    slack.send_message(message)
    return e


# get the count
def status(e):
    st = redis.status(e['channel'], e['user'])
    message = {
        "channel": e['channel'],
        "text": f"<@{e['user']}> marked {st} times this month so far :raised_hands:"
    }
    slack.send_message(message)
    return e


# decrease the count
def cancel(e):
    st = redis.cancel(e['channel'], e['user'])
    message = {
        "channel": e['channel'],
        "text": f"<@{e['user']}> marked {st} times this month so far :raised_hands:"
    }
    slack.send_message(message)
    return e


def challenge(request):
    return request['challenge']
