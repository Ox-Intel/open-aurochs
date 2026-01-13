#! /bin/sh

ROOT=`pwd`

echo "Removing public library dependencies"
mv aurochs/apps/webapp/src/mixins/feature_flips.airgapped.js aurochs/apps/webapp/src/mixins/feature_flips.js 
# mv aurochs/apps/webapp/package.airgapped.json aurochs/apps/webapp/package.json
cd aurochs/apps/webapp && yarn remove rollbar
cd $ROOT

