#! /bin/sh

echo "Setting up directories..."
ROOT=`pwd`
mkdir -p aurochs/apps/webapp/static/dist

echo "Building vue app..."
cd $ROOT/aurochs/apps/webapp

yarn set version berry
yarn
yarn build

cd $ROOT
