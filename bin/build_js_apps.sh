#! /bin/sh
set -e

echo "Setting up directories..."
ROOT="$(pwd)"
mkdir -p aurochs/apps/webapp/static/dist

echo "Building vue app..."
cd "$ROOT/aurochs/apps/webapp"

# Remove yarnPath from .yarnrc.yml if it exists (the file is gitignored)
# This allows yarn set version to work without the missing release file
if [ -f .yarnrc.yml ]; then
  sed -i.bak '/^yarnPath:/d' .yarnrc.yml 2>/dev/null || sed -i '' '/^yarnPath:/d' .yarnrc.yml
  rm -f .yarnrc.yml.bak
fi

yarn set version berry
yarn
yarn build

cd "$ROOT"
