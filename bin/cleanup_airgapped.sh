#! /bin/sh

ROOT=`pwd`


echo "Clearing public apps"
cd $ROOT
rm -rf aurochs/apps/public

echo "Removing build libraries"
rm -rf aurochs/apps/webapp/.yarn
rm -rf aurochs/apps/public/.yarn
rm -rf aurochs/apps/webapp/node_modules
rm -rf aurochs/apps/public/node_modules
rm -rf node_modules
rm -rf aurochs/collected_static/client/static/js/*.map
rm -rf aurochs/collected_static/client/static/js/*.map.br
rm -rf aurochs/collected_static/client/static/js/*.map.gz
rm -rf aurochs/collected_static/client/js/*.map
rm -rf aurochs/collected_static/client/js/*.map.br
rm -rf aurochs/collected_static/client/js/*.map.gz
