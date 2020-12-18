import constants as c
import logging
import os


def setup_logging(app):
    if not app.debug:
        # In production mode, add log handler to sys.stderr.
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.INFO)


def setup_credentials():
    if 'SLACK_APP_TOKEN' in os.environ:
        c.SLACK_APP_TOKEN = f"Bearer {os.environ['SLACK_APP_TOKEN']}"
