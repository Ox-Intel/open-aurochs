#!/bin/bash

set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

apt-get update

apt-get -y upgrade

apt-get -y install tzdata libpq-dev weasyprint

apt-get clean

# Delete index files we don't need anymore:
rm -rf /var/lib/apt/lists/*