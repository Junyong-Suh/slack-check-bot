from rq import Queue
from worker import conn
from libs import slack, logger

q = Queue(connection=conn)


def enqueue(message):
    result = q.enqueue(slack.chat_post_message, message)
    logger.info(f"enqueued_at: {result.enqueued_at}, ttl: {result.ttl}")
