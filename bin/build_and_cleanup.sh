#! /bin/sh

ROOT=`pwd`

echo "Clearing collected_static"
cd $ROOT
rm -rf aurochs/collected_static/*

echo "Ensuring env"
export $(grep -v '^#' $ROOT/.env | xargs -d '\n')

echo "Collecting static"
python manage.py collectstatic --noinput 

echo "Clearing vue app source and libraries..."
cd $ROOT/aurochs/apps/webapp
rm -rf .yarn
cd $ROOT

# aurochs/apps/webapp/static/compiled/*
# aurochs/apps/public/static/compiled-static/*
rm -rf $ROOT/aurochs/apps/webapp/.yarn
rm -rf $ROOT/aurochs/apps/public/.yarn
rm -rf $ROOT/aurochs/apps/webapp/node_modules
rm -rf $ROOT/aurochs/apps/public/node_modules
rm -rf $ROOT/aurochs/collected_static/client/static/js/*.map
rm -rf $ROOT/aurochs/collected_static/client/static/js/*.map.br
rm -rf $ROOT/aurochs/collected_static/client/static/js/*.map.gz
rm -rf $ROOT/aurochs/collected_static/client/js/*.map
rm -rf $ROOT/aurochs/collected_static/client/js/*.map.br
rm -rf $ROOT/aurochs/collected_static/client/js/*.map.gz
rm -rf $ROOT/node_modules

echo "Clearing cypress & tests..."
cd $ROOT
rm -rf cypress
rm -rf postman
rm -rf tests
