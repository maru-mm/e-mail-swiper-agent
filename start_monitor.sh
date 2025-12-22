#!/bin/bash

# Script per avviare il monitor email in background

cd "$(dirname "$0")"

echo "🚀 Avvio Email Monitor..."

# Attiva ambiente virtuale
source venv/bin/activate

# Avvia il monitor in background e salva il PID
nohup python email_monitor.py > monitor.log 2>&1 &
MONITOR_PID=$!

echo "✅ Monitor avviato con PID: $MONITOR_PID"
echo $MONITOR_PID > monitor.pid

echo "📄 Log disponibile in: monitor.log"
echo "🛑 Per fermare: ./stop_monitor.sh"
echo ""
echo "Per vedere i log in tempo reale: tail -f monitor.log"

