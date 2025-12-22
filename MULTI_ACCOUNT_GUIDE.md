# 🔄 Guida Multi-Account

Sistema per gestire multipli account Gmail con diverse credenziali OAuth 2.0.

---

## ✅ Account Configurati

### Account 1 - Wasabi Offers (ATTIVO)
- **Email**: `your-email@gmail.com`
- **Client ID**: `YOUR_CLIENT_ID.apps.googleusercontent.com`
- **Client Secret**: `YOUR_CLIENT_SECRET`
- **Token**: `token_account1.pickle`

### Account 2
- **Email**: (da configurare)
- **Client ID**: `YOUR_SECOND_CLIENT_ID.apps.googleusercontent.com`
- **Client Secret**: `YOUR_SECOND_CLIENT_SECRET`
- **Token**: `token_account2.pickle`

---

## 🚀 Comandi Veloci

### Cambio Account Rapido
```bash
cd "/Users/mac/Desktop/WASABI OFFERS TECH/email reverse agent"
source venv/bin/activate
python switch_account.py
```

### Gestione Completa Account
```bash
python account_manager.py
```

**Azioni disponibili:**
1. Seleziona account attivo
2. Aggiungi nuovo account
3. Rimuovi account
4. Genera credentials.json per account attivo
5. Mostra account attivo

---

## 📋 Come Funziona

### 1. File di Configurazione: `google_accounts.json`

Contiene tutti gli account configurati:
```json
{
  "accounts": [
    {
      "name": "Account 1 - Wasabi Offers",
      "email": "maru@wasabioffers.com",
      "client_id": "...",
      "client_secret": "...",
      "token_file": "token_account1.pickle",
      "active": true
    },
    {
      "name": "Account 2",
      "email": "",
      "client_id": "...",
      "client_secret": "...",
      "token_file": "token_account2.pickle",
      "active": false
    }
  ]
}
```

### 2. Token Separati

Ogni account ha il suo token:
- `token_account1.pickle` - Account 1
- `token_account2.pickle` - Account 2
- `token_account3.pickle` - Account 3 (se aggiunto)

### 3. Credentials.json Dinamico

Il file `credentials.json` viene **generato automaticamente** per l'account attivo quando:
- Cambi account con `switch_account.py`
- Esegui `process_emails.py`
- Esegui `test_connection.py` (con account manager)

---

## 🎯 Workflow Tipico

### Scenario 1: Usare Account 1 (già attivo)

```bash
# L'account 1 è già attivo, quindi:
python process_emails.py
```

### Scenario 2: Cambiare ad Account 2

```bash
# 1. Cambia account
python switch_account.py
# Seleziona: 2

# 2. Configura i redirect URI su Google Cloud Console
# Per Account 2, aggiungi: http://localhost:8080/

# 3. Estrai le email
python process_emails.py
```

### Scenario 3: Aggiungere Account 3

```bash
# 1. Apri il gestore
python account_manager.py

# 2. Seleziona: [2] Aggiungi nuovo account
# Inserisci:
#   - Nome: Account 3 - Marketing
#   - Email: marketing@example.com
#   - Client ID: ...
#   - Client Secret: ...

# 3. Attiva il nuovo account
#    Seleziona: [1] Seleziona account attivo
#    Scegli: 3

# 4. Genera credentials
#    Seleziona: [4] Genera credentials.json

# 5. Esci e usa l'account
#    Seleziona: [0] Esci
python process_emails.py
```

---

## 🔐 Configurazione Redirect URI

**IMPORTANTE**: Ogni Client ID deve avere configurato su Google Cloud Console:

```
http://localhost:8080/
http://localhost:8080
```

### Per Account 1:
- Vai su: https://console.cloud.google.com/apis/credentials
- Trova Client ID: `1095822054176-uligfuunb8tgt9urbdrjmcs48u4str3a`
- Aggiungi redirect URI: `http://localhost:8080/`

### Per Account 2:
- Vai su: https://console.cloud.google.com/apis/credentials
- Trova Client ID: `273042617440-gc2gmmclbaunpkrdij163b3uj6gju8b7`
- Aggiungi redirect URI: `http://localhost:8080/`

---

## 💾 Database Separati (Opzionale)

Se vuoi database separati per ogni account:

### Opzione 1: Database Unico (Consigliato)
Tutte le email da tutti gli account vanno in `emails.db`.
Puoi distinguerle per sender.

### Opzione 2: Database Separati
Modifica `process_emails.py`:
```python
# Dopo la riga con AccountManager
active = account_mgr.get_active_account()
db_file = f"emails_{active['name'].replace(' ', '_')}.db"
db = EmailDatabase(db_path=db_file)
```

---

## 📊 Visualizzare Email da Tutti gli Account

La dashboard web (`python app.py`) mostra tutte le email dal database `emails.db`, indipendentemente dall'account di origine.

**Pro Tip**: Il sender email ti permette di identificare da quale account Gmail provengono le email.

---

## 🛠️ Comandi Utili

### Vedere Account Attivo
```bash
python -c "from account_manager import AccountManager; m = AccountManager(); a = m.get_active_account(); print(f'{a[\"name\"]} - {a[\"email\"]}')"
```

### Resettare Autenticazione Account 2
```bash
rm token_account2.pickle
python switch_account.py  # Seleziona account 2
python test_connection.py
```

### Esportare Configurazione
```bash
cat google_accounts.json
```

---

## ⚠️ Troubleshooting

### "redirect_uri_mismatch" per Account 2
- ✅ Configura `http://localhost:8080/` su Google Cloud Console
- ✅ Aspetta 1-2 minuti per la propagazione
- ✅ Elimina `token_account2.pickle` e riautentica

### Account non cambia
- ✅ Usa `python switch_account.py` invece di modificare manualmente
- ✅ Verifica che `credentials.json` sia stato rigenerato
- ✅ Controlla che `google_accounts.json` abbia `"active": true` sull'account corretto

### File credentials.json non trovato
- ✅ Esegui: `python switch_account.py` e seleziona l'account
- ✅ Oppure: `python account_manager.py` → [4] Genera credentials.json

---

## 🎉 Quick Reference

```bash
# Cambia account
python switch_account.py

# Gestisci account (aggiungi/rimuovi/configura)
python account_manager.py

# Estrai email con account attivo
python process_emails.py

# Testa connessione account attivo
python test_connection.py

# Visualizza dashboard
python app.py
```

---

## 📝 Note Importanti

1. **Un account attivo alla volta**: Solo un account può essere attivo contemporaneamente
2. **Token persistenti**: I token sono salvati e non richiedono riautenticazione a ogni utilizzo
3. **Credenziali sicure**: Il file `google_accounts.json` è in `.gitignore` - non condividerlo!
4. **Database condiviso**: Le email da tutti gli account vanno nello stesso database (se preferito)
5. **Porta fissa**: Tutti gli account usano porta 8080 per OAuth (configurabile se necessario)

---

**Pronto per usare multipli account Gmail! 🚀**

