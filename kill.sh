FILE_APP_PID="data/app.pid"
FILE_NODE_PID="data/node.pid"

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