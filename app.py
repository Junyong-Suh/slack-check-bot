# -*- coding: utf-8 -*-
from libs import setup, logger, handle, slack
from flask import Flask, request, jsonify
from rq import Queue
from worker import conn

app = Flask(__name__)
q = Queue(connection=conn)


@app.before_first_request
def initialize():
    setup.setup_credentials()


@app.route('/', methods=['GET'])
def index():
    logger.info('Hello World!')
    return jsonify('Hello World!')


@app.route('/worker', methods=['GET'])
def worker():
    message = {
        "channel": "G01H6SBNCQ5",
        "text": "test message to worker"
    }
    # slack.send_message(message)
    q.enqueue(slack.send_message, message)
    return jsonify('queued')


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
