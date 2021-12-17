#!/usr/bin/env bash

TARGET_DIR="${1:-"${HOME}/code/advent_of_code/.venv"}"
SOURCE_PY="${2:-"/usr/local/opt/python@3.10/bin/python3"}"

virtualenv \
    --download \
    --always-copy \
    --clear \
    --python "${SOURCE_PY}" \
    --verbose \
    "${TARGET_DIR}"
