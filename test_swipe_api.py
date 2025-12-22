"""
Test dell'API Swipe v1
"""

import requests
import json


def test_swipe_api():
    """
    Testa l'API /api/v1/swipe
    """
    print("="*80)
    print("🧪 TEST API SWIPE v1")
    print("="*80)
    
    # URL dell'API (assicurati che Flask sia in esecuzione)
    url = 'http://localhost:5000/api/v1/swipe'
    
    # Email di esempio (da Bioma Health)
    raw_text = """Your 120 kg deal disappears tonight

Hey there,

76% sold — claim your 80% OFF before midnight.
Your 120 kg deal disappears tonight.

Welcome to Bioma Health, where science meets nature for sustainable weight loss.

Our clinically-proven formula helps you:
• Reduce cravings naturally
• Boost metabolism 24/7
• Feel more energized
• Reach your goal weight

Limited time offer - 80% OFF ends at midnight!

👉 Click here to claim your discount

Don't wait - join thousands who've already transformed their lives.

Team Bioma Health
505 Montgomery Street, San Francisco, CA 94111"""

    # Dettagli del tuo prodotto
    product_details = """Product Name: FitTrack Pro

Description: AI-powered fitness tracking mobile app with personalized workout plans and nutrition coaching

Target Audience: Busy professionals (ages 25-45) who want to get fit but struggle with time and motivation

Unique Selling Points:
- AI coach that learns your preferences and schedule
- 15-minute science-backed workouts
- Meal plans that adapt to your lifestyle
- Real-time progress tracking with wearables
- 30-day money-back guarantee

Tone of Voice: Empowering, modern, tech-savvy but friendly

Key Benefits:
- Fit workouts into your busy schedule
- No gym required - workout anywhere
- Personalized to YOUR goals and body
- Proven results in just 30 days

Pricing: $29/month or $199/year (save 40%)"""

    print("\n📧 Email Originale:")
    print("-" * 60)
    print(raw_text[:200] + "...")
    
    print("\n🎯 Prodotto:")
    print("-" * 60)
    print(product_details[:150] + "...")
    
    print("\n🚀 Invio richiesta all'API...")
    print("⏳ Generazione swipe con AI (può richiedere 5-10 secondi)...\n")
    
    try:
        response = requests.post(
            url,
            headers={'Content-Type': 'application/json'},
            json={
                'rawText': raw_text,
                'productDetails': product_details
            },
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print("="*80)
            print("✅ SWIPE GENERATO CON SUCCESSO!")
            print("="*80)
            
            print(f"\n🤖 AI Provider: {data.get('aiProvider')}")
            print(f"⏱️  Timestamp: {data.get('timestamp')}")
            print(f"🔧 Used AI: {data.get('usedAI')}")
            
            print("\n" + "="*80)
            print("📧 EMAIL SWIPATA:")
            print("="*80)
            print(data.get('swiped', ''))
            
            # Metadata
            metadata = data.get('metadata', {})
            
            if metadata.get('changes'):
                print("\n" + "="*80)
                print("🔄 MODIFICHE APPLICATE:")
                print("="*80)
                for idx, change in enumerate(metadata['changes'], 1):
                    print(f"\n{idx}. Tipo: {change.get('type', 'N/A')}")
                    print(f"   Originale: {change.get('original', '')[:50]}...")
                    print(f"   Nuovo: {change.get('new', '')[:50]}...")
                    print(f"   Motivo: {change.get('reasoning', '')}")
            
            if metadata.get('key_insights'):
                print("\n" + "="*80)
                print("💡 STRATEGIA UTILIZZATA:")
                print("="*80)
                print(metadata['key_insights'])
            
            print("\n" + "="*80)
            print("✅ TEST COMPLETATO!")
            print("="*80)
            
        else:
            print(f"\n❌ Errore HTTP {response.status_code}")
            print(response.json())
    
    except requests.exceptions.ConnectionError:
        print("\n❌ ERRORE: Impossibile connettersi al server")
        print("\n💡 Soluzione:")
        print("   1. Avvia il server Flask: python app.py")
        print("   2. Aspetta che sia pronto (vedrai 'Running on http://...')")
        print("   3. Riprova questo test")
    
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    test_swipe_api()

