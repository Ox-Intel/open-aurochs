#! /bin/sh

echo "Setting up directories..."
ROOT=`pwd`
mkdir -p aurochs/apps/public/static/dist

echo "Building public app..."
cd $ROOT/aurochs/apps/public
yarn set version berry
yarn
yarn build

cd $ROOT
