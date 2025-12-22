# 📧 Email Analyzer SaaS

Sistema completo per estrarre, analizzare e visualizzare email da Gmail con intelligenza artificiale.

## 🎯 Funzionalità

- ✅ **Estrazione completa** di tutte le email da Gmail tramite OAuth 2.0
- ✅ **Analisi AI** con OpenAI GPT-4 per categorizzare automaticamente:
  - Email Type (marketing, transactional, promotion, etc.)
  - Campaign Type (promo, seasonal, abandoned checkout, etc.)
  - Funnel Stage (awareness, consideration, conversion, etc.)
  - Pricing Extract (offerte, sconti, prezzi)
  - Target Audience
  - Product Mentioned
  - Notes e insights
- ✅ **Database SQLite** per salvare e organizzare le email
- ✅ **Dashboard Web** moderna con Tailwind CSS
- ✅ **Visualizzazione per Sender** con filtri avanzati
- ✅ **Estrazione URL** automatica dalle email
- ✅ **Statistiche** e analytics in tempo reale

## 📊 Campi Estratti per Ogni Email

```
- SENDER
- SUBJECT (OBJECT)
- EMAIL BODY
- DATE
- TIME - USA
- NOTES (AI-generated insights)
- EMAIL TYPE
- CAMPAIGN TYPE
- PRICING EXTRACT
- TARGET AUDIENCE
- PRODUCT MENTIONED
- RETENTION
- FUNNEL STAGE
- URLS (lista completa)
```

## 🚀 Installazione

### 1. Requisiti

- Python 3.9+
- Account Gmail
- API Key di OpenAI
- Credenziali OAuth 2.0 di Google Cloud Console

### 2. Setup Ambiente

```bash
# Naviga nella directory del progetto
cd "/Users/mac/Desktop/WASABI OFFERS TECH/email reverse agent"

# Attiva l'ambiente virtuale
source venv/bin/activate

# Verifica le dipendenze (già installate)
pip list
```

### 3. Configurazione Gmail OAuth 2.0

Le credenziali OAuth 2.0 sono già configurate:
- ✅ Client ID: `1095822054176-uligfuunb8tgt9urbdrjmcs48u4str3a.apps.googleusercontent.com`
- ✅ Client Secret: configurato
- ✅ Redirect URI: `http://localhost:8080/`
- ✅ File: `credentials.json` (già presente)

### 4. Configurazione OpenAI API

La chiave API OpenAI è già configurata nel file `process_emails.py`:
- ✅ API Key: già impostata
- ✅ Modello: GPT-4o-mini (veloce ed economico)

## 📝 Come Usare

### Step 1: Estrai e Analizza le Email

Esegui lo script principale per:
1. Estrarre TUTTE le email da Gmail
2. Analizzarle con OpenAI AI
3. Salvarle nel database

```bash
cd "/Users/mac/Desktop/WASABI OFFERS TECH/email reverse agent"
source venv/bin/activate
python process_emails.py
```

**Nota**: Il processo può richiedere tempo in base al numero di email (circa 2-5 secondi per email).

### Step 2: Avvia la Dashboard Web

```bash
cd "/Users/mac/Desktop/WASABI OFFERS TECH/email reverse agent"
source venv/bin/activate
python app.py
```

Poi apri il browser su: **http://localhost:5000**

## 🖥️ Dashboard Features

### Homepage
- 📊 **Statistiche generali**: totale email, sender unici, breakdown per tipo
- 👥 **Lista sender**: tutti i mittenti con conteggio email
- 🔍 **Ricerca**: cerca per sender, subject, body
- 📈 **Analytics**: visualizza metriche chiave

### Vista Sender
- 📧 **Tutte le email** di uno specifico sender
- 🎯 **Filtri**: per email type e funnel stage
- 💰 **Pricing highlights**: evidenzia offerte e sconti
- 🔗 **URL extraction**: tutti i link contenuti nelle email
- 📝 **AI insights**: note e categorizzazioni automatiche

## 🎨 Interfaccia UI

Dashboard moderna con:
- **Tailwind CSS** per design responsive
- **Card layout** per facile visualizzazione
- **Color-coded badges** per categorizzazione rapida
- **Modal dettaglio** per visualizzare email complete
- **Real-time filtering** per trovare info specifiche

## 📦 Struttura del Progetto

```
email reverse agent/
│
├── gmail_extractor.py          # Modulo per estrarre email da Gmail
├── email_analyzer.py            # Modulo per analizzare email con OpenAI
├── database.py                  # Modulo per gestire il database SQLite
├── process_emails.py            # Script principale per estrazione + analisi
├── app.py                       # Web app Flask
│
├── templates/
│   ├── index.html              # Homepage dashboard
│   └── sender.html             # Vista email per sender
│
├── static/                      # File statici (se necessario)
│
├── credentials.json             # Credenziali OAuth 2.0 (già configurate)
├── token.pickle                 # Token OAuth salvato
├── emails.db                    # Database SQLite (creato automaticamente)
│
├── requirements.txt             # Dipendenze Python
├── .env                         # Variabili d'ambiente (opzionale)
└── .gitignore                  # File da ignorare in Git
```

## 🔧 API Endpoints

La web app Flask espone questi endpoint:

- `GET /` - Homepage con lista sender
- `GET /sender/<sender>` - Vista email per sender specifico
- `GET /api/senders` - JSON: tutti i sender con conteggio
- `GET /api/sender/<sender>` - JSON: tutte le email di un sender
- `GET /api/statistics` - JSON: statistiche generali
- `GET /api/search?q=<query>` - JSON: ricerca email
- `GET /api/emails?limit=<n>` - JSON: tutte le email (con limite opzionale)

## 📊 Esempi di Analisi AI

L'AI categorizza automaticamente le email. Esempi:

### Email Marketing
```json
{
  "email_type": "marketing",
  "campaign_type": "seasonal (Black Friday)",
  "funnel_stage": "conversion",
  "pricing_extract": "80% OFF; expires at midnight",
  "target_audience": "subscribers interested in weight management",
  "product_mentioned": "Bioma Health supplements",
  "notes": "Urgent Black Friday promo with countdown timer"
}
```

### Email Transactional
```json
{
  "email_type": "transactional",
  "campaign_type": "order confirmation",
  "funnel_stage": "onboarding",
  "pricing_extract": "$196.94 total; multiple discounts applied",
  "target_audience": "recent purchasers",
  "product_mentioned": "Psychic Reading package",
  "notes": "Order #50270 confirmation with itemized breakdown"
}
```

## 🎯 Categorizzazioni AI

### Email Types
- `marketing` - Email promozionali
- `transactional` - Conferme ordine, spedizioni
- `promotion` - Offerte speciali, sconti
- `personal` - Email personali
- `recruiting` - Offerte di lavoro
- `product education` - Contenuti educativi
- `onboarding` - Welcome emails
- `retention` - Re-engagement

### Funnel Stages
- `awareness` - Prima fase, scoperta
- `consideration` - Valutazione prodotto
- `conversion` - Acquisto/azione
- `onboarding` - Post-acquisto iniziale
- `retention` - Fidelizzazione cliente

## 💡 Tips & Best Practices

1. **Prima estrazione**: Inizia con un numero limitato di email per testare:
   ```python
   emails = extractor.extract_all_emails(max_results=10)
   ```

2. **Costi OpenAI**: GPT-4o-mini costa circa $0.15 per 1M tokens di input. 100 email ≈ $0.50

3. **Performance**: L'analisi AI richiede 2-5 secondi per email. Per 1000 email: ~1-2 ore

4. **Database**: Il file `emails.db` crescerà con più email. Usa SQLite browser per esplorarlo

5. **Backup**: Fai backup regolari del database: `cp emails.db emails_backup.db`

## 🔐 Sicurezza

- ⚠️ **Non condividere** `credentials.json`, `token.pickle`, `.env`
- ⚠️ Le chiavi API sono in `.gitignore`
- ⚠️ Il database contiene dati sensibili - proteggilo
- ✅ OAuth 2.0 in sola lettura (gmail.readonly scope)

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'openai'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Autenticazione Gmail fallita"
Elimina `token.pickle` e ripeti l'auth:
```bash
rm token.pickle
python process_emails.py
```

### "OpenAI API error"
Verifica la chiave API in `process_emails.py` sia valida

### "Database locked"
Chiudi altre connessioni al DB o riavvia Flask:
```bash
pkill -f "python app.py"
python app.py
```

## 📈 Prossimi Step / Roadmap

- [ ] Export CSV/Excel delle email analizzate
- [ ] Grafici e charts per analytics
- [ ] Filtri avanzati (date range, multiple senders)
- [ ] Autenticazione multi-utente
- [ ] Deploy su server cloud
- [ ] Analisi sentiment
- [ ] Competitor analysis dashboard

## 📄 Licenza

Proprietario - WASABI OFFERS TECH

## 🙋 Supporto

Per domande o problemi, contatta il team di sviluppo.

---

**Creato con ❤️ per analizzare le strategie email di marketing**

