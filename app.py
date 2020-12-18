# -*- coding: utf-8 -*-
import redis as redis_heroku
import constants as c

from libs import setup, logger, slack
from flask import Flask, request, jsonify


app = Flask(__name__)
redis = redis_heroku.from_url(c.REDIS_URL, charset="utf-8", decode_responses=True)


@app.before_first_request
def setup():
    setup.setup_credentials()


@app.route('/', methods=['GET'])
def hello_world():
    logger.info('Hello World!')
    return jsonify('Hello World!')


# handles Slack's challenge
@app.route('/challenge', methods=['POST'])
def slack_challenge():
    r = request.get_json()
    logger.info(r)

    # should respond to Slack's challenge
    if 'challenge' in r:
        return r['challenge']

    # capture events
    if 'event' in r:
        slack.handle_event(r)

    logger.error("unknown event received")
    return r


# main
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
