# -*- coding: utf-8 -*-
from libs import setup, logger, handle, redis
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

    # respond to Slack's challenge
    if 'challenge' in r:
        return r['challenge']

    # capture events
    if 'event' in r:
        return handle.event(r['event'])

    logger.error(f"unexpected request received: {r}")
    return r


# main
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
