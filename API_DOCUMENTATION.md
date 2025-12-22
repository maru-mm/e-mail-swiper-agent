# 📡 API Documentation - Email Swipe System

API REST per generare swipe di email marketing usando AI.

---

## 🔗 Base URL

```
http://localhost:5000
```

---

## 📬 Endpoints

### **POST /api/v1/swipe**

Genera uno swipe di un'email adattandola per un prodotto specifico.

#### **Request**

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "rawText": "Original email text (subject + body)",
  "productDetails": "Detailed product description and brief"
}
```

**Parametri:**

| Campo | Tipo | Richiesto | Descrizione |
|-------|------|-----------|-------------|
| `rawText` | string | ✅ | Testo completo dell'email originale (subject line + body) |
| `productDetails` | string | ✅ | Brief dettagliato del tuo prodotto (nome, descrizione, USP, target audience, tone of voice) |

#### **Response**

**Success (200):**
```json
{
  "success": true,
  "rawText": "Original email text",
  "productDetails": "Product description",
  "swiped": "Generated email copy adapted for your product",
  "usedAI": true,
  "aiProvider": "OpenAI GPT-4o",
  "timestamp": "2024-12-17T16:00:00.000Z",
  "metadata": {
    "subject": "Swiped subject line",
    "body": "Swiped body text",
    "changes": [
      {
        "type": "hook",
        "original": "Original hook",
        "new": "New hook",
        "reasoning": "Why changed"
      }
    ],
    "key_insights": "Strategy explanation"
  }
}
```

**Error (400/500):**
```json
{
  "success": false,
  "error": "Error description",
  "timestamp": "2024-12-17T16:00:00.000Z"
}
```

---

## 📝 Examples

### **Example 1: JavaScript/Fetch**

```javascript
fetch('http://localhost:5000/api/v1/swipe', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    rawText: `Your 120 kg deal disappears tonight

76% sold — claim your 80% OFF before midnight.
Your 120 kg deal disappears tonight.
Welcome to Bioma Health...`,
    
    productDetails: `Product Name: My Fitness App
Description: Premium fitness tracking app with AI-powered meal plans
Target Audience: Women 25-45 interested in weight management
USP: Personalized AI coach, 30-day guarantee, science-backed
Tone: Friendly, empowering, motivational`
  })
})
.then(res => res.json())
.then(data => {
  console.log('Swipe generated:', data.swiped);
  console.log('AI Provider:', data.aiProvider);
  console.log('Changes:', data.metadata.changes);
});
```

### **Example 2: cURL**

```bash
curl -X POST http://localhost:5000/api/v1/swipe \
  -H "Content-Type: application/json" \
  -d '{
    "rawText": "Hey! Want to know the secret?\n\nDiscover our amazing product...",
    "productDetails": "A premium fitness app for busy professionals"
  }'
```

### **Example 3: Python**

```python
import requests

response = requests.post('http://localhost:5000/api/v1/swipe', json={
    'rawText': """Your deal expires tonight
    
    Don't miss this limited-time offer!
    Get 50% OFF our premium product...""",
    
    'productDetails': """
    Product: My SaaS Platform
    Description: Project management tool for remote teams
    Target: Startups and small businesses
    USP: Simple, affordable, integrates with everything
    Tone: Professional yet friendly
    """
})

data = response.json()

if data['success']:
    print("Swiped Email:")
    print(data['swiped'])
    print(f"\nGenerated using: {data['aiProvider']}")
else:
    print(f"Error: {data['error']}")
```

---

## 🎯 Input Format Best Practices

### **rawText:**

**Formato consigliato:**
```
[Subject Line]

[Email Body completo]
```

**Esempio:**
```
Your 120 kg deal disappears tonight

Hey there,

76% sold — claim your 80% OFF before midnight.
Your 120 kg deal disappears tonight.

Welcome to Bioma Health, where science meets nature...

[CTA: Shop Now]

Unsubscribe | 505 Montgomery Street, San Francisco
```

### **productDetails:**

**Formato consigliato:**
```
Product Name: [Nome]
Description: [Descrizione breve]
Target Audience: [Chi è il target]
USP (Unique Selling Points): [Cosa rende unico il prodotto]
Tone of Voice: [Come vuoi comunicare]
Key Benefits: [Benefici principali]
Pricing: [Modello di prezzo se rilevante]
```

**Esempio:**
```
Product Name: FitTrack Pro
Description: AI-powered fitness tracking app with personalized coaching
Target Audience: Women 25-45, health-conscious, busy professionals
USP: Only app with real-time AI coach, science-backed meal plans, 98% user satisfaction
Tone of Voice: Empowering, friendly, scientific but accessible
Key Benefits: Lose weight sustainably, custom meal plans, 24/7 AI support
Pricing: $29/month, 30-day money-back guarantee
```

---

## 🤖 AI Processing

### **Cosa Fa l'AI:**

1. **Analizza** la struttura dell'email originale
2. **Identifica** hook, benefits, urgency tactics, CTA
3. **Estrae** lo stile e il tone of voice
4. **Legge** il brief del tuo prodotto
5. **Adatta** tutti gli elementi per il tuo prodotto
6. **Mantiene** la struttura che funziona
7. **Genera** un'email naturale e convincente

### **Modello AI:**

- **Provider:** OpenAI
- **Model:** GPT-4o
- **Temperature:** 0.7 (bilanciamento creatività/coerenza)
- **Output:** JSON strutturato

### **Costo per Richiesta:**

- ~**$0.01 - 0.03** per swipe (dipende dalla lunghezza)
- Include analisi completa e generazione

---

## 📊 Response Metadata

Il campo `metadata` contiene informazioni dettagliate:

```json
{
  "metadata": {
    "subject": "Subject line swipato separato",
    "body": "Body swipato separato",
    "changes": [
      {
        "type": "hook",
        "original": "Your 120 kg deal...",
        "new": "Your fitness journey starts...",
        "reasoning": "Adapted to focus on journey vs weight loss number"
      },
      {
        "type": "benefit",
        "original": "Science-backed formula",
        "new": "AI-powered coaching",
        "reasoning": "Aligned with product's main USP"
      }
    ],
    "key_insights": "Maintained urgency and scarcity tactics while adapting benefits to match AI coaching angle instead of supplements"
  }
}
```

---

## 🔐 Authentication

Attualmente: **Nessuna autenticazione richiesta** (uso locale)

Per produzione, considera di aggiungere:
- API Key authentication
- Rate limiting
- CORS restrictions

---

## ⚡ Performance

- **Simulato:** ~1-2 secondi
- **Con AI (GPT-4o):** ~5-10 secondi
- **Rate Limit:** Nessun limite (OpenAI default: 10,000 RPM)

---

## 🧪 Testing

### **Test con Postman**

1. Importa questa richiesta:
   ```
   POST http://localhost:5000/api/v1/swipe
   Content-Type: application/json
   ```

2. Body:
   ```json
   {
     "rawText": "Your deal expires\n\nGet 50% off today!",
     "productDetails": "My Product - A premium tool"
   }
   ```

### **Test con Browser Console**

Vai su http://localhost:5000 e nella console:

```javascript
fetch('/api/v1/swipe', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    rawText: 'Your deal expires tonight\n\nGet 50% off!',
    productDetails: 'My SaaS Platform for teams'
  })
})
.then(r => r.json())
.then(d => console.log(d));
```

---

## 📋 Complete API Reference

| Endpoint | Method | Descrizione |
|----------|--------|-------------|
| `/api/v1/swipe` | POST | Genera swipe email (standard API) |
| `/api/swipe/generate` | POST | Genera swipe (uso interno UI) |
| `/api/products` | GET | Lista tutti i prodotti |
| `/api/products` | POST | Crea nuovo prodotto |
| `/api/products/:id` | PUT | Aggiorna prodotto |
| `/api/products/:id` | DELETE | Elimina prodotto |
| `/api/products/:id/upload` | POST | Upload documento |
| `/api/products/:id/documents` | GET | Lista documenti prodotto |
| `/api/senders` | GET | Lista sender con conteggi |
| `/api/sender/:email` | GET | Email di un sender |
| `/api/statistics` | GET | Statistiche generali |
| `/api/search` | GET | Cerca email |
| `/api/monitor/status` | GET | Stato monitor email |
| `/api/swipes` | POST | Salva swipe |
| `/api/swipes` | GET | Lista swipe salvati |

---

## 🔧 Configuration

Per abilitare/disabilitare AI in `app.py`:

```python
# Usa AI (OpenAI GPT-4o)
swipe_gen = SwipeGenerator(api_key=OPENAI_API_KEY, use_ai=True)

# Usa simulazione (gratuito, veloce)
swipe_gen = SwipeGenerator(use_ai=False)
```

---

## 📞 Support

Per problemi con l'API:
- Verifica che il server Flask sia attivo: `python app.py`
- Controlla i log del server
- Testa con richieste semplici prima

---

**API pronta all'uso! 🚀**

