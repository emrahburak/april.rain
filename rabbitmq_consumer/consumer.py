from __future__ import annotations

import os
import logging
from threading import Thread
from kombu import Connection, Queue, Consumer
from kombu.mixins import ConsumerMixin
from recognizer import TestQueue

# prod
HOST = os.environ["HOST"]
QUEUE = os.environ["QUEUE"]

# dev
# HOST = 'localhost'
# QUEUE = 'hello'





logging.basicConfig(level=logging.INFO)
conn = Connection('amqp://guest:guest@{}:5672//'.format(HOST))
queue = Queue('{}'.format(QUEUE))

test_queue = TestQueue()


class C(ConsumerMixin):

    def __init__(self, connection):
        self.connection = connection

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

        # t = Thread(target=test_queue.process_of_queue)
        # t.start()
        # t.join()
        message.ack()
        logging.info('RECOGNIZED: \n {}'.format(recocnized_text))
        logging.info('MESSAGE ACKED')


if __name__ == '__main__':
    consume = C(conn).run()


