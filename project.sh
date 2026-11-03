#!/bin/bash

if [ "$1" == "dev" ]; then
    cd app/
    uv run fastapi dev

elif [ "$1" == "prod" ]; then
    uv run fastapi prod

elif [ "$1" == "format" ]; then
    black app/ --line-length 79
    isort app/

else
    echo "Usage: ./project.sh [dev|prod]"
fi