import requests
import config as c
from libs import logger


# send a message to Slack
def send_message(message):
    try:
        response = requests.post(
            url=c.SLACK_API_URL,
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
        print("Http Error: ", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting: ", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error: ", errt)
    except requests.exceptions.RequestException as err:
        print("Error: ", err)


def mention(user_id):
    return f"<@{user_id}>"
