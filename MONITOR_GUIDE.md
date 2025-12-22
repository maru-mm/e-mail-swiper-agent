# 📡 Guida Monitor Email Automatico

Sistema di monitoraggio automatico che controlla periodicamente l'arrivo di nuove email e le processa con AI.

---

## 🎯 Cosa Fa il Monitor

Il servizio di monitoraggio:

✅ **Controlla** l'account Gmail ogni 15 minuti
✅ **Identifica** le email nuove (non ancora nel database)
✅ **Scarica** i dettagli completi delle nuove email
✅ **Analizza** ogni email con OpenAI per categorizzarla
✅ **Salva** tutto nel database automaticamente
✅ **Log** di tutte le operazioni

---

## 🚀 Come Avviare

### **Metodo 1: Script Automatico (Consigliato)**

```bash
cd "/Users/mac/Desktop/WASABI OFFERS TECH/email reverse agent"
./start_monitor.sh
```

**Output:**
```
🚀 Avvio Email Monitor...
✅ Monitor avviato con PID: 12345
📄 Log disponibile in: monitor.log
🛑 Per fermare: ./stop_monitor.sh

Per vedere i log in tempo reale: tail -f monitor.log
```

### **Metodo 2: Manuale (per vedere l'output)**

```bash
cd "/Users/mac/Desktop/WASABI OFFERS TECH/email reverse agent"
source venv/bin/activate
python email_monitor.py
```

**Ctrl+C** per fermare

---

## 🛑 Come Fermare

```bash
./stop_monitor.sh
```

---

## 📊 Come Controllare lo Stato

### **Opzione 1: Script**
```bash
./monitor_status.sh
```

### **Opzione 2: Dashboard Web**
Vai su: **http://localhost:5000/monitor**

Vedrai:
- ✅/❌ Stato monitor (attivo/non attivo)
- 🆔 PID del processo
- 📋 Log degli ultimi controlli
- ⚙️ Configurazione attiva
- 🔄 Bottone aggiorna in tempo reale

---

## 📋 Workflow Automatico

### **Ogni 15 minuti il monitor:**

1. **🔍 Controlla Gmail**
   ```
   📥 Recupero messaggi recenti da Gmail...
   📊 Email già nel database: 150
   ```

2. **🆕 Identifica Nuove Email**
   ```
   🆕 Trovate 3 nuove email!
   ```

3. **📧 Estrae Dettagli**
   ```
   📧 Email 1/3...
      Da: Bioma Health <hello@bioma.health>
      Oggetto: New promotion for you
   ```

4. **🤖 Analizza con AI**
   ```
   🤖 Analisi AI in corso per 3 email...
   Analisi email 1/3...
   Analisi email 2/3...
   Analisi email 3/3...
   ```

5. **💾 Salva nel Database**
   ```
   💾 Salvataggio nel database...
   ✅ Processate e salvate 3 nuove email!
   ```

6. **📊 Riepilogo**
   ```
   📊 RIEPILOGO NUOVE EMAIL
   
   📧 Per tipo:
      • marketing: 2
      • transactional: 1
   
   👥 Sender unici: 2
   ```

---

## ⚙️ Configurazione

### **Modifica Intervallo di Controllo**

Modifica in `email_monitor.py`:

```python
CHECK_INTERVAL_MINUTES = 15  # Cambia qui (in minuti)
```

Opzioni comuni:
- `5` - Ogni 5 minuti (frequente)
- `15` - Ogni 15 minuti (bilanciato) ✓ Default
- `30` - Ogni 30 minuti
- `60` - Ogni ora

### **Modifica Numero Email Controllate**

In `email_monitor.py`, metodo `check_for_new_emails()`:

```python
messages = self.extractor.get_messages(max_results=50)  # Cambia qui
```

---

## 📄 Log File

Tutto viene salvato in **`monitor.log`**

### **Vedere Log in Tempo Reale:**
```bash
tail -f monitor.log
```

### **Vedere Ultimi 50 Log:**
```bash
tail -50 monitor.log
```

### **Cercare Errori:**
```bash
grep "Errore" monitor.log
grep "❌" monitor.log
```

---

## 🔧 Troubleshooting

### **Monitor non si avvia**

1. **Verifica autenticazione Gmail:**
   ```bash
   python test_connection.py
   ```

2. **Controlla che non sia già attivo:**
   ```bash
   ./monitor_status.sh
   ```

3. **Verifica log errori:**
   ```bash
   cat monitor.log
   ```

### **Monitor si ferma da solo**

Possibili cause:
- Token OAuth scaduto → Elimina `token.pickle` e riautentica
- Quota API Gmail superata → Riduci frequenza controlli
- Errore OpenAI → Verifica credito API key

### **Email non vengono processate**

1. **Verifica che siano davvero nuove:**
   - Il monitor controlla solo le ultime 50 email
   - Email già nel DB vengono saltate

2. **Controlla i log:**
   ```bash
   tail -50 monitor.log
   ```

---

## 💡 Best Practices

### **1. Avvia Monitor in Background**
```bash
./start_monitor.sh
```

Così gira sempre, anche se chiudi il terminale.

### **2. Monitora i Log Periodicamente**
```bash
tail -f monitor.log
```

O usa la dashboard web: http://localhost:5000/monitor

### **3. Backup Database Regolarmente**
```bash
cp emails.db emails_backup_$(date +%Y%m%d).db
```

### **4. Controlla Costi OpenAI**

Il monitor usa GPT-4o-mini:
- ~$0.001 per email
- 100 email/giorno = ~$3/mese
- Monitora su: https://platform.openai.com/usage

---

## 🎯 Integrazione con Dashboard

Le nuove email processate automaticamente:
- ✅ Appaiono immediatamente in tutte le viste
- ✅ Sono categorizzate e analizzate
- ✅ Disponibili per swipe
- ✅ Incluse nelle statistiche

**Nessuna azione richiesta!** Il monitor popola tutto automaticamente.

---

## 📊 Statistiche Monitor

Accedi a: **http://localhost:5000/monitor**

Vedrai:
- 🟢 Stato in tempo reale (attivo/non attivo)
- 📋 Log delle ultime operazioni
- ⚙️ Configurazione corrente
- 🔄 Refresh automatico ogni 30 secondi

---

## 🚀 Quick Start

```bash
# 1. Avvia il monitor
cd "/Users/mac/Desktop/WASABI OFFERS TECH/email reverse agent"
./start_monitor.sh

# 2. Verifica stato
./monitor_status.sh

# 3. Vedi log in tempo reale
tail -f monitor.log

# 4. Apri dashboard
# http://localhost:5000/monitor

# Quando vuoi fermare:
./stop_monitor.sh
```

---

## ⚡ Processo Completo

```
┌─────────────────────────────────────────┐
│  📡 Email Monitor (background)          │
│  ↓ Ogni 15 minuti                       │
│  1. Controlla Gmail                     │
│  2. Trova nuove email                   │
│  3. Scarica dettagli                    │
│  4. Analizza con OpenAI                 │
│  5. Salva in database                   │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│  🌐 Dashboard Web (http://localhost:5000)│
│  • Vista Tabella (nuove email visibili)│
│  • Swipe email (disponibili subito)    │
│  • Statistiche (aggiornate auto)       │
└─────────────────────────────────────────┘
```

---

## 🎉 Vantaggi

✅ **Zero lavoro manuale** - Tutto automatico
✅ **Sempre aggiornato** - Database sempre fresh
✅ **Analisi immediate** - Nuove email già categorizzate
✅ **Swipe pronto** - Ogni nuova email già analizzabile
✅ **Multi-account** - Supporta account multipli
✅ **Resiliente** - Riprende automaticamente dopo errori

---

## 📞 Supporto

Se il monitor ha problemi:

1. Controlla `monitor.log`
2. Verifica autenticazione Gmail
3. Controlla credito OpenAI
4. Restart monitor: `./stop_monitor.sh && ./start_monitor.sh`

---

**Il monitor è pronto! Avvialo con `./start_monitor.sh`** 🚀

