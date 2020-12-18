import requests
import constants as c
from libs import logger


def handle_event(r):
    event = parse_event(r['event'])
    if has_keywords(event['text']):
        message = {"channel": event['channel'], "text": event['text']}
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
    for k in c.KEYWORDS:
        if k in text:
            return True
    return False


def parse_event(event):
    logger.info(event)
    return {
        'user': event['user'],  # ex. U01GMLMBBND
        'text': event['text'],
        'channel': event['channel']  # ex. G01G1PQ91NE
    }

