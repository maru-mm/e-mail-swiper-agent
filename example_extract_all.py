"""
Esempio: Estrae TUTTE le email dall'account Gmail
"""

import json
from gmail_extractor import GmailExtractor


def main():
    """
    Estrae tutte le email dall'account Gmail
    """
    print("="*80)
    print("ESTRAZIONE COMPLETA EMAIL DA GMAIL")
    print("="*80)
    
    # Inizializza l'estrattore
    extractor = GmailExtractor()
    
    # Mostra informazioni account
    profile = extractor.get_profile()
    if profile:
        print(f"\nAccount: {profile['emailAddress']}")
        print(f"Totale messaggi nell'account: {profile['messagesTotal']}")
        print(f"Totale thread: {profile['threadsTotal']}")
        print(f"\nATTENZIONE: L'estrazione di {profile['messagesTotal']} email può richiedere tempo!")
        
        # Chiedi conferma
        risposta = input("\nVuoi procedere con l'estrazione di TUTTE le email? (s/n): ")
        
        if risposta.lower() in ['s', 'si', 'sì', 'y', 'yes']:
            print("\nInizio estrazione...")
            
            # ESTRAI TUTTE LE EMAIL (senza limite)
            # Nota: Non specificare max_results o passa None per estrarre tutte
            emails = extractor.extract_all_emails()
            
            # Salva in un file JSON
            output_file = 'tutte_le_email.json'
            print(f"\nSalvataggio di {len(emails)} email nel file '{output_file}'...")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(emails, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Completato! {len(emails)} email salvate in '{output_file}'")
            
            # Mostra statistiche
            print("\n" + "="*80)
            print("STATISTICHE:")
            print("="*80)
            
            # Conta email lette/non lette
            unread_count = sum(1 for email in emails if 'UNREAD' in email.get('labels', []))
            read_count = len(emails) - unread_count
            
            print(f"Email totali estratte: {len(emails)}")
            print(f"Email lette: {read_count}")
            print(f"Email non lette: {unread_count}")
            
            # Conta mittenti unici
            senders = set(email.get('from', '') for email in emails)
            print(f"Mittenti unici: {len(senders)}")
            
            # Mostra prime 5 email come esempio
            print("\n" + "="*80)
            print("PRIME 5 EMAIL (ESEMPIO):")
            print("="*80)
            
            for idx, email in enumerate(emails[:5], 1):
                print(f"\nEmail #{idx}")
                print(f"Da: {email['from']}")
                print(f"Oggetto: {email['subject']}")
                print(f"Data: {email['date']}")
                print(f"Labels: {', '.join(email.get('labels', []))}")
                print("-"*80)
        else:
            print("\nOperazione annullata.")
            print("\nPer estrarre un numero limitato di email, puoi usare:")
            print("  emails = extractor.extract_all_emails(max_results=100)")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nEstrazione interrotta dall'utente.")
    except Exception as e:
        print(f"\nErrore: {e}")
        import traceback
        traceback.print_exc()

