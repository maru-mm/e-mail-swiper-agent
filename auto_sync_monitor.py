"""
Monitor automatico che sincronizza nuove email con Supabase
Combina email_monitor.py con sync automatico a Supabase
"""

import time
import schedule
from datetime import datetime
from gmail_extractor import GmailExtractor
from email_analyzer import EmailAnalyzer
from database import EmailDatabase
from supabase_sync import SupabaseSync
from account_manager import AccountManager
import os
from dotenv import load_dotenv

load_dotenv()

# Configurazione
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CHECK_INTERVAL_MINUTES = int(os.getenv('CHECK_INTERVAL_MINUTES', 15))
ENABLE_SUPABASE = os.getenv('ENABLE_SUPABASE', 'true').lower() == 'true'


class AutoSyncMonitor:
    """
    Monitor che salva email sia in locale (SQLite) che in cloud (Supabase)
    """
    
    def __init__(self, check_interval: int = CHECK_INTERVAL_MINUTES):
        """
        Inizializza il monitor con sync Supabase
        """
        self.check_interval = check_interval
        self.local_db = EmailDatabase()
        self.analyzer = EmailAnalyzer(api_key=OPENAI_API_KEY)
        self.extractor = None
        self.supabase = None
        self.running = False
        
        print("="*80)
        print("☁️  AUTO-SYNC MONITOR - Gmail → SQLite → Supabase")
        print("="*80)
        
        # Inizializza Supabase se abilitato
        if ENABLE_SUPABASE:
            try:
                self.supabase = SupabaseSync()
                print("✅ Supabase abilitato e connesso")
            except Exception as e:
                print(f"⚠️  Supabase non configurato: {e}")
                print("   Le email verranno salvate solo in locale (SQLite)")
                self.supabase = None
        else:
            print("ℹ️  Supabase disabilitato - Solo storage locale")
    
    def initialize_extractor(self):
        """
        Inizializza l'estrattore Gmail
        """
        try:
            account_mgr = AccountManager()
            active = account_mgr.get_active_account()
            
            if active:
                print(f"\n📧 Account attivo: {active['name']}")
            
            self.extractor = GmailExtractor(account_manager=account_mgr)
            
            profile = self.extractor.get_profile()
            if profile:
                print(f"✅ Connesso a Gmail: {profile['emailAddress']}")
                return True
            return False
                
        except Exception as e:
            print(f"❌ Errore inizializzazione Gmail: {e}")
            return False
    
    def get_existing_email_ids(self) -> set:
        """
        Recupera gli ID delle email già nel database locale
        """
        emails = self.local_db.get_all_emails()
        return {email['email_id'] for email in emails if email.get('email_id')}
    
    def check_and_sync(self):
        """
        Controlla nuove email e sincronizza con Supabase
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{'='*80}")
        print(f"🔍 Controllo + Sync - {timestamp}")
        print(f"{'='*80}")
        
        try:
            # 1. Identifica nuove email
            existing_ids = self.get_existing_email_ids()
            print(f"📊 Email in database locale: {len(existing_ids)}")
            
            print("📥 Recupero email recenti da Gmail...")
            messages = self.extractor.get_messages(max_results=50)
            
            new_messages = [msg for msg in messages if msg['id'] not in existing_ids]
            
            if not new_messages:
                print("✅ Nessuna nuova email")
                return
            
            print(f"🆕 Trovate {len(new_messages)} nuove email!")
            
            # 2. Estrai dettagli
            new_emails_data = []
            for idx, message in enumerate(new_messages, 1):
                print(f"📧 Email {idx}/{len(new_messages)}...", end='\r')
                email_detail = self.extractor.get_message_detail(message['id'])
                if email_detail:
                    new_emails_data.append(email_detail)
            
            print()
            
            # 3. Analizza con AI
            print(f"🤖 Analisi AI per {len(new_emails_data)} email...")
            analyzed_emails = self.analyzer.analyze_batch(new_emails_data)
            
            # 4. Salva in locale (SQLite)
            print(f"💾 Salvataggio locale (SQLite)...")
            saved_local = self.local_db.save_batch(analyzed_emails)
            print(f"✅ Salvate localmente: {saved_local} email")
            
            # 5. Sincronizza con Supabase
            if self.supabase:
                print(f"☁️  Sincronizzazione cloud (Supabase)...")
                supabase_stats = self.supabase.sync_batch(analyzed_emails)
                print(f"✅ Sincronizzate su Supabase: {supabase_stats['success']} email")
            else:
                print("ℹ️  Supabase disabilitato - Skip sync cloud")
            
            # 6. Riepilogo
            self.show_summary(analyzed_emails)
            
        except Exception as e:
            print(f"\n❌ Errore durante controllo: {e}")
            import traceback
            traceback.print_exc()
    
    def show_summary(self, emails: list):
        """
        Mostra riepilogo delle email processate
        """
        print(f"\n{'='*80}")
        print("📊 RIEPILOGO")
        print(f"{'='*80}")
        
        types = {}
        for email in emails:
            email_type = email.get('email_type', 'unknown')
            types[email_type] = types.get(email_type, 0) + 1
        
        print(f"\n📧 Per tipo:")
        for email_type, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {email_type}: {count}")
        
        print(f"\n🔝 Prime email:")
        for idx, email in enumerate(emails[:3], 1):
            print(f"\n   {idx}. {email.get('subject', '')[:50]}...")
            print(f"      Da: {email.get('from', '')[:40]}...")
    
    def start(self):
        """
        Avvia il servizio
        """
        print(f"\n{'='*80}")
        print("🚀 AVVIO AUTO-SYNC MONITOR")
        print(f"{'='*80}")
        
        if not self.initialize_extractor():
            print("\n❌ Impossibile avviare")
            return
        
        print(f"\n⏱️  Intervallo: ogni {self.check_interval} minuti")
        print(f"🤖 Analisi AI: OpenAI GPT-4o")
        print(f"💾 Storage locale: SQLite (emails.db)")
        
        if self.supabase:
            print(f"☁️  Storage cloud: Supabase (sync automatico)")
        else:
            print(f"📍 Storage cloud: Disabilitato")
        
        print(f"\n💡 Premi Ctrl+C per fermare\n")
        
        # Primo controllo
        print("📍 Primo controllo...")
        self.check_and_sync()
        
        # Schedula controlli
        schedule.every(self.check_interval).minutes.do(self.check_and_sync)
        
        self.running = True
        
        try:
            while self.running:
                schedule.run_pending()
                time.sleep(30)
        
        except KeyboardInterrupt:
            print("\n\n⚠️ Monitor interrotto")
            self.stop()
    
    def stop(self):
        """
        Ferma il monitor
        """
        self.running = False
        print("\n✅ Monitor fermato")


def main():
    """
    Avvia il monitor con sync Supabase
    """
    monitor = AutoSyncMonitor()
    monitor.start()


if __name__ == '__main__':
    main()

