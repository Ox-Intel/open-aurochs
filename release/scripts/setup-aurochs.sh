#! /bin/bash

# Upgrade to aurochs from client/service backends.
RELEASE=latest
PORT=80

echo "Getting network info"

# Ensure the network exists
docker network create --driver bridge ox-net

echo "Getting date"
NOW=`date -I`
echo $NOW

# Load the images.
echo "Loading redis image"
docker load < redis.tar.gz
echo "Loading postgres image"
docker load < postgres.tar.gz
echo "Loading aurochs image"
docker load < aurochs.tar.gz

# Start the images
echo "Starting redis"
docker run --rm -d --name=redis --network="ox-net" -p 6379:6379 redis:6.0-alpine

echo "Starting postgresql"
docker run --rm -d --name=db -p 5432:5432  -v "pgdata:/var/lib/postgresql/data" --network="ox-net"  -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=aurochs postgres:13.6

echo "Setting up database schema"
docker run --rm -it --network="ox-net" --env-file env.airgapped aurochs:$RELEASE /bin/bash -c "python3 manage.py migrate"

echo "Setting up initial data"
docker run --rm -it --network="ox-net" --env-file env.airgapped aurochs:$RELEASE /bin/bash -c "python3 manage.py initial_setup"

echo "Preparing cache"
docker run --rm -it --network="ox-net" --env-file env.airgapped aurochs:$RELEASE /bin/bash -c "python3 manage.py clear_cache"
docker run --rm -it --network="ox-net" --env-file env.airgapped aurochs:$RELEASE /bin/bash -c "python3 manage.py warm_cache"

echo "Starting aurochs"
docker run --rm -d --name=aurochs --network="ox-net" -p $PORT:$PORT --env-file env.airgapped aurochs:$RELEASE

echo "Setup Complete."
