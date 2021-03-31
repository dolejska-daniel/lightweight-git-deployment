#!/usr/bin/env bash

if [[ -f "deployer.pid" ]]; then
  kill -9 "$(cat deployer.pid)"
  rm deployer.pid
fi

setsid --fork pipenv run python deployer.py >/dev/null 2>&1
