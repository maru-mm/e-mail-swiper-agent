"""
Servizio di monitoraggio automatico delle nuove email
Controlla periodicamente l'account Gmail e processa le nuove email con AI
"""

import time
import schedule
from datetime import datetime
from gmail_extractor import GmailExtractor
from email_analyzer import EmailAnalyzer
from database import EmailDatabase
from account_manager import AccountManager
import os
from dotenv import load_dotenv

# Carica variabili d'ambiente
load_dotenv()

# Configurazione
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY non trovata nel file .env")

CHECK_INTERVAL_MINUTES = int(os.getenv('CHECK_INTERVAL_MINUTES', 15))  # Controlla ogni 15 minuti


class EmailMonitor:
    """
    Monitora e processa automaticamente nuove email
    """
    
    def __init__(self, check_interval: int = CHECK_INTERVAL_MINUTES):
        """
        Inizializza il monitor
        
        Args:
            check_interval: Intervallo di controllo in minuti
        """
        self.check_interval = check_interval
        self.db = EmailDatabase()
        self.analyzer = EmailAnalyzer(api_key=OPENAI_API_KEY)
        self.extractor = None
        self.last_check = None
        self.running = False
        
        print("="*80)
        print("📧 EMAIL MONITOR - Servizio di Monitoraggio Automatico")
        print("="*80)
    
    def initialize_extractor(self):
        """
        Inizializza l'estrattore Gmail
        """
        try:
            # Usa account manager per supporto multi-account
            account_mgr = AccountManager()
            active = account_mgr.get_active_account()
            
            if active:
                print(f"\n📧 Account attivo: {active['name']}")
                if active.get('email'):
                    print(f"   Email: {active['email']}")
            
            self.extractor = GmailExtractor(account_manager=account_mgr)
            
            # Test connessione
            profile = self.extractor.get_profile()
            if profile:
                print(f"✅ Connesso a: {profile['emailAddress']}")
                print(f"📊 Totale messaggi: {profile['messagesTotal']}")
                return True
            else:
                print("❌ Impossibile connettersi a Gmail")
                return False
                
        except Exception as e:
            print(f"❌ Errore nell'inizializzazione: {e}")
            return False
    
    def get_existing_email_ids(self) -> set:
        """
        Recupera gli ID di tutte le email già nel database
        
        Returns:
            Set di email_id già presenti
        """
        emails = self.db.get_all_emails()
        return {email['email_id'] for email in emails if email.get('email_id')}
    
    def check_for_new_emails(self):
        """
        Controlla se ci sono nuove email e le processa
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{'='*80}")
        print(f"🔍 Controllo nuove email - {timestamp}")
        print(f"{'='*80}")
        
        try:
            # Recupera gli ID delle email già presenti
            existing_ids = self.get_existing_email_ids()
            print(f"📊 Email già nel database: {len(existing_ids)}")
            
            # Recupera le email più recenti (ultimi 50 messaggi)
            print("📥 Recupero messaggi recenti da Gmail...")
            messages = self.extractor.get_messages(max_results=50)
            
            # Filtra solo le nuove
            new_messages = [msg for msg in messages if msg['id'] not in existing_ids]
            
            if not new_messages:
                print("✅ Nessuna nuova email trovata")
                self.last_check = datetime.now()
                return
            
            print(f"\n🆕 Trovate {len(new_messages)} nuove email!")
            
            # Processa le nuove email
            new_emails_data = []
            for idx, message in enumerate(new_messages, 1):
                print(f"\n📧 Email {idx}/{len(new_messages)}...")
                
                # Estrai dettagli
                email_detail = self.extractor.get_message_detail(message['id'])
                
                if email_detail:
                    print(f"   Da: {email_detail.get('from', 'Unknown')}")
                    print(f"   Oggetto: {email_detail.get('subject', 'No subject')[:60]}...")
                    new_emails_data.append(email_detail)
            
            # Analizza con AI
            if new_emails_data:
                print(f"\n🤖 Analisi AI in corso per {len(new_emails_data)} email...")
                analyzed_emails = self.analyzer.analyze_batch(new_emails_data)
                
                # Salva nel database
                print(f"\n💾 Salvataggio nel database...")
                saved_count = self.db.save_batch(analyzed_emails)
                
                print(f"\n✅ Processate e salvate {saved_count} nuove email!")
                
                # Mostra riepilogo
                self.show_summary(analyzed_emails)
            
            self.last_check = datetime.now()
            
        except Exception as e:
            print(f"\n❌ Errore durante il controllo: {e}")
            import traceback
            traceback.print_exc()
    
    def show_summary(self, emails: list):
        """
        Mostra un riepilogo delle email processate
        
        Args:
            emails: Lista di email analizzate
        """
        print(f"\n{'='*80}")
        print("📊 RIEPILOGO NUOVE EMAIL")
        print(f"{'='*80}")
        
        # Raggruppa per tipo
        types = {}
        senders = set()
        
        for email in emails:
            email_type = email.get('email_type', 'unknown')
            types[email_type] = types.get(email_type, 0) + 1
            senders.add(email.get('sender', 'Unknown'))
        
        print(f"\n📧 Per tipo:")
        for email_type, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {email_type}: {count}")
        
        print(f"\n👥 Sender unici: {len(senders)}")
        
        # Mostra le prime 3 email
        print(f"\n🔝 Prime 3 email:")
        for idx, email in enumerate(emails[:3], 1):
            print(f"\n   {idx}. {email.get('subject', 'No subject')[:50]}...")
            print(f"      Da: {email.get('from', 'Unknown')[:40]}...")
            print(f"      Tipo: {email.get('email_type', 'unknown')}")
            if email.get('pricing_extract'):
                print(f"      💰 Offer: {email.get('pricing_extract', '')}")
    
    def start(self):
        """
        Avvia il servizio di monitoraggio
        """
        print(f"\n{'='*80}")
        print("🚀 AVVIO SERVIZIO MONITOR")
        print(f"{'='*80}")
        
        # Inizializza estrattore
        if not self.initialize_extractor():
            print("\n❌ Impossibile avviare il monitor. Verifica la configurazione Gmail.")
            return
        
        print(f"\n⏱️  Intervallo di controllo: ogni {self.check_interval} minuti")
        print(f"🤖 Analisi AI: Abilitata (OpenAI)")
        print(f"\n💡 Premi Ctrl+C per fermare il monitor\n")
        
        # Esegui il primo controllo immediatamente
        print("📍 Esecuzione primo controllo...")
        self.check_for_new_emails()
        
        # Schedula i controlli periodici
        schedule.every(self.check_interval).minutes.do(self.check_for_new_emails)
        
        self.running = True
        
        # Loop principale
        try:
            while self.running:
                schedule.run_pending()
                time.sleep(30)  # Controlla ogni 30 secondi se c'è qualcosa da eseguire
        
        except KeyboardInterrupt:
            print("\n\n⚠️ Monitor interrotto dall'utente")
            self.stop()
    
    def stop(self):
        """
        Ferma il servizio di monitoraggio
        """
        self.running = False
        print("\n✅ Servizio monitor fermato")
        print("="*80)


def main():
    """
    Funzione principale
    """
    # Crea e avvia il monitor
    monitor = EmailMonitor(check_interval=CHECK_INTERVAL_MINUTES)
    monitor.start()


if __name__ == '__main__':
    main()

