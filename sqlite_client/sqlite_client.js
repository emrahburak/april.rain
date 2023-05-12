
const amqp = require("amqplib/callback_api");
const { Sequelize, Model, DataTypes } = require("sequelize")


const AMQP_QUEUE = `${process.env.QUEUE}`;
const HOST = `amqp://${process.env.HOST}`;
const DB = `${process.env.DB}`;
const DB_NAME = `${process.env.DB_NAME}`;


const sequelize = new Sequelize('sqlite::recognized.db')

const Recognized = sequelize.define('Recognized',{
    text: DataTypes.STRING
});

sequelize.sync();


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
        Recognized.create({
            text: msg.content.toString()
        })
      },
      {
        noAck: true,
      }
    );
  });
});
