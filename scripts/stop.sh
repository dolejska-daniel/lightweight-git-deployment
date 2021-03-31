#!/usr/bin/env bash

if [[ -f "deployer.pid" ]]; then
  PID=$(cat deployer.pid)
  echo "Killing $PID..."
  kill -9 "$PID"
  rm deployer.pid
else
  echo "Process is not running!"
fi
