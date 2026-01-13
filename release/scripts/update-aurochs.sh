#! /bin/bash

# Upgrade  aurochs instance.
RELEASE=latest
PORT=80


# Backup the current database
echo "Getting date"
NOW=`date -I`
echo $NOW

echo "Getting pg dump as a backup before updating"
docker exec -i db /bin/bash -c "PGPASSWORD=postgres pg_dump --username postgres aurochs" > ./dump$NOW.sql

# Load the new version of the aurochs image.
echo "Loading aurochs image"
docker load < aurochs.tar.gz

# Stop the existing container
echo "Stopping aurochs container"
docker stop aurochs

# Start the images
echo "Migrating database"
docker run --rm  --network="ox-net" --env-file env.airgapped aurochs:$RELEASE /bin/bash -c "python3 manage.py migrate"

echo "Preparing cache"
docker run --rm -it --network="ox-net" --env-file env.airgapped aurochs:$RELEASE /bin/bash -c "python3 manage.py clear_cache"
docker run --rm -it --network="ox-net" --env-file env.airgapped aurochs:$RELEASE /bin/bash -c "python3 manage.py warm_cache"

echo "Starting aurochs"
docker run --rm -d --name=aurochs --network="ox-net" -p $PORT:$PORT --env-file env.airgapped aurochs:$RELEASE

echo "COMPLETE"
