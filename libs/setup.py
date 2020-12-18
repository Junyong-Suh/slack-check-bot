import os
import constants as c


def setup_credentials():
    if 'SLACK_APP_TOKEN' in os.environ:
        c.SLACK_APP_TOKEN = f"Bearer {os.environ['SLACK_APP_TOKEN']}"
