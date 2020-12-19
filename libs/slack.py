import requests
import constants as c
from libs import logger


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
