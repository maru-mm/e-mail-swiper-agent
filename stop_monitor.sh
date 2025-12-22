#!/bin/bash

# Script per fermare il monitor email

cd "$(dirname "$0")"

if [ -f monitor.pid ]; then
    PID=$(cat monitor.pid)
    echo "🛑 Fermando Email Monitor (PID: $PID)..."
    kill $PID
    rm monitor.pid
    echo "✅ Monitor fermato"
else
    echo "⚠️ File monitor.pid non trovato. Il monitor potrebbe non essere in esecuzione."
    echo "Cerco processi monitor attivi..."
    pkill -f email_monitor.py && echo "✅ Processi monitor fermati" || echo "❌ Nessun processo monitor trovato"
fi

