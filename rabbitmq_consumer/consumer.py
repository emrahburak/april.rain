from __future__ import annotations

import os
import logging
import dataset
from threading import Thread
from kombu import Connection, Queue, Consumer
from kombu.mixins import ConsumerMixin
from recognizer import TestQueue


# prod
HOST = os.environ["HOST"]
QUEUE = os.environ["QUEUE"]
QUEUE_2 = os.environ["QUEUE_2"]
DB_NAME = os.environ["DB_NAME"]

# dev
# HOST = 'localhost'
# QUEUE = 'hello'





logging.basicConfig(level=logging.INFO)
conn = Connection('amqp://guest:guest@{}:5672//'.format(HOST))
simple_queue = conn.SimpleQueue(QUEUE_2)
queue = Queue('{}'.format(QUEUE))

test_queue = TestQueue()


class C(ConsumerMixin):

    def __init__(self, connection, pub_simple_queue):
        self.connection = connection
        self.simple_queue = pub_simple_queue

    def get_consumers(self, Consumer, channel):
        print("listening..")
        return [
            Consumer(queue, callbacks=[self.on_message], accept=['json']),
        ]

    def on_message(self, body, message):
        body = body[1:-1]
        logging.info('RECEIVED MESSAGE: {0!r}'.format(body))
        test_queue.to_queue(body)
        logging.info('Processing...')
        recocnized_text = test_queue.process_of_queue()
        # with dataset.connect('sqlite:///\/var/data/'+DB_NAME) as db:
        #     db['updates'].insert(dict(text=recocnized_text))

        message.ack()
        logging.info('MESSAGE ACKED')


        # send message to another queue for database
        self.simple_queue.put(recocnized_text)




if __name__ == '__main__':
    consume = C(conn, simple_queue).run()


