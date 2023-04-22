
const fastify = require("fastify")({
  logger: true,
});

fastify.post("/post", async (request, reply) => {

  let {file_name} = request.body
  console.log(file_name)
  reply
    .code(201)
    .header("Content-Type", "application/json; charset=utf-8")
    .send({ status: 201 });
});

fastify.listen({ host: "0.0.0.0", port: 5001 }, (err, address) => {
  if (err) throw err;
});
