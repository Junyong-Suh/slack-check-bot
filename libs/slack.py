import config as c
import requests
from libs import logger, queue


# actually, queue a message to be sent by worker
def send_message(message):
    logger.info(f"Queue a message: {message}")
    queue.enqueue(message)


# send a message to Slack
# https://api.slack.com/docs/rate-limits#rate-limits__limits-when-posting-messages
# In general, apps may post no more than one message per second per channel
# ToDo: Let post message to Slack ONCE per minute per channel to avoid rate limit using Redis
def chat_post_message(message):
    try:
        response = requests.post(
            url=c.SLACK_API_CHAT_POST_MESSAGE_URL,
            json=message,
            headers={
                "Authorization": c.SLACK_APP_TOKEN,
                "Content-type": "application/json; charset=utf-8"  # missing_charset if omitted
            }
        )
        response.raise_for_status()
        logger.info(response.json())
        return response
    except requests.exceptions.HTTPError as errh:
        logger.error("Http Error: ", errh)
    except requests.exceptions.ConnectionError as errc:
        logger.error("Error Connecting: ", errc)
    except requests.exceptions.Timeout as errt:
        logger.error("Timeout Error: ", errt)
    except requests.exceptions.RequestException as err:
        logger.error("Error: ", err)


def mention(user_id):
    return f"<@{user_id}>"
