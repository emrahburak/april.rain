# This stage installs our modules
FROM mhart/alpine-node:14

WORKDIR /app
COPY package.json yarn.lock ./

#RUN npm ci --prod #for npm

RUN yarn install --production


# Then we copy over the modules from above onto a `slim` image
FROM mhart/alpine-node:slim-14

ENV QUEUE  'hello'
ENV HOST  'amqp://localhost'

RUN apk add --no-cache bash

WORKDIR /app
COPY --from=0 /app .
COPY . .

CMD ["node", "consumer.js"]
