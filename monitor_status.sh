#!/bin/bash

# Script per controllare lo stato del monitor

cd "$(dirname "$0")"

echo "📊 Stato Email Monitor"
echo "===================="

if [ -f monitor.pid ]; then
    PID=$(cat monitor.pid)
    if ps -p $PID > /dev/null; then
        echo "✅ Monitor ATTIVO (PID: $PID)"
        echo ""
        echo "📄 Ultimi 10 log:"
        tail -10 monitor.log
    else
        echo "❌ Monitor NON attivo (PID obsoleto)"
        rm monitor.pid
    fi
else
    # Cerca processi attivi
    if pgrep -f email_monitor.py > /dev/null; then
        echo "⚠️ Monitor attivo ma senza PID file"
        pgrep -af email_monitor.py
    else
        echo "❌ Monitor NON in esecuzione"
    fi
fi

echo ""
echo "===================="

