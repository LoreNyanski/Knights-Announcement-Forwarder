#!/usr/bin/env bash

# find process
# kill it
# pull from github
# run the bot

# ----- vars ----
TEST_MODE="False"
PULL_GITHUB="False"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_MAIN="scr/main.py"
SCRIPT_VENV=".venv"
LOG_FILE="app.log"
PID_FILE="app.pid"

cd "$SCRIPT_DIR"

# ----- process flags -----
while getopts "thn" opt; do
  case $opt in
    t)
      TEST_MODE="True"
      ;;
    n)
      PULL_GITHUB="True"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done
shift $((OPTIND -1))

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
nohup "$SCRIPT_VENV/bin/python" -u "$SCRIPT_MAIN" > "$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"