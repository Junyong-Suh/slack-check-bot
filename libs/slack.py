import requests
import constants as c
from libs import logger, redis


KEYWORDS = ["done", "status", "Done", "Status", "DONE", "STATUS"]


def handle_event(r):
    event = r['event']
    logger.info(event)

    if has_keywords(event['text']):
        message = {"channel": event['channel'], "text": event['text']}
        send_message(message)

    # done
    if any(tag in event.message.text for tag in ['#인증', '#ㅇㅈ']):
        # set redis
        redis.mark(event['channel'], event['user'])
        message = {"channel": event['channel'], "text": "인증!"}
        send_message(message)

    # status
    if any(tag in event.message.text for tag in ['#인증현황', '#인증내역']):
        # get redis
        status = redis.status(event['channel'], event['user'])
        message = {"channel": event['channel'], "text": f"인증현황: {status}"}
        send_message(message)

    return event


def send_message(message):
    response = requests.post(
        url=c.SLACK_API_URL,
        json=message,
        headers={"Authorization": c.SLACK_APP_TOKEN}
    )
    logger.info(response.json())
    return response


def has_keywords(text):
    for k in KEYWORDS:
        if k in text:
            return True
    return False


