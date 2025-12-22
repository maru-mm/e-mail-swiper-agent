# 🚀 QUICK START GUIDE

## ✅ Sistema Pronto!

Tutto è configurato e pronto all'uso:
- ✅ Ambiente virtuale creato
- ✅ Dipendenze installate
- ✅ Gmail OAuth 2.0 configurato
- ✅ OpenAI API configurata e testata
- ✅ Database schema pronto
- ✅ Dashboard web pronta

---

## 📋 Comandi Veloci

### 1️⃣ Estrai e Analizza TUTTE le Email

```bash
cd "/Users/mac/Desktop/WASABI OFFERS TECH/email reverse agent"
source venv/bin/activate
python process_emails.py
```

**Cosa fa:**
- Si connette a Gmail (ti chiederà di autorizzare se è la prima volta)
- Estrae TUTTE le 146 email dall'account `maru@wasabioffers.com`
- Analizza ogni email con OpenAI AI per estrarre:
  - Email Type
  - Campaign Type
  - Funnel Stage
  - Pricing/Offers
  - Target Audience
  - Product Mentioned
  - AI Insights
  - URLs
- Salva tutto nel database `emails.db`

⏱️ **Tempo stimato**: ~10-15 minuti per 146 email

---

### 2️⃣ Avvia la Dashboard Web

```bash
cd "/Users/mac/Desktop/WASABI OFFERS TECH/email reverse agent"
source venv/bin/activate
python app.py
```

Poi apri il browser su: **http://localhost:5000**

**Cosa puoi fare:**
- 📊 Visualizzare statistiche generali
- 👥 Vedere tutti i sender con conteggio email
- 📧 Cliccare su un sender per vedere tutte le sue email
- 🔍 Filtrare per tipo, campaign, funnel stage
- 💰 Vedere prezzi/offerte estratti
- 🔗 Visualizzare tutti i link delle email
- 📝 Leggere gli insights generati dall'AI

---

## 🎯 Workflow Completo

### Step 1: Test Connessioni (Opzionale)

```bash
# Test Gmail
python test_connection.py

# Test OpenAI
python test_openai.py
```

### Step 2: Estrazione e Analisi

```bash
python process_emails.py
```

Conferma con `s` quando richiesto.

### Step 3: Visualizza Dashboard

```bash
python app.py
```

Apri: http://localhost:5000

---

## 📊 Cosa Vedrai

### Homepage Dashboard
```
┌─────────────────────────────────────────┐
│  📊 STATISTICHE                          │
│  • Totale Email: 146                    │
│  • Sender Unici: X                      │
│  • Marketing: XX                        │
│  • Transactional: XX                    │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  👥 LISTA SENDER                         │
│  ┌───────────────────────────────────┐  │
│  │ Bioma Health           45 email   │  │
│  │ Psychic Marie          23 email   │  │
│  │ Lady Soraya            12 email   │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### Vista Sender
```
┌─────────────────────────────────────────┐
│  Email da: Bioma Health                  │
│  [Filtri: Tipo | Stage]                 │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  📧 EMAIL #1                             │
│  Subject: Your 120 kg deal disappears    │
│  [marketing] [conversion] [80% OFF]     │
│                                          │
│  💡 AI Insight: Urgent promo with       │
│     countdown timer targeting weight    │
│     management audience                 │
│                                          │
│  🎯 Target: Weight loss prospects       │
│  💰 Pricing: 80% OFF, expires midnight  │
│  🔗 URLs: 5 links                       │
│                                          │
│  [Vedi dettagli completi →]             │
└─────────────────────────────────────────┘
```

---

## 🎨 Design Features

- **Tailwind CSS** - Design moderno e responsive
- **Color-coded badges** - Categorizzazione visuale
- **Real-time filters** - Filtra per tipo/stage
- **Modal views** - Visualizza email complete
- **Search** - Cerca per keyword
- **Statistics cards** - Metriche in evidenza

---

## 📁 Files Creati

```
✅ gmail_extractor.py      - Estrazione da Gmail
✅ email_analyzer.py        - Analisi AI con OpenAI
✅ database.py              - Gestione database SQLite
✅ process_emails.py        - Script principale
✅ app.py                   - Web app Flask
✅ templates/index.html     - Homepage dashboard
✅ templates/sender.html    - Vista email sender
✅ test_openai.py          - Test connessione OpenAI
✅ emails.db               - Database (dopo process)
```

---

## 💡 Pro Tips

### Estrazione Parziale (Test)
Per testare prima con poche email:

```python
# In process_emails.py, modifica la riga:
emails = extractor.extract_all_emails(max_results=10)  # Solo 10 email
```

### Export CSV
Le email sono in SQLite, puoi esportarle:

```bash
sqlite3 emails.db
.headers on
.mode csv
.output emails_export.csv
SELECT * FROM emails;
.quit
```

### Riavvia Analisi
Per re-analizzare le email (se migliori il prompt):

```bash
rm emails.db  # Elimina DB
python process_emails.py  # Ri-estrai e ri-analizza
```

---

## 🔥 Next Steps

1. **Esegui** `python process_emails.py` per importare le email
2. **Avvia** `python app.py` per vedere la dashboard
3. **Esplora** i dati per sender
4. **Filtra** per tipo di email e funnel stage
5. **Estrai insights** per migliorare le tue campagne

---

## 📞 Supporto

Se qualcosa non funziona:

1. **Verifica ambiente virtuale**: `source venv/bin/activate`
2. **Verifica dipendenze**: `pip list`
3. **Test connessioni**: 
   - `python test_connection.py` (Gmail)
   - `python test_openai.py` (OpenAI)
4. **Check logs**: Leggi gli errori in console

---

**🎉 Pronto? Parti con Step 1!**

```bash
cd "/Users/mac/Desktop/WASABI OFFERS TECH/email reverse agent"
source venv/bin/activate
python process_emails.py
```

