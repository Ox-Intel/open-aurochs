#! /bin/sh
TIMEOUT_SEC=720
start_time="$(date -u +%s)"
until $(curl --output /dev/null --silent --head --fail http://localhost:8120); do
    printf '.'
    sleep 5
    current_time="$(date -u +%s)"
    elapsed_seconds=$(($current_time-$start_time))
    if [ $elapsed_seconds -gt $TIMEOUT_SEC ]; then
      echo "timeout of $TIMEOUT_SEC sec"
      exit 1
    fi
    docker compose logs
done
printf '.. server ready.'