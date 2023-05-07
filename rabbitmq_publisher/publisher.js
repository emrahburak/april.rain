const shell = require("shelljs");
const amqp = require("amqplib/callback_api");
const fastify = require("fastify")({
  logger: true,
});


// ----prod----
//require("dotenv").config();
const AMQP_QUEUE = `${process.env.QUEUE}`;
const AMQP_HOST = `amqp://${process.env.HOST}`;

// ----dev----
// const AMQP_QUEUE = 'hello';
// const AMQP_HOST =  'amqp://localhost';


// Create rabbitmq connection
let channel = null;
amqp.connect(AMQP_HOST, function (err, conn) {
  if (!conn) {
    throw new Error(`AMQP connection not available on ${AMQP_HOST}`);
  }
  conn.createChannel(function (err, ch) {
    channel = ch;
  });
});

fastify.get("/", async (request, reply) => {
  reply.type("application/json").code(200);
  return { hello: "world" };
});

fastify.post("/post", async (request, reply) => {

  let {file_name} = request.body
  channel.sendToQueue(AMQP_QUEUE, Buffer.from(JSON.stringify(file_name)));
  reply
    .code(201)
    .header("Content-Type", "application/json; charset=utf-8")
    .send({ status: 201, queueu:AMQP_QUEUE, host:AMQP_HOST, data:file_name });
});

fastify.listen({ host: "0.0.0.0", port: 5000 }, (err, address) => {
  if (err) throw err;
});

//     channel.sendToQueue(QUEUE, Buffer.from(JSON.stringify(fileName)));
