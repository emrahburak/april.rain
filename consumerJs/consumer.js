const amqp = require("amqplib/callback_api");

const AMQP_QUEUE = `${process.env.QUEUE}`;
const AMQP_HOST = `amqp://${process.env.HOST}`;

amqp.connect(AMQP_HOST, function (err, conn) {
  if (!conn) {
    throw new Error(`AMQP connection not available on ${AMQP_HOST}`);
  }
  conn.createChannel(function (err, ch) {
    ch.assertQueue(AMQP_QUEUE, {
      durable: false,
    });

    console.log(
      " [*] Waiting for messages in %s. To exit press CTRL+C",
      AMQP_QUEUE
    );

    ch.consume(
      AMQP_QUEUE,
      function (msg) {
        console.log(" [x] Received %s", msg.content.toString());
      },
      {
        noAck: false,
      }
    );
  });
});