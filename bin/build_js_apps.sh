#! /bin/sh
set -e

echo "Setting up directories..."
ROOT="$(pwd)"
mkdir -p aurochs/apps/webapp/static/dist

echo "Building vue app..."
cd "$ROOT/aurochs/apps/webapp"

# Build with the committed, pinned Yarn "zero-install" setup: .yarnrc.yml's yarnPath
# points to .yarn/releases/yarn-4.12.0.cjs, and the full dependency cache plus .pnp.cjs
# are committed to git (and therefore present in the Docker build context).
#
# Do NOT run `yarn set version berry`. It pulls an unpinned, newer Yarn that re-resolves
# the PnP dependency tree under stricter rules and breaks the build on @vue/cli-plugin-babel's
# undeclared @babel/runtime peer dependency. Invoking the committed binary directly with
# `--immutable` keeps the build deterministic and fully offline (no registry access needed).
node .yarn/releases/yarn-4.12.0.cjs install --immutable
node .yarn/releases/yarn-4.12.0.cjs build

cd "$ROOT"
