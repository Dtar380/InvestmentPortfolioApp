#!/bin/bash

set -e

ENV=${1:-dev}

if [ "$ENV" != "dev" ] && [ "$ENV" != "prod" ]; then
  echo "Usage: $0 [dev|prod]"
  exit 1
fi

echo "Building project for $ENV environment..."

if [ "$ENV" == "dev" ]; then
    docker-compose -f ../deployments/docker-compose.dev.yml build
else
    docker-compose -f ../deployments/docker-compose.prod.yml build
fi

echo "Build completed successfully for $ENV environment."
exit 0
