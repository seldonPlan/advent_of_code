#!/usr/bin/env bash

# assume script is running from child "scripts" dir
script_abs_path="$(cd "$(dirname "${0}")/.." && pwd)"

target_dir="${1:-"${script_abs_path}/.venv"}"
source_py="${2:-"$(type -p python3)"}"

virtualenv \
    --download \
    --always-copy \
    --clear \
    --python "${source_py}" \
    --verbose \
    "${target_dir}"
