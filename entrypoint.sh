#!/bin/sh

## Runs database migrations scripts
export FLASK_APP=run.py
while true; do
  flask db upgrade
  if [[ "$?" == "0" ]]; then
    break
  fi
  echo "Upgrade command failed, retrying in 5 seconds..."
  sleep 5
done
unset FLASK_APP

## Runs the application server
python3 server.py
