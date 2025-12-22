"""
Script veloce per cambiare account Gmail
"""

from account_manager import AccountManager


def main():
    """
    Menu veloce per cambiare account
    """
    manager = AccountManager()
    accounts = manager.get_all_accounts()
    
    print("="*80)
    print("🔄 CAMBIO ACCOUNT GMAIL")
    print("="*80)
    
    if not accounts:
        print("\n⚠️ Nessun account configurato.")
        print("Esegui: python account_manager.py per configurare gli account")
        return
    
    print("\n👥 Account disponibili:\n")
    for i, account in enumerate(accounts):
        active = "✓ ATTIVO" if account.get('active') else "  "
        print(f"  [{i+1}] {active} {account['name']}")
        if account.get('email'):
            print(f"      📧 {account['email']}")
        print(f"      🔑 {account['client_id'][:40]}...")
        print()
    
    choice = input("Seleziona account (numero): ").strip()
    
    try:
        index = int(choice) - 1
        if manager.set_active_account(index):
            selected = accounts[index]
            print(f"\n✅ Account '{selected['name']}' attivato!")
            
            # Genera il file credentials.json
            manager.create_credentials_file(selected)
            
            print("\n💡 Ora puoi eseguire:")
            print("   python process_emails.py")
            print("   python test_connection.py")
        else:
            print("\n❌ Indice non valido.")
    except (ValueError, IndexError):
        print("\n❌ Input non valido.")


if __name__ == '__main__':
    main()

