# ☁️ Guida Setup Supabase

Integrazione cloud per sincronizzare automaticamente le email analizzate su Supabase.

---

## 🎯 Perché Supabase?

- ☁️ **Cloud Storage** - Accedi ai dati da ovunque
- 🔄 **Real-time Sync** - Aggiornamenti istantanei
- 🌐 **API REST automatica** - Supabase genera API per te
- 📊 **Dashboard Web** - Esplora dati con interfaccia grafica
- 🔐 **Sicuro** - Row Level Security (RLS)
- 💰 **Gratuito** - 500 MB database, 2GB bandwidth/mese

---

## 🚀 Setup Supabase

### **Step 1: Crea un Progetto Supabase**

1. Vai su: https://app.supabase.com/
2. Click **"New Project"**
3. Compila:
   - **Name**: `email-swiper-agent`
   - **Database Password**: Crea una password sicura
   - **Region**: Scegli la più vicina (es: Europe West)
4. Click **"Create new project"**
5. ⏰ Aspetta 2-3 minuti per il setup

---

### **Step 2: Crea le Tabelle**

1. Nel menu laterale, vai su **"SQL Editor"**
2. Click **"New query"**
3. Copia e incolla questo SQL:

```sql
-- Tabella principale email
CREATE TABLE IF NOT EXISTS emails (
    id BIGSERIAL PRIMARY KEY,
    email_id TEXT UNIQUE NOT NULL,
    thread_id TEXT,
    sender TEXT,
    subject TEXT,
    email_body TEXT,
    snippet TEXT,
    date TEXT,
    time_usa TEXT,
    notes TEXT,
    email_type TEXT,
    campaign_type TEXT,
    pricing_extract TEXT,
    target_audience TEXT,
    product_mentioned TEXT,
    retention TEXT,
    funnel_stage TEXT,
    urls JSONB DEFAULT '[]'::jsonb,
    labels JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indici per performance
CREATE INDEX IF NOT EXISTS idx_emails_sender ON emails(sender);
CREATE INDEX IF NOT EXISTS idx_emails_type ON emails(email_type);
CREATE INDEX IF NOT EXISTS idx_emails_date ON emails(date);
CREATE INDEX IF NOT EXISTS idx_emails_created ON emails(created_at);

-- Tabella prodotti
CREATE TABLE IF NOT EXISTS my_products (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    brief TEXT,
    documents_text TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabella documenti prodotto
CREATE TABLE IF NOT EXISTS product_documents (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT REFERENCES my_products(id) ON DELETE CASCADE,
    filename TEXT,
    file_type TEXT,
    extracted_text TEXT,
    file_size INTEGER,
    uploaded_at TIMESTAMP DEFAULT NOW()
);

-- Tabella swipe email
CREATE TABLE IF NOT EXISTS email_swipes (
    id BIGSERIAL PRIMARY KEY,
    email_id TEXT,
    product_id BIGINT REFERENCES my_products(id),
    swipe_notes TEXT,
    swiped_subject TEXT,
    swiped_body TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Commenti per documentazione
COMMENT ON TABLE emails IS 'Email estratte e analizzate da Gmail con AI';
COMMENT ON TABLE my_products IS 'Prodotti dell''utente con brief e documenti';
COMMENT ON TABLE email_swipes IS 'Swipe email salvati';
```

4. Click **"Run"** (o F5)
5. Verifica che vedi: **"Success. No rows returned"**

---

### **Step 3: Ottieni le Credenziali**

1. Nel menu laterale, vai su **"Settings"** (icona ingranaggio)
2. Click **"API"**
3. Copia:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon public**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

---

### **Step 4: Configura il File .env**

Aggiungi queste righe al tuo file `.env`:

```bash
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-public-key-here
ENABLE_SUPABASE=true
```

---

## 📦 Installazione Dipendenza

```bash
cd "/Users/mac/Desktop/WASABI OFFERS TECH/email reverse agent"
source venv/bin/activate
pip install supabase
```

---

## 🔄 Sincronizzazione

### **Opzione 1: Sync Iniziale (Una volta)**

Sincronizza tutte le email esistenti:

```bash
python sync_to_supabase.py
```

**Cosa fa:**
- Legge tutte le email da SQLite locale
- Le carica su Supabase
- Sincronizza anche i prodotti

---

### **Opzione 2: Monitor con Auto-Sync (Continuo)**

Monitor che salva automaticamente sia locale che cloud:

```bash
python auto_sync_monitor.py
```

O in background:

```bash
# Modifica start_monitor.sh per usare auto_sync_monitor.py
nohup python auto_sync_monitor.py > monitor.log 2>&1 &
```

**Cosa fa:**
- Controlla Gmail ogni 15 minuti
- Analizza nuove email con AI
- Salva in SQLite (locale)
- Sincronizza su Supabase (cloud)
- Log di tutte le operazioni

---

## 🎯 Workflow Completo

```
┌─────────────────────────┐
│      GMAIL INBOX        │
│   (Nuova email arriva)  │
└───────────┬─────────────┘
            ↓
┌─────────────────────────┐
│   AUTO-SYNC MONITOR     │
│  (Controlla ogni 15min) │
└───────────┬─────────────┘
            ↓
┌─────────────────────────┐
│   OPENAI ANALYSIS       │
│  (Categorizza con AI)   │
└───────────┬─────────────┘
            ↓
     ┌──────┴──────┐
     ↓             ↓
┌─────────┐   ┌──────────┐
│ SQLite  │   │ Supabase │
│ (Local) │   │ (Cloud)  │
└────┬────┘   └────┬─────┘
     │             │
     ↓             ↓
┌─────────────────────────┐
│   DASHBOARD WEB         │
│ (Visualizza + Swipe)    │
└─────────────────────────┘
```

---

## 📊 Vantaggi Dual Storage

### **SQLite (Locale)**
- ⚡ Velocissimo
- 📍 Offline access
- 🔒 Privacy totale
- 💾 Backup facile

### **Supabase (Cloud)**
- ☁️ Accesso da ovunque
- 👥 Condivisione team
- 🔄 Sync multi-device
- 📊 Dashboard Supabase
- 🔌 API REST automatiche

---

## 🎨 Features Supabase

### **1. Dashboard Supabase**

Vai su: https://app.supabase.com/project/_/editor

- 📊 **Table Editor** - Vedi/modifica email come Excel
- 🔍 **Filters** - Filtra per sender, tipo, data
- 📈 **SQL Editor** - Query personalizzate
- 📥 **Export** - Scarica CSV/JSON

### **2. API REST Automatica**

Supabase genera automaticamente API REST:

```javascript
// Esempio: Recupera email da JavaScript
const { data } = await supabase
  .from('emails')
  .select('*')
  .eq('email_type', 'marketing')
  .limit(100);
```

### **3. Real-time Subscriptions**

```javascript
// Esempio: Ascolta nuove email in tempo reale
supabase
  .from('emails')
  .on('INSERT', payload => {
    console.log('Nuova email!', payload.new);
  })
  .subscribe();
```

---

## 🔧 Configurazione Avanzata

### **Disabilitare Supabase Temporaneamente**

Nel file `.env`:
```bash
ENABLE_SUPABASE=false
```

### **Sync Solo Locale**

Usa il monitor originale:
```bash
python email_monitor.py
```

### **Sync Manuale (quando vuoi)**

```bash
python sync_to_supabase.py
```

---

## 🧪 Test Connessione

```bash
python -c "from supabase_sync import SupabaseSync; s = SupabaseSync(); s.test_connection()"
```

**Output atteso:**
```
✅ Connesso a Supabase
✅ Connessione Supabase OK - X record test
```

---

## 📋 SQL Queries Utili

### **Contare email per sender:**
```sql
SELECT sender, COUNT(*) as count
FROM emails
GROUP BY sender
ORDER BY count DESC;
```

### **Email con pricing/offerte:**
```sql
SELECT sender, subject, pricing_extract, date
FROM emails
WHERE pricing_extract IS NOT NULL AND pricing_extract != ''
ORDER BY date DESC;
```

### **Email per funnel stage:**
```sql
SELECT funnel_stage, COUNT(*) as count
FROM emails
GROUP BY funnel_stage;
```

### **Ultime 10 email:**
```sql
SELECT sender, subject, date, email_type
FROM emails
ORDER BY created_at DESC
LIMIT 10;
```

---

## 🔐 Row Level Security (RLS)

Per abilitare la sicurezza:

```sql
-- Abilita RLS
ALTER TABLE emails ENABLE ROW LEVEL SECURITY;
ALTER TABLE my_products ENABLE ROW LEVEL SECURITY;

-- Policy esempio: solo il proprietario può vedere
CREATE POLICY "Users can view own emails"
ON emails FOR SELECT
USING (auth.uid() = user_id);
```

---

## 💡 Best Practices

1. **Sync Iniziale**
   ```bash
   python sync_to_supabase.py
   ```

2. **Monitor Continuo**
   ```bash
   python auto_sync_monitor.py &
   ```

3. **Backup Regolari**
   ```bash
   # SQLite locale
   cp emails.db backup/emails_$(date +%Y%m%d).db
   
   # Supabase ha backup automatici
   ```

4. **Monitora Quota**
   - Dashboard Supabase → Settings → Usage
   - Free tier: 500 MB database, 2 GB bandwidth/mese

---

## 📊 Monitoring

### **Controlla Stato Sync:**

```bash
# Via script
./monitor_status.sh

# Via Python
python -c "from supabase_sync import SupabaseSync; s = SupabaseSync(); print(len(s.get_all_emails(limit=1000)))"
```

### **Dashboard Web:**

http://localhost:5000/monitor

---

## 🚨 Troubleshooting

### **"SUPABASE_URL non trovata"**
- Verifica che `.env` contenga le credenziali
- Format: `SUPABASE_URL=https://xxx.supabase.co`

### **"Connection refused"**
- Verifica che il progetto Supabase sia attivo
- Controlla che l'URL sia corretto

### **"Table 'emails' does not exist"**
- Crea le tabelle con lo SQL fornito sopra
- Verifica nello SQL Editor di Supabase

---

## 📞 Support

- Supabase Docs: https://supabase.com/docs
- Supabase Dashboard: https://app.supabase.com/

---

**Setup completo! Le tue email saranno sincronizzate automaticamente nel cloud** ☁️

