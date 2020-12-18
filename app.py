# -*- coding: utf-8 -*-
import logging
import sys
import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

SLACK_API_URL = "https://slack.com/api/chat.postMessage"
SLACK_APP_TOKEN = ""
KEYWORDS = ["done", "status"]


@app.before_first_request
def setup():
    setup_logging()
    setup_credentials()


def setup_logging():
    if not app.debug:
        # In production mode, add log handler to sys.stderr.
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.INFO)


def setup_credentials():
    global SLACK_APP_TOKEN
    if 'SLACK_APP_TOKEN' in os.environ:
        SLACK_APP_TOKEN = f"Bearer {os.environ['SLACK_APP_TOKEN']}"


@app.route('/', methods=['GET'])
def hello_world():
    app.logger.info('Hello World!')
    return jsonify('Hello World!')


# handles Slack's challenge
@app.route('/challenge', methods=['POST'])
def slack_challenge():
    r = request.get_json()
    app.logger.info(r)

    if 'challenge' in r:
        challenge = r['challenge']
        return challenge

    if 'event' in r:
        event = parse_event(r['event'])
        if has_keywords(event['text']):
            message = {"channel": event['channel'], "text": event['text']}
            send_message_to_slack(message)
        return event

    app.logger.error("unknown event received")
    return r


def has_keywords(text):
    for k in KEYWORDS:
        if k in text:
            return True
    return False


def parse_event(event):
    app.logger.info(event)
    return {
        'user': event['user'],
        'text': event['text'],
        'channel': event['channel']  # G01G1PQ91NE
    }


def send_message_to_slack(message):
    r = requests.post(
        url=SLACK_API_URL,
        json=message,
        headers={"Authorization": SLACK_APP_TOKEN}
    )
    app.logger.info(r.json())
    return r


# main
if __name__ == "__main__":
    if 1 < len(sys.argv) and sys.argv[1] == "production":
        # logging.basicConfig(level=logging.INFO)
        app.run(host='0.0.0.0', port=5000)
    else:
        # logging.basicConfig(level=logging.DEBUG)
        app.run(host='0.0.0.0', port=5000)
