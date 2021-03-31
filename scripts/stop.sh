#!/usr/bin/env bash

if [[ -f "deployer.pid" ]]; then
  kill -9 "$(cat deployer.pid)"
  rm deployer.pid
fi
