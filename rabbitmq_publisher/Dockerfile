# This stage installs our modules
FROM mhart/alpine-node:14

WORKDIR /app
COPY package.json yarn.lock ./

#RUN npm ci --prod #for npm

RUN apk add --no-cache bash
RUN yarn install --production


# Then we copy over the modules from above onto a `slim` image
FROM mhart/alpine-node:slim-14


RUN mkdir -p /var/watchdir
RUN mkdir -p /var/destination

ENV QUEUE  'hello'
ENV HOST  'amqp://localhost'

EXPOSE 5000

WORKDIR /app
COPY --from=0 /app .
COPY . .

CMD ["node", "publisher.js"]




