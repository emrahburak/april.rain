# This stage installs our modules
FROM mhart/alpine-node:14

WORKDIR /app
COPY . .

#RUN npm ci --prod #for npm
RUN yarn install --production


RUN mkdir -p /var/watchdir
RUN mkdir -p /var/destination

ENV QUEUE  'hello'
ENV HOST  'amqp://localhost'

CMD ["node", "publisher.js"]