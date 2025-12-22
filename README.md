# 📧 E-Mail Swiper Agent

Sistema completo per estrarre, analizzare e fare swipe di email marketing da Gmail usando intelligenza artificiale.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 🎯 Features

- 🔐 **OAuth 2.0 Gmail Integration** - Estrazione sicura delle email
- 🤖 **AI-Powered Analysis** - Categorizzazione automatica con OpenAI GPT-4o
- 📊 **Multi-Account Support** - Gestisci multipli account Gmail
- 📡 **Auto-Monitor** - Rileva e processa automaticamente nuove email
- 🎨 **Email Swipe Generator** - Adatta email per i tuoi prodotti con AI
- 📋 **Excel-Style Dashboard** - Vista tabellare con export CSV/Excel
- 📄 **Document Upload** - Carica PDF/DOCX per estrarre brief prodotti
- 🌐 **Modern Web UI** - Dashboard responsive con Tailwind CSS
- 💾 **SQLite Database** - Storage veloce e organizzato
- 🔗 **REST API** - Integrazione programmatica

---

## 📊 Dashboard Preview

### Funzionalità Principali:

- **📊 Analytics Dashboard** - Statistiche, sender, tipi di email
- **📋 Excel View** - Tabella completa con tutte le email
- **🎨 Swipe Generator** - Vista comparativa originale vs swipata
- **📡 Auto Monitor** - Monitoraggio real-time nuove email
- **🎯 Products Manager** - Gestione prodotti con brief e documenti

---

## 🚀 Quick Start

### 1. Clone del Repository

```bash
git clone https://github.com/maru-mm/e-mail-swiper-agent.git
cd e-mail-swiper-agent
```

### 2. Setup Ambiente

```bash
# Crea ambiente virtuale
python3 -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate

# Installa dipendenze
pip install -r requirements.txt
```

### 3. Configurazione

Crea un file `.env` con le tue credenziali:

```bash
# Gmail OAuth 2.0
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret

# OpenAI API
OPENAI_API_KEY=your_openai_api_key

# Monitor Configuration
CHECK_INTERVAL_MINUTES=15
```

**Ottieni le credenziali:**
- **Gmail OAuth**: [Google Cloud Console](https://console.cloud.google.com/)
- **OpenAI API**: [OpenAI Platform](https://platform.openai.com/)

### 4. Prima Importazione

```bash
python process_emails.py
```

Questo importerà tutte le tue email e le analizzerà con AI.

### 5. Avvia la Dashboard

```bash
python app.py
```

Vai su: **http://localhost:5000**

---

## 📚 Documentazione

- 📖 [Quick Start Guide](QUICK_START.md) - Guida rapida
- 📡 [Monitor Guide](MONITOR_GUIDE.md) - Monitoraggio automatico
- 🔄 [Multi-Account Guide](MULTI_ACCOUNT_GUIDE.md) - Gestione account multipli
- 🚀 [SaaS Overview](README_SAAS.md) - Panoramica completa
- 📡 [API Documentation](API_DOCUMENTATION.md) - REST API reference

---

## 🎨 Email Swipe API

### REST API Endpoint

```bash
POST /api/v1/swipe
Content-Type: application/json

{
  "rawText": "Email originale da swipare",
  "productDetails": "Brief dettagliato del tuo prodotto"
}
```

### Esempio JavaScript

```javascript
fetch('/api/v1/swipe', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    rawText: 'Your deal expires tonight\n\nGet 50% off...',
    productDetails: 'My SaaS Platform - Project management for teams'
  })
})
.then(res => res.json())
.then(data => console.log(data.swiped));
```

Leggi [API_DOCUMENTATION.md](API_DOCUMENTATION.md) per dettagli completi.

---

## 📦 Architettura

```
┌─────────────────────────────────────────────────────┐
│                 GMAIL ACCOUNTS                      │
│              (OAuth 2.0 Multi-Account)              │
└──────────────────┬──────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────┐
│              EMAIL EXTRACTOR                        │
│         (Auto-Monitor ogni 15 min)                  │
└──────────────────┬──────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────┐
│               AI ANALYZER                           │
│        (OpenAI GPT-4o categorization)               │
└──────────────────┬──────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────┐
│             SQLite DATABASE                         │
│   (Emails, Products, Documents, Swipes)             │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        ↓                     ↓
┌──────────────┐     ┌──────────────────┐
│  WEB UI      │     │   REST API       │
│  (Flask +    │     │   (/api/v1/...)  │
│   Tailwind)  │     │                  │
└──────────────┘     └──────────────────┘
```

---

## 🔧 Tecnologie

- **Backend:** Python 3.9+, Flask
- **AI:** OpenAI GPT-4o
- **Database:** SQLite
- **Frontend:** Tailwind CSS, Vanilla JS
- **Email:** Gmail API
- **Document Processing:** PyPDF2, python-docx
- **Scheduling:** schedule library

---

## 📋 Campi Estratti per Email

Ogni email viene analizzata e categorizzata automaticamente:

- **Sender** - Mittente
- **Subject** - Oggetto
- **Body** - Corpo completo
- **Date/Time** - Data e ora
- **Email Type** - marketing, transactional, promotion, etc.
- **Campaign Type** - seasonal, abandoned cart, win-back, etc.
- **Funnel Stage** - awareness, consideration, conversion, retention
- **Pricing Extract** - Offerte, sconti, prezzi
- **Target Audience** - Audience identificata
- **Product Mentioned** - Prodotto menzionato
- **URLs** - Tutti i link estratti
- **AI Notes** - Insights generati dall'AI

---

## 🎯 Use Cases

### **1. Competitive Analysis**
- Monitora email dei competitor
- Analizza strategie e campagne
- Identifica pattern vincenti

### **2. Email Swipe File**
- Costruisci una libreria di email efficaci
- Categorizza per tipo e funnel stage
- Swipa per i tuoi prodotti

### **3. Marketing Research**
- Studia tone of voice e copywriting
- Analizza pricing e offerte
- Identifica target audience

### **4. Automation**
- Monitora automaticamente nuove email
- Analisi AI in tempo reale
- Database sempre aggiornato

---

## 🔐 Sicurezza

⚠️ **IMPORTANTE:** Non committare mai:
- `credentials.json`
- `token*.pickle`
- `.env`
- `google_accounts.json`
- File in `uploads/`

Il `.gitignore` è configurato per proteggerti, ma verifica sempre prima di fare push.

---

## 📊 Costi Stimati

### OpenAI API (GPT-4o)
- **Analisi email:** ~$0.001 per email
- **Swipe generation:** ~$0.01-0.03 per swipe
- **Monitor automatico:** ~$3-10/mese (dipende dal volume)

### Gmail API
- **Gratuito** fino a 1 miliardo di quota/mese
- Ampiamente sufficiente per uso personale/aziendale

---

## 🛠️ Troubleshooting

### Gmail OAuth Error 403
- Aggiungi la tua email come "Utente di test" su Google Cloud Console
- Verifica redirect URI: `http://localhost:8080/`

### OpenAI API Error
- Verifica la chiave API in `.env`
- Controlla credito su https://platform.openai.com/usage

### Monitor non funziona
- Verifica autenticazione Gmail: `python test_connection.py`
- Controlla log: `tail -f monitor.log`

Leggi le guide complete nella cartella docs.

---

## 📄 License

MIT License - Vedi [LICENSE](LICENSE) per dettagli

---

## 👨‍💻 Author

**WASABI OFFERS TECH**

---

## 🙏 Credits

Costruito con:
- [Google Gmail API](https://developers.google.com/gmail/api)
- [OpenAI GPT-4](https://openai.com/)
- [Flask](https://flask.palletsprojects.com/)
- [Tailwind CSS](https://tailwindcss.com/)

---

## 🚀 Contributing

Pull requests benvenute! Per modifiche importanti, apri prima un issue.

---

## ⭐ Star this repo

Se trovi questo progetto utile, lascia una stella! ⭐

---

**Made with ❤️ for email marketers and copywriters**
