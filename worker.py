import os
import redis as redis_heroku
from rq import Worker, Queue, Connection
from libs import setup

listen = ['high', 'default', 'low']
redis_url = os.environ.get("REDIS_URL", 'redis://localhost:6379')
conn = redis_heroku.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        setup.setup_credentials()
        worker = Worker(map(Queue, listen))
        worker.work()
