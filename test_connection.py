"""
Script di test per verificare la connessione a Gmail
"""

from gmail_extractor import GmailExtractor


def test_connection():
    """
    Testa la connessione a Gmail e mostra le informazioni base
    """
    print("="*80)
    print("TEST CONNESSIONE GMAIL")
    print("="*80)
    
    try:
        # Inizializza l'estrattore (farà OAuth se necessario)
        print("\nConnessione a Gmail...")
        extractor = GmailExtractor()
        
        # Recupera il profilo
        print("\nRecupero informazioni account...")
        profile = extractor.get_profile()
        
        if profile:
            print("\n✅ CONNESSIONE RIUSCITA!")
            print("\n" + "="*80)
            print("INFORMAZIONI ACCOUNT:")
            print("="*80)
            print(f"Email: {profile['emailAddress']}")
            print(f"Totale messaggi: {profile['messagesTotal']}")
            print(f"Totale thread: {profile['threadsTotal']}")
            print(f"Storia ID: {profile.get('historyId', 'N/A')}")
            
            # Mostra le etichette
            print("\n" + "="*80)
            print("ETICHETTE DISPONIBILI:")
            print("="*80)
            labels = extractor.get_labels()
            for label in labels:
                print(f"  • {label['name']} (ID: {label['id']})")
            
            # Test estrazione di 1 email
            print("\n" + "="*80)
            print("TEST ESTRAZIONE EMAIL:")
            print("="*80)
            print("Estrazione di 1 email di test...")
            
            test_emails = extractor.extract_all_emails(max_results=1)
            
            if test_emails:
                email = test_emails[0]
                print("\n✅ Email estratta con successo!")
                print(f"\nDa: {email['from']}")
                print(f"A: {email['to']}")
                print(f"Data: {email['date']}")
                print(f"Oggetto: {email['subject']}")
                print(f"Snippet: {email['snippet'][:100]}...")
                
                print("\n" + "="*80)
                print("✅ TUTTO OK! Il sistema è pronto per estrarre le email.")
                print("="*80)
                print("\nPer estrarre TUTTE le email, usa:")
                print("  python example_extract_all.py")
                print("\nOppure nel tuo codice:")
                print("  emails = extractor.extract_all_emails()")
            else:
                print("\n⚠️ Nessuna email trovata nell'account.")
        else:
            print("\n❌ Impossibile recuperare il profilo.")
    
    except FileNotFoundError as e:
        print("\n❌ ERRORE: File credentials.json non trovato!")
        print("\nSEGUI QUESTI PASSI:")
        print("1. Vai su https://console.cloud.google.com/")
        print("2. Crea un progetto e abilita Gmail API")
        print("3. Crea credenziali OAuth 2.0 (Desktop app)")
        print("4. Scarica il file JSON e rinominalo 'credentials.json'")
        print("5. Metti il file nella directory del progetto")
        print("\nLeggi README.md per istruzioni dettagliate.")
    
    except Exception as e:
        print(f"\n❌ ERRORE: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    test_connection()

