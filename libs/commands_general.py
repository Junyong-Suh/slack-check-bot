from libs import redis, slack, utils as u


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
