"""
Script per creare automaticamente le tabelle su Supabase
"""

from supabase_sync import SupabaseSync


def setup_tables():
    """
    Crea le tabelle necessarie su Supabase
    """
    print("="*80)
    print("☁️  SETUP TABELLE SUPABASE")
    print("="*80)
    
    # SQL per creare le tabelle
    sql_schema = """
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
    urls JSONB DEFAULT '[]'::jsonb,
    labels JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indici per performance
CREATE INDEX IF NOT EXISTS idx_emails_sender ON emails(sender);
CREATE INDEX IF NOT EXISTS idx_emails_type ON emails(email_type);
CREATE INDEX IF NOT EXISTS idx_emails_date ON emails(date);
CREATE INDEX IF NOT EXISTS idx_emails_created ON emails(created_at);

-- Tabella prodotti
CREATE TABLE IF NOT EXISTS my_products (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    brief TEXT,
    documents_text TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabella documenti prodotto
CREATE TABLE IF NOT EXISTS product_documents (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT REFERENCES my_products(id) ON DELETE CASCADE,
    filename TEXT,
    file_type TEXT,
    extracted_text TEXT,
    file_size INTEGER,
    uploaded_at TIMESTAMP DEFAULT NOW()
);

-- Tabella swipe email
CREATE TABLE IF NOT EXISTS email_swipes (
    id BIGSERIAL PRIMARY KEY,
    email_id TEXT,
    product_id BIGINT REFERENCES my_products(id),
    swipe_notes TEXT,
    swiped_subject TEXT,
    swiped_body TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Commenti
COMMENT ON TABLE emails IS 'Email estratte e analizzate da Gmail con AI';
COMMENT ON TABLE my_products IS 'Prodotti dell utente con brief e documenti';
COMMENT ON TABLE email_swipes IS 'Swipe email salvati';
"""
    
    print("\n📋 SQL Schema da eseguire su Supabase:")
    print("="*80)
    print(sql_schema)
    print("="*80)
    
    print("\n📝 ISTRUZIONI:")
    print("1. Vai su: https://app.supabase.com/project/gbxvxaksuuufbxowhalv/sql/new")
    print("2. Copia il SQL qui sopra")
    print("3. Click 'Run' (o premi F5)")
    print("4. Verifica che vedi: 'Success. No rows returned'")
    print("\nPoi riprova a testare la connessione.")
    
    # Testa la connessione
    print("\n🧪 Test connessione Supabase...")
    try:
        supabase = SupabaseSync()
        if supabase.test_connection():
            print("\n✅ Supabase connesso e pronto!")
        else:
            print("\n⚠️  Tabelle non ancora create. Segui le istruzioni sopra.")
    except Exception as e:
        print(f"\n❌ Errore: {e}")


if __name__ == '__main__':
    setup_tables()

