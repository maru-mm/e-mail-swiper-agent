"""
Modulo per gestire il database delle email analizzate
"""

import sqlite3
import json
from typing import List, Dict, Optional
from datetime import datetime


class EmailDatabase:
    """
    Gestisce il database SQLite per le email analizzate
    """
    
    def __init__(self, db_path: str = 'emails.db'):
        """
        Inizializza il database
        
        Args:
            db_path: Path del file database
        """
        self.db_path = db_path
        self._create_tables()
    
    def _create_tables(self):
        """
        Crea le tabelle del database se non esistono
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabella principale per le email
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email_id TEXT UNIQUE,
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
                urls TEXT,
                labels TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Indici per query veloci
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sender ON emails(sender)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_email_type ON emails(email_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_campaign_type ON emails(campaign_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_funnel_stage ON emails(funnel_stage)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_date ON emails(date)')
        
        # Tabella per i prodotti dell'utente
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS my_products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                brief TEXT,
                documents_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabella per i documenti caricati
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                filename TEXT,
                file_type TEXT,
                extracted_text TEXT,
                file_size INTEGER,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES my_products(id) ON DELETE CASCADE
            )
        ''')
        
        # Tabella per salvare gli swipe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_swipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email_id TEXT,
                product_id INTEGER,
                swipe_notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES my_products(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_email(self, email: Dict) -> bool:
        """
        Salva un'email nel database
        
        Args:
            email: Dizionario con i dati dell'email
        
        Returns:
            True se salvata con successo
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Converti liste in JSON
            urls_json = json.dumps(email.get('urls', []))
            labels_json = json.dumps(email.get('labels', []))
            
            cursor.execute('''
                INSERT OR REPLACE INTO emails (
                    email_id, thread_id, sender, subject, email_body, snippet,
                    date, time_usa, notes, email_type, campaign_type,
                    pricing_extract, target_audience, product_mentioned,
                    retention, funnel_stage, urls, labels, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                email.get('email_id', ''),
                email.get('thread_id', ''),
                email.get('sender', ''),
                email.get('subject', ''),
                email.get('email_body', ''),
                email.get('snippet', ''),
                email.get('date', ''),
                email.get('time_usa', ''),
                email.get('notes', ''),
                email.get('email_type', ''),
                email.get('campaign_type', ''),
                email.get('pricing_extract', ''),
                email.get('target_audience', ''),
                email.get('product_mentioned', ''),
                email.get('retention', ''),
                email.get('funnel_stage', ''),
                urls_json,
                labels_json
            ))
            
            conn.commit()
            conn.close()
            return True
        
        except Exception as e:
            print(f"Errore durante il salvataggio dell'email: {e}")
            return False
    
    def save_batch(self, emails: List[Dict]) -> int:
        """
        Salva un batch di email
        
        Args:
            emails: Lista di email da salvare
        
        Returns:
            Numero di email salvate
        """
        saved_count = 0
        for email in emails:
            if self.save_email(email):
                saved_count += 1
        return saved_count
    
    def get_all_senders(self) -> List[Dict]:
        """
        Recupera tutti i sender unici con il conteggio delle email
        
        Returns:
            Lista di dizionari con sender e conteggio
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT sender, COUNT(*) as count
            FROM emails
            GROUP BY sender
            ORDER BY count DESC
        ''')
        
        senders = []
        for row in cursor.fetchall():
            senders.append({
                'sender': row[0],
                'count': row[1]
            })
        
        conn.close()
        return senders
    
    def get_emails_by_sender(self, sender: str) -> List[Dict]:
        """
        Recupera tutte le email di un sender specifico
        
        Args:
            sender: Email del sender
        
        Returns:
            Lista di email
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM emails
            WHERE sender = ?
            ORDER BY date DESC
        ''', (sender,))
        
        emails = []
        for row in cursor.fetchall():
            email = dict(row)
            # Parse JSON fields
            email['urls'] = json.loads(email.get('urls', '[]'))
            email['labels'] = json.loads(email.get('labels', '[]'))
            emails.append(email)
        
        conn.close()
        return emails
    
    def get_all_emails(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Recupera tutte le email
        
        Args:
            limit: Limite opzionale di email da recuperare
        
        Returns:
            Lista di email
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = 'SELECT * FROM emails ORDER BY date DESC'
        if limit:
            query += f' LIMIT {limit}'
        
        cursor.execute(query)
        
        emails = []
        for row in cursor.fetchall():
            email = dict(row)
            email['urls'] = json.loads(email.get('urls', '[]'))
            email['labels'] = json.loads(email.get('labels', '[]'))
            emails.append(email)
        
        conn.close()
        return emails
    
    def get_statistics(self) -> Dict:
        """
        Recupera statistiche sulle email
        
        Returns:
            Dizionario con statistiche
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Totale email
        cursor.execute('SELECT COUNT(*) FROM emails')
        total_emails = cursor.fetchone()[0]
        
        # Email per tipo
        cursor.execute('''
            SELECT email_type, COUNT(*) as count
            FROM emails
            GROUP BY email_type
            ORDER BY count DESC
        ''')
        email_types = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Email per funnel stage
        cursor.execute('''
            SELECT funnel_stage, COUNT(*) as count
            FROM emails
            GROUP BY funnel_stage
            ORDER BY count DESC
        ''')
        funnel_stages = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Sender unici
        cursor.execute('SELECT COUNT(DISTINCT sender) FROM emails')
        unique_senders = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_emails': total_emails,
            'unique_senders': unique_senders,
            'email_types': email_types,
            'funnel_stages': funnel_stages
        }
    
    def search_emails(self, query: str, field: str = 'all') -> List[Dict]:
        """
        Cerca email nel database
        
        Args:
            query: Termine di ricerca
            field: Campo in cui cercare ('all', 'sender', 'subject', 'body')
        
        Returns:
            Lista di email che corrispondono
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if field == 'all':
            sql = '''
                SELECT * FROM emails
                WHERE sender LIKE ? OR subject LIKE ? OR email_body LIKE ? OR snippet LIKE ?
                ORDER BY date DESC
            '''
            search_term = f'%{query}%'
            cursor.execute(sql, (search_term, search_term, search_term, search_term))
        else:
            sql = f'SELECT * FROM emails WHERE {field} LIKE ? ORDER BY date DESC'
            cursor.execute(sql, (f'%{query}%',))
        
        emails = []
        for row in cursor.fetchall():
            email = dict(row)
            email['urls'] = json.loads(email.get('urls', '[]'))
            email['labels'] = json.loads(email.get('labels', '[]'))
            emails.append(email)
        
        conn.close()
        return emails

