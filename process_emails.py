"""
Script principale per estrarre, analizzare e salvare le email
"""

import os
from dotenv import load_dotenv
from gmail_extractor import GmailExtractor
from email_analyzer import EmailAnalyzer
from database import EmailDatabase
from account_manager import AccountManager

# Carica le variabili d'ambiente
load_dotenv()

# Chiave API OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY non trovata. Crea un file .env con la tua chiave API.")


def main():
    """
    Processo principale: estrae, analizza e salva le email
    """
    print("="*80)
    print("📧 EMAIL ANALYZER - Estrazione e Analisi Completa")
    print("="*80)
    
    # Step 1: Seleziona l'account Gmail
    print("\n🔐 Step 1: Selezione Account Gmail...")
    account_mgr = AccountManager()
    
    accounts = account_mgr.get_all_accounts()
    if len(accounts) > 1:
        print("\n👥 Account disponibili:")
        for i, acc in enumerate(accounts):
            active = "✓" if acc.get('active') else " "
            print(f"  [{i+1}] {active} {acc['name']} ({acc.get('email', 'N/A')})")
        
        choice = input("\nScegli l'account (invio per usare l'attivo): ").strip()
        if choice:
            try:
                account_mgr.set_active_account(int(choice) - 1)
            except:
                print("⚠️ Scelta non valida, uso account attivo")
    
    # Step 2: Connessione a Gmail
    print("\n🔐 Step 2: Connessione a Gmail...")
    extractor = GmailExtractor(account_manager=account_mgr)
    
    profile = extractor.get_profile()
    if profile:
        print(f"✅ Connesso a: {profile['emailAddress']}")
        print(f"📊 Totale messaggi nell'account: {profile['messagesTotal']}")
    
    # Chiedi conferma
    print("\n" + "="*80)
    risposta = input("Vuoi estrarre TUTTE le email per l'analisi? (s/n): ")
    
    if risposta.lower() not in ['s', 'si', 'sì', 'y', 'yes']:
        print("❌ Operazione annullata.")
        return
    
    print("\n🔍 Step 3: Estrazione email da Gmail...")
    emails = extractor.extract_all_emails()
    print(f"✅ Estratte {len(emails)} email!")
    
    # Step 3: Analizza le email con OpenAI
    print("\n🤖 Step 4: Analisi email con AI (OpenAI)...")
    print("⏳ Questo processo può richiedere alcuni minuti...")
    
    analyzer = EmailAnalyzer(api_key=OPENAI_API_KEY)
    analyzed_emails = analyzer.analyze_batch(emails)
    
    print(f"✅ Analizzate {len(analyzed_emails)} email!")
    
    # Step 4: Salva nel database
    print("\n💾 Step 5: Salvataggio nel database...")
    db = EmailDatabase()
    saved_count = db.save_batch(analyzed_emails)
    
    print(f"✅ Salvate {saved_count}/{len(analyzed_emails)} email nel database!")
    
    # Step 5: Mostra statistiche
    print("\n📊 Step 6: Statistiche")
    print("="*80)
    
    stats = db.get_statistics()
    print(f"Totale email nel database: {stats['total_emails']}")
    print(f"Sender unici: {stats['unique_senders']}")
    
    print("\n📧 Email per tipo:")
    for email_type, count in stats['email_types'].items():
        print(f"  - {email_type}: {count}")
    
    print("\n🎯 Email per funnel stage:")
    for stage, count in stats['funnel_stages'].items():
        print(f"  - {stage}: {count}")
    
    print("\n" + "="*80)
    print("✅ PROCESSO COMPLETATO!")
    print("="*80)
    print("\n🌐 Per visualizzare le email, avvia la web app:")
    print("   python app.py")
    print("\nPoi apri il browser su: http://localhost:5000")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Processo interrotto dall'utente.")
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        import traceback
        traceback.print_exc()

