import config as c
import os


# inject env variables
def setup_credentials():
    if 'SLACK_APP_TOKEN' in os.environ:
        c.SLACK_APP_TOKEN = f"Bearer {os.environ['SLACK_APP_TOKEN']}"
    if 'SLACK_CHECK_BOT_ID' in os.environ:
        c.SLACK_CHECK_BOT_ID = f"{os.environ['SLACK_CHECK_BOT_ID']}"
    if 'ADMIN_SLACK_IDS' in os.environ:
        c.ADMIN_SLACK_IDS = f"{os.environ['ADMIN_SLACK_IDS']}"
