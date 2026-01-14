#! /bin/sh

ROOT="$(pwd)"

# Export env dir to env
echo "Adding env..."
acceptlist_regex=${2:-''}
denylist_regex=${3:-'^(PATH|GIT_DIR|CPATH|CPPATH|LD_PRELOAD|LIBRARY_PATH)$'}
if [ -d "$ENV_DIR" ]; then
for e in $(ls $ENV_DIR); do
  echo "$e" | grep -E "$acceptlist_regex" | grep -qvE "$denylist_regex" &&
  export "$e=$(cat $ENV_DIR/$e)"
  :
done
fi

echo "Installing yarn..."
npm i -g yarn

echo "Running build js apps"
./bin/build_js_apps.sh

echo "Running build public js apps"
./bin/build_public_apps.sh

echo "Running build and cleanup"
./bin/build_and_cleanup.sh
