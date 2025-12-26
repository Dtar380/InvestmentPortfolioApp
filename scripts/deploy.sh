#!/bin/bash

set -e

ENV=${1:-dev}

if [ "$ENV" != "dev" ] && [ "$ENV" != "prod" ]; then
  echo "Usage: $0 [dev|prod]"
  exit 1
fi

echo "Deploying project to $ENV environment..."

if [ "$ENV" == "dev" ]; then
    docker-compose -f ../deployments/docker-compose.dev.yml up -d
else
    docker-compose -f ../deployments/docker-compose.prod.yml up -d
fi

echo "Deployment completed successfully for $ENV environment."
exit 0
