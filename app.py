# -*- coding: utf-8 -*-
from libs import setup, logger, slack
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.before_first_request
def initialize():
    setup.setup_credentials()


@app.route('/', methods=['GET'])
def index():
    logger.info('Hello World!')
    return jsonify('Hello World!')


# handles Slack's challenge
@app.route('/challenge', methods=['POST'])
def challenge():
    r = request.get_json()
    logger.info(r)

    # should respond to Slack's challenge
    if 'challenge' in r:
        return r['challenge']

    # capture events
    if 'event' in r:
        return slack.handle_event(r)

    logger.error("unknown event received")
    return r


# main
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
