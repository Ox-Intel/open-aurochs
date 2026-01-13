#! /bin/bash

# Backup the current database
echo "Getting date"
NOW=`date -I`
echo $NOW

echo "Creating backup..."
docker exec -i db /bin/bash -c "PGPASSWORD=postgres pg_dump --username postgres aurochs" > ./dump$NOW.sql

echo "Backup complete as dump$NOW.sql"
