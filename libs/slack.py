import requests
import constants as c
from libs import logger, redis


KEYWORDS = ["status", "Status", "STATUS"]
KEYWORDS_MARK = ["인증", "ㅇㅈ", "done", "Done", "DONE"]
KEYWORDS_STATUS = ["현황", "내역", "status", "Status", "STATUS"]


def handle_event(r):
    event = r['event']
    logger.info(event)

    # done
    if any(tag in event['text'] for tag in KEYWORDS_MARK):
        # set redis
        status = redis.mark(event['channel'], event['user'])
        message = {
            "channel": event['channel'],
            "text": f"{event['user']} marked {status} times this month :raised_hands:"
        }
        send_message(message)
        return event

    # status
    if any(tag in event['text'] for tag in KEYWORDS_STATUS):
        # get redis
        status = redis.status(event['channel'], event['user'])
        message = {
            "channel": event['channel'],
            "text": f"Marked {status} times this month :raised_hands:"
        }
        send_message(message)
        return event

    return event


# send a message to Slack
def send_message(message):
    response = requests.post(
        url=c.SLACK_API_URL,
        json=message,
        headers={
            "Authorization": c.SLACK_APP_TOKEN,
            "Content-type": "application/json; charset=utf-8"  # missing_charset if omitted
        }
    )
    logger.info(response.json())
    return response


def has_keywords(text):
    for k in KEYWORDS:
        if k in text:
            return True
    return False


