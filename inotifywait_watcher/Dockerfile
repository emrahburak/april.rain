# Base image
FROM alpine:latest

RUN apk add --no-cache inotify-tools curl bash

ENV REMOTE_URL ""
ENV WATCHDIR "/var/watchdir"
ENV DESTINATION  "/var/destination"

RUN mkdir -p ${WATCHDIR} 
RUN mkdir -p ${DESTINATION}

WORKDIR /my_app

# Copy the script into the container
COPY app.sh .

# Make the script executable
RUN chmod +x ./app.sh

# Run the script inside the container
CMD ["./app.sh"]

