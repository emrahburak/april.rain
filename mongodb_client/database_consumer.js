const amqp = require("amqplib/callback_api");
const mongoose = require("mongoose");

//prod
const AMQP_QUEUE = `${process.env.QUEUE}`;
const HOST = `amqp://${process.env.HOST}`;
const DB = `${process.env.DB}`;
const DB_NAME = `${process.env.DB_NAME}`;

mongoose
  .connect("mongodb://root:hello@s_mongo:27017/april_rain_db", {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => {
    console.log("MongoDB veritabanına bağlandı");
  });

//dev
// const AMQP_QUEUE = 'hello';
// const HOST = 'amqp://localhost';

amqp.connect(HOST, function (err, conn) {
  if (!conn) {
    throw new Error(`AMQP connection not available on ${HOST}`);
  }
  conn.createChannel(function (err, ch) {
    ch.assertQueue(AMQP_QUEUE, {
      durable: true,
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
        noAck: true,
      }
    );
  });
});
