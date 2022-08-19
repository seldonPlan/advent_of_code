#!/usr/bin/env nix-shell

# python versions [ python37, python38, python39, python310, python311 ]
#!nix-shell -i bash -p python310
# shellcheck shell=bash disable=SC2059

# script accepts a single arg pointing to a directory path to put the venv into
script_abs_path="$(cd "$(dirname "${0}")/.." && pwd)"
target_dir="${1:-"${script_abs_path}/.venv"}"
source_py="$(type -p python3)"

# use styled text for script output to user
blue="\033[34m"
yellow="\033[33m"
bold="\033[1m"
dim="\033[2m"
italic="\033[3m"
endstyle="\033[0m"

# info line
printf "\n${dim}${italic}installing venv into${endstyle} "
printf "[ ${yellow}${bold}%s${endstyle} ] " "$target_dir"
printf "${dim}${italic}using${endstyle} "
printf "[ ${yellow}${bold}%s${endstyle} ]\n\n" "$("$(type -p python3)" --version)"

# virtualenv execution
printf -- "${blue}${bold}[===== ${yellow}virtualenv output ${blue}======================================================]${endstyle}\n"
virtualenv \
    --download \
    --always-copy \
    --clear \
    --python "${source_py}" \
    --verbose \
    "${target_dir}"
printf -- "${blue}${bold}[==============================================================================]${endstyle}\n"
