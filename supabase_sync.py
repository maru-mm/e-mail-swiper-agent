"""
Modulo per sincronizzare email con Supabase
"""

import os
from typing import List, Dict, Optional
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


class SupabaseSync:
    """
    Gestisce la sincronizzazione delle email con Supabase
    """
    
    def __init__(self, url: str = None, key: str = None):
        """
        Inizializza la connessione Supabase
        
        Args:
            url: URL del progetto Supabase (default da .env)
            key: API key Supabase (default da .env)
        """
        self.url = url or os.getenv('SUPABASE_URL')
        self.key = key or os.getenv('SUPABASE_KEY')
        
        if not self.url or not self.key:
            raise ValueError(
                "SUPABASE_URL e SUPABASE_KEY richiesti nel file .env\n"
                "Ottienili da: https://app.supabase.com/project/_/settings/api"
            )
        
        self.client: Client = create_client(self.url, self.key)
        print("✅ Connesso a Supabase")
    
    def create_tables(self):
        """
        Verifica/crea le tabelle necessarie su Supabase
        
        NOTA: Le tabelle devono essere create manualmente su Supabase UI
        Questo metodo è solo per reference dello schema
        """
        schema_sql = """
        -- Tabella principale email
        CREATE TABLE IF NOT EXISTS emails (
            id BIGSERIAL PRIMARY KEY,
            email_id TEXT UNIQUE NOT NULL,
            thread_id TEXT,
            sender TEXT,
            subject TEXT,
            email_body TEXT,
            snippet TEXT,
            date TEXT,
            time_usa TEXT,
            notes TEXT,
            email_type TEXT,
            campaign_type TEXT,
            pricing_extract TEXT,
            target_audience TEXT,
            product_mentioned TEXT,
            retention TEXT,
            funnel_stage TEXT,
            urls JSONB,
            labels JSONB,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );

        -- Indici per performance
        CREATE INDEX IF NOT EXISTS idx_sender ON emails(sender);
        CREATE INDEX IF NOT EXISTS idx_email_type ON emails(email_type);
        CREATE INDEX IF NOT EXISTS idx_date ON emails(date);

        -- Tabella prodotti
        CREATE TABLE IF NOT EXISTS my_products (
            id BIGSERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            brief TEXT,
            documents_text TEXT,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );

        -- Tabella swipe
        CREATE TABLE IF NOT EXISTS email_swipes (
            id BIGSERIAL PRIMARY KEY,
            email_id TEXT,
            product_id BIGINT REFERENCES my_products(id),
            swipe_notes TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        );
        """
        
        return schema_sql
    
    def sync_email(self, email: Dict) -> bool:
        """
        Sincronizza una singola email su Supabase
        
        Args:
            email: Dizionario con i dati dell'email
        
        Returns:
            True se sincronizzata con successo
        """
        try:
            # Prepara i dati secondo lo schema esistente su Supabase
            # Schema tabella e-mails: id, created_at, sender, body, subject
            data = {
                'sender': email.get('sender', ''),
                'subject': email.get('subject', ''),
                'body': email.get('email_body', '') or email.get('snippet', ''),
            }
            
            # Insert (ogni email viene inserita come nuova)
            result = self.client.table('e-mails').insert(data).execute()
            
            return True
        
        except Exception as e:
            error_msg = str(e)
            # Ignora duplicati se la tabella ha unique constraint
            if 'duplicate' in error_msg.lower() or 'unique' in error_msg.lower():
                return True  # Email già presente, non è un errore
            print(f"❌ Errore sync email: {error_msg}")
            return False
    
    def sync_batch(self, emails: List[Dict], batch_size: int = 50) -> Dict:
        """
        Sincronizza un batch di email
        
        Args:
            emails: Lista di email da sincronizzare
            batch_size: Dimensione del batch (default 50)
        
        Returns:
            Dizionario con statistiche sync
        """
        print(f"\n📤 Sincronizzazione {len(emails)} email su Supabase...")
        
        success_count = 0
        error_count = 0
        
        # Processa in batch
        for i in range(0, len(emails), batch_size):
            batch = emails[i:i + batch_size]
            print(f"   Batch {i//batch_size + 1}: {len(batch)} email...", end='\r')
            
            for email in batch:
                if self.sync_email(email):
                    success_count += 1
                else:
                    error_count += 1
        
        print()
        print(f"✅ Sincronizzate: {success_count}/{len(emails)}")
        if error_count > 0:
            print(f"⚠️  Errori: {error_count}")
        
        return {
            'total': len(emails),
            'success': success_count,
            'errors': error_count
        }
    
    def get_all_emails(self, limit: int = 1000) -> List[Dict]:
        """
        Recupera tutte le email da Supabase
        
        Args:
            limit: Numero massimo di email da recuperare
        
        Returns:
            Lista di email
        """
        try:
            response = self.client.table('e-mails').select('*').limit(limit).execute()
            return response.data
        except Exception as e:
            print(f"❌ Errore nel recupero email da Supabase: {e}")
            return []
    
    def get_emails_by_sender(self, sender: str) -> List[Dict]:
        """
        Recupera email di un sender specifico
        
        Args:
            sender: Email del sender
        
        Returns:
            Lista di email
        """
        try:
            response = self.client.table('e-mails').select('*').eq('sender', sender).execute()
            return response.data
        except Exception as e:
            print(f"❌ Errore: {e}")
            return []
    
    def sync_products(self, products: List[Dict]) -> bool:
        """
        Sincronizza i prodotti su Supabase
        
        Args:
            products: Lista di prodotti
        
        Returns:
            True se successo
        """
        try:
            for product in products:
                self.client.table('my_products').upsert(product).execute()
            print(f"✅ Sincronizzati {len(products)} prodotti")
            return True
        except Exception as e:
            print(f"❌ Errore sync prodotti: {e}")
            return False
    
    def test_connection(self) -> bool:
        """
        Testa la connessione a Supabase
        
        Returns:
            True se la connessione funziona
        """
        try:
            # Prova a fare una query semplice con le colonne esistenti
            result = self.client.table('e-mails').select('id, sender, subject').limit(1).execute()
            print(f"✅ Connessione Supabase OK - {len(result.data)} record trovati")
            if result.data:
                print(f"   Schema tabella: {list(result.data[0].keys())}")
            return True
        except Exception as e:
            print(f"❌ Errore connessione Supabase: {e}")
            return False

