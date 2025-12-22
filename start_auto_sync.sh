#!/bin/bash

# Script per avviare il monitor con auto-sync Supabase

cd "$(dirname "$0")"

echo "☁️  Avvio Auto-Sync Monitor (Gmail → SQLite → Supabase)..."

# Attiva ambiente virtuale
source venv/bin/activate

# Avvia il monitor in background e salva il PID
nohup python auto_sync_monitor.py > monitor_autosync.log 2>&1 &
MONITOR_PID=$!

echo "✅ Auto-Sync Monitor avviato con PID: $MONITOR_PID"
echo $MONITOR_PID > monitor_autosync.pid

echo "📄 Log disponibile in: monitor_autosync.log"
echo "🛑 Per fermare: ./stop_auto_sync.sh"
echo ""
echo "Per vedere i log in tempo reale: tail -f monitor_autosync.log"

