#!/usr/bin/env bash

# find process
# kill it
# pull from github
# run the bot

# ----- vars ----
TEST_MODE="False"
PULL_GITHUB="False"

DIR_CWD="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DIR_VENV=".venv"

SCRIPT_MAIN="scr/main.py"
SCRIPT_INDEXJS="node-js/index.js"

FILE_APP_LOG="app.log"
FILE_NODE_LOG="node.log"
FILE_APP_PID="data/app.pid"
FILE_NODE_PID="data/node.pid"

cd "$DIR_CWD"

# ----- process flags -----
# Use getopt to parse both short and long options
OPTIONS=$(getopt -o pth --long pull,test,help -- "$@")
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
    -h|--help)
      echo "Flags: [-p|--pull] [-t|--test] [-h|--help]"
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

# ----- kill python bot -----
if [[ -f "$FILE_APP_PID" ]]; then
    OLD_PID="$(cat "$FILE_APP_PID")"
    if kill -0 "$OLD_PID" 2>/dev/null; then
        kill "$OLD_PID" 2>/dev/null || true
        sleep 3
        if kill -0 "$OLD_PID" 2>/dev/null; then
            echo "Force killing Python process $OLD_PID"
            kill -9 "$OLD_PID"
        fi
    fi
fi

# ----- kill node server -----
if [[ -f "$FILE_NODE_PID" ]]; then
    OLD_NODE_PID="$(cat "$FILE_NODE_PID")"
    if kill -0 "$OLD_NODE_PID" 2>/dev/null; then
        kill "$OLD_NODE_PID" 2>/dev/null || true
        sleep 3
        if kill -0 "$OLD_NODE_PID" 2>/dev/null; then
            echo "Force killing Node process $OLD_NODE_PID"
            kill -9 "$OLD_NODE_PID"
        fi
    fi
fi

# ----- pull from github -----
if [[ "$PULL_GITHUB" == "True" ]]; then
    git fetch origin
    git reset --hard origin/main
    git clean -fd
    # ----- updating requirements -----
    "$DIR_VENV/bin/pip" install -r requirements.txt
fi

# ----- run the Node.js server -----
nohup node "$SCRIPT_INDEXJS" > "$FILE_NODE_LOG" 2>&1 &
echo $! > "$FILE_NODE_PID"
echo "Node.js WhatsApp server started with PID $(cat "$FILE_NODE_PID")"

# ----- run the discord bot -----
export TEST_MODE="$TEST_MODE"
nohup "$DIR_VENV/bin/python" -u "$SCRIPT_MAIN" > "$FILE_APP_LOG" 2>&1 &
echo $! > "$FILE_APP_PID"
echo "discord bot started with PID $(cat "$FILE_APP_PID")"
