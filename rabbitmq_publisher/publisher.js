const shell = require("shelljs");
const amqp = require("amqplib/callback_api");
const fastify = require("fastify")({
  logger: true,
});
require("dotenv").config();

const QUEUE = `${process.env.QUEUE}`;
const HOST = `${process.env.HOST}`;

// Create rabbitmq connection
// let channel = null;
// amqp.connect(HOST, function (err, conn) {
//   if (!conn) {
//     throw new Error(`AMQP connection not available on ${HOST}`);
//   }
//   conn.createChannel(function (err, ch) {
//     channel = ch;
//   });
// });

fastify.get("/", async (request, reply) => {
  reply.type("application/json").code(200);
  return { hello: "world" };
});

fastify.post("/post", async (request, reply) => {
  reply
    .code(201)
    .header("Content-Type", "application/json; charset=utf-8")
    .send({ status: 201 });
});

fastify.listen({ port: 5000 }, (err, address) => {
  if (err) throw err;
});

//     channel.sendToQueue(QUEUE, Buffer.from(JSON.stringify(fileName)));
