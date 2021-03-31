#!/usr/bin/env bash

if [[ -f "deployer.pid" ]]; then
  PID=$(cat deployer.pid)
  echo "Process is still running, killing $PID..."
  kill -9 "$PID"
  rm deployer.pid
fi

echo "Starting deployer in new process..."
setsid --fork pipenv run python deployer.py >/dev/null 2>&1
sleep 1

if [[ -f "deployer.pid" ]]; then
  echo "Deployer process $(cat deployer.pid) now running!"
else
  echo "Deployer process failed to launch!"
  exit 1
fi
