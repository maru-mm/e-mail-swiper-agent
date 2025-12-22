#!/bin/bash

# Script per fermare il monitor auto-sync

cd "$(dirname "$0")"

if [ -f monitor_autosync.pid ]; then
    PID=$(cat monitor_autosync.pid)
    echo "🛑 Fermando Auto-Sync Monitor (PID: $PID)..."
    kill $PID
    rm monitor_autosync.pid
    echo "✅ Monitor fermato"
else
    echo "⚠️ File monitor_autosync.pid non trovato."
    echo "Cerco processi auto_sync attivi..."
    pkill -f auto_sync_monitor.py && echo "✅ Processi fermati" || echo "❌ Nessun processo trovato"
fi

