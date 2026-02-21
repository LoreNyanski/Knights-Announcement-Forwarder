#!/usr/bin/env bash

# find process
# kill it
# pull from github
# run the bot

# ----- vars ----
TEST_MODE="False"
PULL_GITHUB="False"
CALIBRATE="False"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_MAIN="scr/main.py"
SCRIPT_COORDINATES="scr/coordinate_finder.py"
SCRIPT_VENV=".venv"
LOG_FILE="app.log"
PID_FILE="data/app.pid"
COORD_FILE="data/app.coordinates"

cd "$SCRIPT_DIR"

# ----- process flags -----
# Use getopt to parse both short and long options
OPTIONS=$(getopt -o ptch --long pull,test,calibrate,help -- "$@")
if [ $? -ne 0 ]; then
  exit 1
fi

# Reorder the positional parameters as parsed by getopt
eval set -- "$OPTIONS"

# Parse the flags
while true; do
  case "$1" in
    -p|--pull)
      PULL_GITHUB=True
      shift
      ;;
    -t|--test)
      TEST_MODE=True
      shift
      ;;
    -c|--calibrate)
      CALIBRATE=False
      shift
      ;;
    -h|--help)
      echo "Flags: [-p|--pull] [-t|--test] [-c|--calibrate] [-h|--help]"
      exit 0
      ;;
    --)
      shift
      break
      ;;
    *)
      echo "Unexpected option: $1"
      exit 1
      ;;
  esac
done

# ----- find & kill process -----
if [[ -f "$PID_FILE" ]]; then
    OLD_PID="$(cat "$PID_FILE")"
    if kill -0 "$OLD_PID" 2>/dev/null; then
        kill "$OLD_PID" 
        sleep 2
    fi
fi

# ----- pull from github -----
if [[ "$PULL_GITHUB" == "True" ]]; then
    git fetch origin
    git reset --hard origin/main
    git clean -fd
    # ----- updating requirements -----
    "$SCRIPT_VENV/bin/pip" install -r requirements.txt
fi

# ----- run the bot -----
export TEST_MODE="$TEST_MODE"
    # ----- calibrating coordinates -----
if [[ "$CALIBRATE" == "True" ]]; then
    "$SCRIPT_VENV/bin/python" "$SCRIPT_COORDINATES"
fi
nohup "$SCRIPT_VENV/bin/python" -u "$SCRIPT_MAIN" > "$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"