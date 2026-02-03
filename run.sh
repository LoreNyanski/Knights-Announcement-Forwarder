#!/usr/bin/env bash

# find process
# kill it
# pull from github
# run the bot

# ----- vars ----
TEST_MODE=false
HEADLESS=false
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_MAIN="scr/main.py"
SCRIPT_VENV=".venv"
LOG_FILE="app.log"
PID_FILE="app.pid"

cd "$SCRIPT_DIR"

# ----- process flags -----
while getopts "th" opt; do
  case $opt in
    t)
      TEST_MODE=true
      ;;
    h)
      HEADLESS=true
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
git fetch origin
git reset --hard origin/main
git clean -fd

# ----- updating requirements -----
"$SCRIPT_VENV/bin/pip" install -r requirements.txt

# ----- run the bot -----
export TEST_MODE="$TEST_MODE"
export HEADLESS="$HEADLESS"
nohup "$SCRIPT_VENV/bin/python" -u "$SCRIPT_MAIN" > "$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"