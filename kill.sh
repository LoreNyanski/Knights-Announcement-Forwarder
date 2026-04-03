FILE_APP_PID="data/app.pid"
FILE_NODE_PID="data/node.pid"

# ----- find & kill processes -----
# Kill Python bot
if [[ -f "$FILE_APP_PID" ]]; then
    OLD_PID="$(cat "$FILE_APP_PID")"
    if kill -0 "$OLD_PID" 2>/dev/null; then
        kill "$OLD_PID"
        sleep 2
    fi
fi

# Kill Node.js WhatsApp server
if [[ -f "$FILE_NODE_PID" ]]; then
    OLD_NODE_PID="$(cat "$FILE_NODE_PID")"
    if kill -0 "$OLD_NODE_PID" 2>/dev/null; then
        kill "$OLD_NODE_PID"
        sleep 2
    fi
fi