import os, dataset, logging
from kombu import Connection, Queue, Consumer
from kombu.mixins import ConsumerMixin
import pymongo


# prod
HOST = os.environ["HOST"]
QUEUE = os.environ["QUEUE"]
DB_NAME = os.environ["DB_NAME"]
CON_STR = os.environ["CON_STR"]

logging.basicConfig(level=logging.INFO)
conn = Connection('amqp://guest:guest@{}:5672//'.format(HOST))
queue = Queue('{}'.format(QUEUE))
# os.chdir('/var/data/')
# db = dataset.connect('sqlite:///'+DB_NAME)
# my_client = pymongo.MongoClient(str(CON_STR))






class C(ConsumerMixin):

    def __init__(self, connection):
        self.connection = connection
        self.client = pymongo.MongoClient(str(CON_STR))

    def get_consumers(self, Consumer, channel):
        print("listening..")
        return [
            Consumer(queue, callbacks=[self.on_message], accept=['text/plain']),
        ]

    def on_message(self, body, message):
        logging.info('RECEIVED MESSAGE: {0!r}'.format(body))
        logging.info('Processing...')
        mydb = self.client[str(CON_STR)]
        mycol = mydb["recognition_test"]

        mydict = {"text":body}


        mycol.insert_one(mydict)

        message.ack()
        logging.info('MESSAGE ACKED')



if __name__ == '__main__':
    consume = C(conn).run()



