#!/bin/bash



# DESTINATION="/tmp/destination"
# WATCHDIR="/tmp/watchdir"
#REMOTE_URL="http://localhost:5000/post"

echo ${WATCHDIR} "listening.." 

while read file; do
    mv -i "$file" $DESTINATION
    #json_file_list=$(echo "${file_list[@]}" | jq -R . | jq -s .)
    curl -X POST -H "Content-Type: application/json" -d '{"file_name": "'"$file"'"}' $REMOTE_URL
    echo
done < <(inotifywait -rmq --format '%w%f' -e create $WATCHDIR)

