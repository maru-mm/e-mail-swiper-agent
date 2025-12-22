"""
Script rapido per autenticare Account 2
"""

from account_manager import AccountManager
from gmail_extractor import GmailExtractor

print("="*80)
print("🔐 AUTENTICAZIONE ACCOUNT 2")
print("="*80)

manager = AccountManager()
active = manager.get_active_account()

print(f"\n✅ Account attivo: {active['name']}")
print(f"🔑 Client ID: {active['client_id']}")
print(f"\n⚠️  IMPORTANTE:")
print(f"   Devi aver aggiunto l'email Gmail come 'Utente di test' su:")
print(f"   https://console.cloud.google.com/apis/credentials/consent?project=273042617440")
print(f"\n🌐 Il browser si aprirà per l'autenticazione...")
print(f"   Scegli l'email che hai aggiunto come utente di test!\n")

input("Premi INVIO per continuare...")

try:
    extractor = GmailExtractor(account_manager=manager)
    profile = extractor.get_profile()
    
    if profile:
        print(f"\n✅ AUTENTICAZIONE RIUSCITA!")
        print(f"📧 Email: {profile['emailAddress']}")
        print(f"📊 Totale messaggi: {profile['messagesTotal']}")
        print(f"💾 Token salvato in: {active['token_file']}")
        
        # Aggiorna l'email nell'account se non c'è
        if not active.get('email'):
            active['email'] = profile['emailAddress']
            manager._save_accounts()
            print(f"\n✅ Email aggiunta alla configurazione account!")
    else:
        print("\n❌ Errore: impossibile recuperare il profilo")
        
except Exception as e:
    print(f"\n❌ ERRORE: {e}")
    print(f"\n💡 Soluzioni:")
    print(f"   1. Verifica di aver aggiunto l'email come 'Utente di test'")
    print(f"   2. Aspetta 1-2 minuti dopo averla aggiunta")
    print(f"   3. Verifica i redirect URI: http://localhost:8080/")
    print(f"   4. Riprova tra qualche minuto")


